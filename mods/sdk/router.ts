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

async function status($: EngineInterface) {
  const task = await load($);
  return { text: JSON.stringify({ handoff: task ? handoff(task) : 'No valid ORE state',
    effectiveModel: await $.session.model(), reportedUsage: await $.session.usage(),
    observedEffort: null, savings: null, modelChanged: false, execution: 'manual-host-selection-required' }, null, 2) };
}

export const register: Register = (on, options) => {
  const python = typeof options.pythonCommand === 'string' ? options.pythonCommand : 'python';
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'ore-model-router', description: 'Evaluate routing or confirm scoped metadata; never changes the host model' });
    await $.command.register({ name: 'ore-model-router-status', description: 'Observe current model and native usage' });
    return next(e);
  });
  on('command.run', { command: 'ore-model-router-status' }, status)
    .catch(() => ({ text: 'Host model/usage observation unavailable', exitCode: 2 }));
  on('command.run', { command: 'ore-model-router' }, async ($, e) => {
    if (!e.args.trim()) return status($);
    const task = await load($);
    if (!task || task.status === 'complete') return { text: 'No active valid ORE state; no action performed' };
    try {
      const request = JSON.parse(e.args) as Record<string, unknown>;
      if (!request || typeof request !== 'object' || Array.isArray(request)) throw new Error('Expected JSON object');
      const action = request.action ?? 'evaluate';
      if (!['evaluate', 'model-policy', 'model-decision'].includes(String(action))) throw new Error('Unsupported router action');
      const raw = request.payload ?? request;
      if (!raw || typeof raw !== 'object' || Array.isArray(raw)) throw new Error('Expected payload object');
      const payload: Record<string, unknown> = { ...(raw as Record<string, unknown>), session_id: await $.session.id() };
      const revision = request.governanceRevision ?? 0;
      if (typeof revision !== 'number' || !Number.isInteger(revision) || revision < 0) throw new Error('Invalid revision');
      if (action !== 'evaluate') {
        // Only allowlisted metadata is echoed. Raw inputs may contain secrets.
        const safe = action === 'model-policy'
          ? JSON.stringify({ policy: payload.policy, scope: payload.scope, expires_at: payload.expires_at, session_id: payload.session_id })
            .replace(/((?:password|secret|token|api[_-]?key|authorization)\s*["']?\s*[:=]\s*["']?)[^\s",}]+/gi, '$1[redacted]')
          : 'Persist the evaluated routing decision metadata';
        const answer = await $.ui.ask(`ORE MODEL ROUTER: ${action}\n${safe}\nTask: ${task.id}; governance revision: ${revision}. This authorizes metadata persistence only; model selection remains manual.`, ['Cancel', 'Confirm durable change']);
        if (answer !== 'Confirm durable change') return { text: 'Cancelled; no state written' };
        const current = await load($);
        if (!current || current.id !== task.id || current.revision !== task.revision) throw new Error('State changed during confirmation');
      }
      const root = await $.session.cwd();
      const argv = [python, `${$.plugin.root}/scripts/ore_state.py`, 'runtime', '--repo', root,
        '--task-id', task.id, '--expect-revision', String(task.revision), '--mod', 'ore-model-router',
        '--action', String(action), '--payload', JSON.stringify(payload)];
      if (action !== 'evaluate') argv.push('--confirmed', '--expect-governance-revision', String(revision));
      const result = await $.process.run(argv, { cwd: root, timeoutMs: 30000 });
      if (result.exitCode || result.isStdoutTruncated) throw new Error('Router validation failed; inspect input locally');
      return { text: JSON.stringify({ routing: JSON.parse(result.stdout), effectiveModel: await $.session.model(),
        reportedUsage: await $.session.usage(), modelChanged: false }, null, 2) };
    } catch { return { text: 'ORE routing blocked: invalid input, changed state or unavailable runtime', exitCode: 2 }; }
  }).catch(() => ({ text: 'ORE router host unavailable', exitCode: 2 }));
};
