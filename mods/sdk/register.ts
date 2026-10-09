import type { EngineInterface, Register } from 'claude-code';
import { pointer, parseTask, handoff } from './state.ts';
import type { Task } from './state.ts';
import { NAME } from './identity.ts';
import { summarize, renderApproval, APPROVE, REJECT, DETAILS } from './approval.ts';

function validGovernance(value: unknown): boolean {
  if (!value || typeof value !== 'object') return false;
  const data = value as Record<string, unknown>;
  if (data.schema_version !== 1 || typeof data.project !== 'string' || !Number.isInteger(data.revision)) return false;
  for (const key of ['rules', 'approvals', 'exceptions', 'events']) {
    if (!Array.isArray(data[key]) || !(data[key] as unknown[]).every(r => r && typeof r === 'object')) return false;
  }
  return (data.rules as Record<string, unknown>[]).every(r =>
    typeof r.id === 'string' && r.project === data.project &&
    ['active', 'revoked', 'replaced'].includes(String(r.status)) &&
    ['allow-paths', 'forbid-paths', 'review'].includes(String(r.kind)) &&
    Array.isArray(r.paths) && r.paths.length > 0 && r.paths.every(p => typeof p === 'string') &&
    (!r.expires_at || typeof r.expires_at === 'string' && Number.isFinite(Date.parse(r.expires_at))));
}

