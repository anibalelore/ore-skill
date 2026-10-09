import type { EngineInterface, Register, Timer, RenderElement } from 'claude-code';
import { pointer, parseTask, handoff, department } from './state.ts';
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
let current: Task | null = null;
let timer: Timer | undefined;
let busy = false;
let generation = 0;

async function refresh($: EngineInterface, epoch: number): Promise<void> {
  if (busy) return;
  busy = true;
  try {
    const task = await load($);
    if (epoch !== generation) return;
    current = task;
    $.ui.invalidate('ui.render');
  } finally { busy = false; }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'ore-departments-status', description: 'Read the persisted ORE task without running a model' });
    timer?.cancel();
    const epoch = ++generation;
    current = null;
    await refresh($, epoch);
    timer = $.clock.every(1000, () => { void refresh($, epoch).catch(() => {}); });
    return next(e);
  });
  on('session.end', ($, e, next) => {
    if (e.reason === 'clear' || e.reason === 'resume') return next(e);
    ++generation;
    timer?.cancel();
    current = null;
    return next(e);
  });
  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const base = await next(e);
    if (!current) return base;
    const { Box, Text } = $.ui.resolve(e);
    return h(Box, { flexDirection: 'column' }, base, h(Text, {}, department(current))) as RenderElement;
  });
  on('command.run', { command: 'ore-departments-status' }, async ($) => {
    const task = await load($);
    return { text: task ? handoff(task) : 'No valid ORE state' };
  });
};
