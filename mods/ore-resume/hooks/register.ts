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
export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'ore-resume-status', description: 'Read the persisted ORE task without running a model' });
    const task = await load($);
    if (task && task.status !== 'complete') $.ui.log(`ORE handoff: ${handoff(task)}`);
    return next(e);
  });
  on('command.run', { command: 'ore-resume-status' }, async ($) => {
    const task = await load($);
    return { text: task ? handoff(task) : 'No valid ORE state' };
  });
};