function display(value: unknown): string {
  return JSON.stringify(value, null, 2).replace(/((?:password|secret|token|api[_-]?key|authorization)\s*["']?\s*[:=]\s*["']?)[^\s",}]+/gi, '$1[redacted]');
}

// Vendored into each plugin. Host calls remain here for permission auditing.
async function load($: EngineInterface): Promise<Task | null> {
  try {
    const root = await $.session.cwd();
    const raw = await $.fs.read(`${root}/.ore/active.json`);
    const id = pointer(raw);
    if (!id) return null;
    const task = parseTask(await $.fs.read(`${root}/.ore/tasks/${id}.json`), id);
    return pointer(await $.fs.read(`${root}/.ore/active.json`)) === id ? task : null;
  } catch { return null; }
}

async function runtime($: EngineInterface, task: Task, payload: Record<string, unknown>, action: string, python: string, governanceRevision = 0) {
  const root = await $.session.cwd();
  const argv = [python, `${$.plugin.root}/scripts/ore_state.py`, 'runtime', '--repo', root,
    '--task-id', task.id, '--expect-revision', String(task.revision), '--mod', NAME,
    '--action', action, '--payload', JSON.stringify(payload)];
  if (action !== 'evaluate') argv.push('--confirmed', '--expect-governance-revision', String(governanceRevision));
  const result = await $.process.run(argv, { cwd: root, timeoutMs: 90000 });
  if (result.exitCode || result.isStdoutTruncated) throw new Error(result.stderr.slice(0, 1000) || 'Runtime operation failed');
  return JSON.parse(result.stdout) as { runtime_result?: Record<string, unknown>; governance?: unknown };
}

export const register: Register = (on, options) => {
  const python = typeof options.pythonCommand === 'string' ? options.pythonCommand : 'python';
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: NAME, description: 'Explicit ORE runtime operation; JSON arguments, no model call' });
    await $.command.register({ name: `${NAME}-status`, description: 'Read persisted ORE task state' });
    return next(e);
  });
  on('command.run', { command: `${NAME}-status` }, async ($) => {
    const task = await load($);
    if (task && ['ore-scope-lock', 'ore-never-again', 'ore-approval-ledger'].includes(NAME)) {
      try { return { text: `${handoff(task)}\n${display(await runtime($, task, {}, 'evaluate', python))}` }; }
      catch { return { text: `${handoff(task)}\nGovernance runtime unavailable` }; }
    }
    return { text: task ? handoff(task) : 'No valid ORE state' };
  });
  on('command.run', { command: NAME }, async ($, e) => {
    const task = await load($);
    if (!task || task.status === 'complete') return { text: 'No active valid ORE state; no action performed' };
    try {
      const input: unknown = e.args.trim() ? JSON.parse(e.args) : {};
      if (!input || typeof input !== 'object' || Array.isArray(input)) throw new Error('Expected a JSON object');
      const request = input as Record<string, unknown>;
      const action = typeof request.action === 'string' ? request.action : 'evaluate';
      const payload = (request.payload ?? request) as Record<string, unknown>;
      const governanceRevision = typeof request.governanceRevision === 'number' ? request.governanceRevision : 0;
      if (NAME === 'ore-first-contact' && payload.run_browser === true) {
        const review = summarize(NAME, payload, task.title, 'Explorar la aplicación local aislada con un navegador.');
        if (review.blocked) return { text: review.blocked, exitCode: 2 };
        let answer = await $.ui.ask(renderApproval(review), [APPROVE, REJECT, DETAILS]);
        if (answer === DETAILS) answer = await $.ui.ask(renderApproval(review, true), [APPROVE, REJECT]);
        if (answer !== APPROVE) return { text: 'Cancelled; no browser started' };
      }
      if (action !== 'evaluate') {
        const review = summarize(NAME, { action, payload, task_revision: task.revision, governance_revision: governanceRevision }, task.title, 'Guardar una decisión explícita con alcance y vigencia en el proyecto.');
        if (review.blocked) return { text: review.blocked, exitCode: 2 };
        let answer = await $.ui.ask(renderApproval(review), [REJECT, DETAILS]);
        if (answer !== DETAILS) return { text: 'Cancelled; exact details were not reviewed' };
        answer = await $.ui.ask(renderApproval(review, true), [APPROVE, REJECT]);
        if (answer !== APPROVE) return { text: 'Cancelled; no state written' };
        const current = await load($);
        if (!current || current.id !== task.id || current.revision !== task.revision) throw new Error('State changed during confirmation');
      }
      return { text: display(await runtime($, task, payload, action, python, governanceRevision)) };
    } catch { return { text: 'ORE operation blocked: input, presentation or runtime unavailable; no authorization was expanded.', exitCode: 2 }; }
  });
  // Path restrictions apply only to declared file edits. Shell scripts are not inspected.
  if (NAME === 'ore-scope-lock' || NAME === 'ore-never-again') {
    on('tool.call', { tool: 'Write' }, async ($, e, next) => {
      const task = await load($);
      if (!task || task.status === 'complete') return next(e);
      let reviewing = false;
      try {
        // No governance, invalid JSON: optional layer is inert.
        const root = await $.session.cwd();
        const governance = JSON.parse(await $.fs.read(`${root}/.ore/governance.json`));
        if (!validGovernance(governance)) return next(e);
        reviewing = true;
        const result = await runtime($, task, { paths: [e.file_path] }, 'evaluate', python);
        const check = result.runtime_result;
        if (check?.allowed === false) return { deny: `ORE path restriction: ${JSON.stringify(check.violations)}` };
        if (Array.isArray(check?.review_required) && check.review_required.length) {
          const snapshot = JSON.stringify(e);
          const review = summarize('Write', { ...e, review_required: check.review_required }, task.title, 'Revisar las reglas de alcance antes de modificar el archivo.');
          if (review.blocked) return { deny: review.blocked };
          let answer = await $.ui.ask(renderApproval(review), [REJECT, DETAILS]);
          if (answer !== DETAILS) return { deny: 'ORE review: exact details were not reviewed' };
          answer = await $.ui.ask(renderApproval(review, true), [APPROVE, REJECT]);
          if (answer !== APPROVE || JSON.stringify(e) !== snapshot || next.signal.aborted) return { deny: 'ORE review was not approved for the unchanged action' };
          const current = await load($);
          if (!current || current.id !== task.id || current.revision !== task.revision || JSON.stringify(await runtime($, task, { paths: [e.file_path] }, 'evaluate', python)) !== JSON.stringify(result)) return { deny: 'ORE state changed during review; review again' };
        }
        return next(e);
      } catch (error) {
        if (!reviewing) return next(e);
        return { deny: 'ORE could not enforce the active rule; reload state or fix the runtime before editing' };
      }
    }).catch(() => ({ deny: 'ORE path review failed' }));
    on('tool.call', { tool: 'Edit' }, async ($, e, next) => {
      const task = await load($);
      if (!task || task.status === 'complete') return next(e);
      let reviewing = false;
      try {
        const root = await $.session.cwd();
        const governance = JSON.parse(await $.fs.read(`${root}/.ore/governance.json`));
        if (!validGovernance(governance)) return next(e);
        reviewing = true;
        const result = await runtime($, task, { paths: [e.file_path] }, 'evaluate', python);
        const check = result.runtime_result;
        if (check?.allowed === false) return { deny: `ORE path restriction: ${JSON.stringify(check.violations)}` };
        if (Array.isArray(check?.review_required) && check.review_required.length) {
          const snapshot = JSON.stringify(e);
          const review = summarize('Edit', { ...e, review_required: check.review_required }, task.title, 'Revisar las reglas de alcance antes de modificar el archivo.');
          if (review.blocked) return { deny: review.blocked };
          let answer = await $.ui.ask(renderApproval(review), [REJECT, DETAILS]);
          if (answer !== DETAILS) return { deny: 'ORE review: exact details were not reviewed' };
          answer = await $.ui.ask(renderApproval(review, true), [APPROVE, REJECT]);
          if (answer !== APPROVE || JSON.stringify(e) !== snapshot || next.signal.aborted) return { deny: 'ORE review was not approved for the unchanged action' };
          const current = await load($);
          if (!current || current.id !== task.id || current.revision !== task.revision || JSON.stringify(await runtime($, task, { paths: [e.file_path] }, 'evaluate', python)) !== JSON.stringify(result)) return { deny: 'ORE state changed during review; review again' };
        }
        return next(e);
      } catch (error) {
        if (!reviewing) return next(e);
        return { deny: 'ORE could not enforce the active rule; reload state or fix the runtime before editing' };
      }
    }).catch(() => ({ deny: 'ORE path review failed' }));
  }
};
