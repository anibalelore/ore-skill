// Run the real TypeScript modules with an in-memory host; never run a tool.
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
const input = JSON.parse(readFileSync(0, 'utf8'));
const folder = resolve('mods', input.mod ?? 'ore-progress', 'hooks');
const state = await import(pathToFileURL(resolve(folder, 'state.ts')));
const rawPointer = input.pointer === undefined ? JSON.stringify({ schema_version: 1, task_id: 'fixture' }) : input.pointer;
const id = state.pointer(rawPointer);
const raw = typeof input.task === 'string' ? input.task : JSON.stringify(input.task);
const task = id ? state.parseTask(raw, id) : null;
if (input.mode === 'projection') {
  process.stdout.write(JSON.stringify(task ? { task, next: state.nextDeliverable(task), gates: state.pendingGates(task), department: state.department(task), changed: state.revisionChanged(state.parseTask(JSON.stringify(input.previous), id), task) } : null));
} else {
  globalThis.h = (type, props, ...children) => ({ type, props, children });
  const handlers = new Map();
  const on = (event, matcher, fn) => {
    if (typeof matcher === 'function') fn = matcher;
    handlers.set(event, fn);
    return { catch() {} };
  };
  const register = await import(pathToFileURL(resolve(folder, 'register.ts')));
  register.register(on, { approvalMode: 'ask', ...input.options });
  const logs = [];
  let tick;
  let asks = 0;
  const questions = [];
  const notices = [];
  let passed = 0;
  let currentRaw = raw;
  const callEvent = input.event ?? { tool: 'Bash', tool_use_id: 'fixture-call', command: input.tool };
  const $ = {
    command: { register: async () => {} },
    session: { cwd: async () => '/workspace' },
    fs: { read: async path => {
      if (input.missing) throw new Error('ENOENT');
      return path.endsWith('active.json') ? rawPointer : currentRaw;
    } },
    clock: { every: (ms, fn) => { tick = fn; return { cancel() { tick = undefined; } }; } },
    ui: {
      notice(id, text) {
        if (input.noticeFailure) throw new Error('notice unavailable');
        if (id !== callEvent.tool_use_id) throw new Error('wrong call');
        notices.push({ id, text });
      },
      invalidate() {}, log(text) { logs.push(text); },
      resolve() { return { Box: 'Box', Text: 'Text' }; },
      ask: async (question, options) => {
        asks++;
        questions.push({ question, options });
        if (input.dismiss) throw new Error('dismissed');
        if (input.changeDuringAsk) currentRaw = JSON.stringify({ ...input.task, revision: input.task.revision + 1 });
        if (input.changeActionDuringAsk) callEvent.command += '; rm -rf data';
        return input.answers?.[asks - 1] ?? input.answer ?? 'Cancel';
      },
    },
  };
  const next = async () => { passed++; return { type: 'Base', props: {}, children: [] }; };
  next.signal = { aborted: input.aborted ?? false };
  if (handlers.has('session.start')) await handlers.get('session.start')($, {}, next);
  if (input.tool && handlers.has('tool.call')) {
    passed = 0;
    const result = await handlers.get('tool.call')($, callEvent, next);
    process.stdout.write(JSON.stringify({ result, asks, passed, logs, questions, notices }));
  } else {
    if (input.updated && tick) {
      currentRaw = JSON.stringify(input.updated);
      tick();
      await new Promise(resolve => setImmediate(resolve));
    }
    if (input.endTurn && handlers.has('turn.complete')) await handlers.get('turn.complete')($, {}, next);
    const drawing = handlers.has('ui.render') ? await handlers.get('ui.render')($, {}, next) : null;
    process.stdout.write(JSON.stringify({ drawing, logs }));
  }
}
