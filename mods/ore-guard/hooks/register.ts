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
import { classify } from './risk.ts';
import { summarize, renderApproval, renderNotice, APPROVE, REJECT, DETAILS } from './approval.ts';

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
    if (risk === 'Invalid guard pattern configuration') return { deny: 'ORE guard: invalid review configuration; fix it before execution.' };
    try {
      const snapshot = JSON.stringify(e);
      const review = summarize(e.tool, e, task.title, 'La acción puede modificar recursos o tener efectos externos.');
      if (review.blocked) return { deny: review.blocked };
      // Bound to this pending call; the engine removes it when the call resolves.
      // Never replace its permission dialog or change the action being authorized.
      $.ui.notice(e.tool_use_id, renderNotice(review));
      let answer = options.approvalMode === 'ask' ? await $.ui.ask(renderApproval(review), [REJECT, DETAILS]) : DETAILS;
      if (answer !== DETAILS) return { deny: 'ORE guard: exact details were not reviewed.' };
      if (answer === DETAILS) answer = options.approvalMode === 'ask' ? await $.ui.ask(renderApproval(review, true), [APPROVE, REJECT]) : APPROVE;
      if (answer !== APPROVE || next.signal.aborted || JSON.stringify(e) !== snapshot) return { deny: 'ORE guard: explicit approval was not granted for this exact action.' };
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
