import type { EngineInterface, Register } from 'claude-code';
import { pointer, parseTask, handoff } from './state.ts';
import type { Task } from './state.ts';

async function load($: EngineInterface): Promise<Task | null> {
  try {
    const root = await $.session.cwd();
    const id = pointer(await $.fs.read(`${root}/.ore/active.json`));
    if (!id) return null;
    const task = parseTask(await $.fs.read(`${root}/.ore/tasks/${id}.json`), id);
    return pointer(await $.fs.read(`${root}/.ore/active.json`)) === id ? task : null;
  } catch { return null; }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'ore-worktree-manager', description: 'Read actual Git worktree topology; no creation or merging' });
    await $.command.register({ name: 'ore-worktree-manager-status', description: 'Read persisted ORE handoff' });
    return next(e);
  });
  on('command.run', { command: 'ore-worktree-manager-status' }, async ($) => {
    const task = await load($);
    return { text: task ? handoff(task) : 'No valid ORE state' };
  });
  on('command.run', { command: 'ore-worktree-manager' }, async ($) => {
    const task = await load($);
    if (!task || task.status === 'complete') return { text: 'No active valid ORE state' };
    const result = await $.process.run(['git', 'worktree', 'list', '--porcelain'], { cwd: await $.session.cwd() });
    return { text: JSON.stringify({ exitCode: result.exitCode, topology: result.stdout, created: false, merged: false }), exitCode: result.exitCode };
  }).catch(() => ({ text: 'Git worktree topology unavailable', exitCode: 2 }));
};
