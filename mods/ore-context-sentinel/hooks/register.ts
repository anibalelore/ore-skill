import type { EngineInterface, Register } from 'claude-code';
import { pointer, parseTask, handoff } from './state.ts';
import type { Task } from './state.ts';
import { NAME } from './identity.ts';

async function load($: EngineInterface): Promise<Task | null> {
  try {
    const root = await $.session.cwd();
    const id = pointer(await $.fs.read(`${root}/.ore/active.json`));
    if (!id) return null;
    const task = parseTask(await $.fs.read(`${root}/.ore/tasks/${id}.json`), id);
    return pointer(await $.fs.read(`${root}/.ore/active.json`)) === id ? task : null;
  } catch { return null; }
}

// These adapters need no process permission or bundled Python runtime.
export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: NAME, description: 'Read native context/cost or observed project manifest presence' });
    await $.command.register({ name: `${NAME}-status`, description: 'Read persisted ORE handoff' });
    return next(e);
  });
  on('command.run', { command: `${NAME}-status` }, async ($) => {
    const task = await load($);
    return { text: task ? handoff(task) : 'No valid ORE state' };
  });
  on('command.run', { command: NAME }, async ($) => {
    const task = await load($);
    if (!task || task.status === 'complete') return { text: 'No active valid ORE state' };
    if (NAME !== 'ore-project-router') {
      return { text: JSON.stringify({ handoff: handoff(task), usage: await $.session.usage(), modelChanged: false, compactionVeto: false }, null, 2) };
    }
    const root = await $.session.cwd();
    const found: string[] = [];
    for (const file of ['package.json', 'pyproject.toml', 'Cargo.toml', 'go.mod', 'pom.xml', 'build.gradle', 'pubspec.yaml']) {
      try { await $.fs.read(`${root}/${file}`); found.push(file); } catch { /* Absence is not evidence. */ }
    }
    return { text: JSON.stringify({ observedManifests: found, status: found.length ? 'evidence-found' : 'unknown', specialistChanged: false }) };
  }).catch(() => ({ text: 'Native counters or project reads unavailable', exitCode: 2 }));
};
