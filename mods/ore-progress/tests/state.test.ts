import { expect, test } from 'claude-code/testing';
import { pointer, parseTask, department, pendingGates } from '../hooks/state.ts';
const task = { schema_version: 1, id: 'fixture', title: 'Fixture', objective: 'Verify', status: 'active', revision: 1, deliverables: [{name:'Build',weight:100,completion:0,status:'pending'}], gates: { TESTS: {required:true,status:'pending'} }, blockers: [] };
test('corrupt and unsafe state is ignored', () => {
  expect(pointer('{')).toBe(null);
  expect(pointer('{"schema_version":1,"task_id":"../outside"}')).toBe(null);
  expect(parseTask('{','fixture')).toBe(null);
});
test('old state preserves gates and falls back to ORE lead', () => {
  const parsed = parseTask(JSON.stringify(task), 'fixture')!;
  expect(department(parsed)).toBe('ORE lead');
  expect(pendingGates(parsed)).toEqual(['TESTS: pending']);
});
