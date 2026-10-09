// Execute actual native TypeScript handlers with a deterministic host adapter.
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
const input = JSON.parse(readFileSync(0, 'utf8'));
const handlers = [];
const on = (event, matcher, fn) => {
  if (typeof matcher === 'function') { fn = matcher; matcher = {}; }
  handlers.push({ event, matcher, fn });
  return { catch() {} };
};
const mod = await import(pathToFileURL(resolve('mods', input.mod, 'hooks/register.ts')));
mod.register(on, {});
let processes = 0, passed = 0, asks = 0;
let lastPayload = null, lastQuestion = null;
const questions = [];
const notices = [];
const $ = {
  plugin: { root: '/plugin' },
  command: { register: async () => {} },
  session: { cwd: async () => '/workspace', id: async () => 'observed-session', model: async () => 'observed-model', usage: async () => ({ context: { used: 100 }, cost: { total: 0.1 } }) },
  fs: { read: async path => {
    if (input.missing) throw new Error('ENOENT');
    if (path.endsWith('governance.json')) {
      if (input.corruptGovernance) return '{';
      return JSON.stringify(input.governance);
    }
    return path.endsWith('active.json') ? JSON.stringify({ schema_version: 1, task_id: 'fixture' }) : JSON.stringify(input.task);
  } },
  process: { run: async argv => {
    processes++;
    const payloadIndex = argv.indexOf('--payload');
    if (payloadIndex >= 0) lastPayload = JSON.parse(argv[payloadIndex + 1]);
    if (input.runtimeUnavailable) throw new Error('Python unavailable');
    return { exitCode: 0, stdout: JSON.stringify(input.result ?? { runtime_result: { allowed: true } }), stderr: '', isStdoutTruncated: false };
  } },
  ui: { notice(id, text) { if (input.noticeFailure) throw new Error('notice unavailable'); notices.push({ id, text }); }, ask: async (question, options) => { asks++; lastQuestion = question; questions.push({ question, options }); if (input.dismiss) throw new Error('dismissed'); return input.answers?.[asks - 1] ?? input.answer ?? 'Cancel'; } }
};
const event = input.tool ? 'tool.call' : 'command.run';
const continuation = async () => { passed++; return { continued: true }; };
continuation.signal = { aborted: input.aborted ?? false };
const target = handlers.find(h => h.event === event && (input.tool ? h.matcher.tool === input.tool : h.matcher.command === input.mod));
const result = await target.fn($, input.tool ? { tool: input.tool, tool_use_id: 'fixture-file', file_path: '/workspace/src/a.py' } : { args: JSON.stringify(input.request ?? {}) }, continuation);
process.stdout.write(JSON.stringify({ result, processes, passed, asks, lastPayload, lastQuestion, questions, notices }));
