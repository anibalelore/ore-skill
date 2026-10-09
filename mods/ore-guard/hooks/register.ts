import type { EngineInterface, Register } from 'claude-code';
import { pointer, parseTask, handoff } from './state.ts';
import type { Task } from './state.ts';

// All host calls stay in this module for static permission auditing.
async function load($: EngineInterface): Promise<Task | null> {
  try {
    const root = await $.session.cwd();
    const active = `${root}/.ore/active.json`;
    const raw = await $.fs.read(active);
    const id = pointer(raw);
    if (!id) return null;
    const task = parseTask(await $.fs.read(`${root}/.ore/tasks/${id}.json`), id);
    // A writer can replace the pointer while the task is being read.
    return pointer(await $.fs.read(active)) === id ? task : null;
  } catch { return null; }
}
import { classify, preview } from './risk.ts';

export const register: Register = (on, options) => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'ore-guard-status', description: 'Read the persisted ORE task without running a model' });
    return next(e);
  });
  on('tool.call', async ($, e, next) => {
    if (e.tool === 'AskUserQuestion') return next(e);
    const task = await load($);
    if (!task || task.status === 'complete') return next(e);
    const risk = classify(e.tool, e, options.patterns);
    if (!risk) return next(e);
    const report = `ORE task: ${task.title} (r${task.revision})\n${risk}\nAction arguments: ${preview(e)}\nImpact is limited to declared arguments; remote effects and hidden script contents are not measured. Proceed with this action?`;
    try {
      const answer = await $.ui.ask(report, ['Cancel', 'Proceed once']);
      if (answer !== 'Proceed once' || next.signal.aborted) return { deny: 'ORE guard: explicit approval was not granted for this action.' };
      const latest = await load($);
      if (!latest || latest.id !== task.id || latest.revision !== task.revision) return { deny: 'ORE guard: state changed during confirmation; resume and review the action again.' };
    } catch {
      return { deny: 'ORE guard: confirmation unavailable or dismissed; action was not executed.' };
    }
    // Approval does not bypass native permission rules or other hooks.
    return next(e);
  }).catch(() => ({ deny: 'ORE guard failed to review the action; it was not executed.' }));
  on('command.run', { command: 'ore-guard-status' }, async ($) => {
    const task = await load($);
    return { text: task ? handoff(task) : 'No valid ORE state' };
  });
};
