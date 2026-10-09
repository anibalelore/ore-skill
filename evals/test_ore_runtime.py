import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import shutil

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/ore/scripts'
sys.path.insert(0, str(SCRIPTS))
from ore_runtime import (apply_governance, check_paths, initial_governance,
                         learning_comparison, smart_tests, autopilot, validate_governance)

NOW = '2026-10-08T12:00:00+00:00'


class RuntimeContracts(unittest.TestCase):
    def rule(self, data=None, **changes):
        payload = dict(id='scope', owner='project owner', evidence='explicit approval', description='Only source files', paths=['src/*'])
        payload.update(changes)
        return apply_governance(data or initial_governance('project'), 'scope', payload, 'project', NOW, True)

    def test_confirmation_and_project_isolation(self):
        with self.assertRaises(ValueError):
            apply_governance(initial_governance('project'), 'scope', {}, 'project', NOW, False)
        with self.assertRaises(ValueError):
            validate_governance(self.rule(), 'other-project')

    def test_scope_exception_expiry_and_replacement(self):
        data = self.rule(exceptions_allowed=True)
        self.assertTrue(check_paths(data, ['src/app.py'], NOW)['allowed'])
        self.assertFalse(check_paths(data, ['README.md'], NOW)['allowed'])
        exception = dict(id='docs-once', owner='owner', evidence='reviewed need', rule_id='scope', path='README.md', expires_at='2026-10-09T00:00:00+00:00')
        data = apply_governance(data, 'exception', exception, 'project', NOW, True)
        self.assertTrue(check_paths(data, ['README.md'], NOW)['allowed'])
        self.assertFalse(check_paths(data, ['README.md'], '2026-10-10T00:00:00+00:00')['allowed'])
        data = self.rule(data, id='new-scope', replaces='scope', paths=['docs/*'])
        self.assertEqual(data['rules'][0]['status'], 'replaced')
        self.assertTrue(check_paths(data, ['docs/guide.md'], NOW)['allowed'])
        self.assertEqual(data['events'][-1]['origin'], 'ore_state.py')

    def test_traversal_and_corrupt_nested_state(self):
        for path in ['../outside', 'C:relative', '//server/share', '.ore/tasks/a.json', './.ore/tasks/a.json']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.rule(paths=[path])
        data = self.rule()
        data['rules'][0]['paths'] = [42]
        with self.assertRaises(ValueError):
            validate_governance(data, 'project')

    def test_budget_and_unknown_test_coverage(self):
        task = {'blockers': []}
        self.assertEqual(autopilot(task, {'steps': ['inspect'], 'attempts': 5})['state'], 'budget-exhausted')
        with self.assertRaises(ValueError):
            autopilot(task, {'steps': ['inspect'] * 6})
        result = smart_tests({'changed_paths': ['src/a.py'], 'mappings': [], 'broad_tests': ['full-suite']})
        self.assertEqual(result['selected'], ['full-suite'])
        self.assertTrue(result['broad_required'])
        self.assertFalse(result['executed'])
        self.assertTrue(smart_tests({'changed_paths': ['src/a.py'], 'mappings': [{'paths': ['src/*'], 'tests': ['unit']}], 'coverage_complete': False})['blocked'])

    def test_efficiency_requires_same_gates_and_complete_counters(self):
        baseline = dict(task='fixture', artifact='immutable-fixture', environment='isolated-test', model='same', settings={}, acceptance=['same'], gates=['TESTS'], counter_source='measured-host', includes_retries=True, includes_subagents=True, passed=True, tokens=100)
        candidate = dict(baseline, tokens=80)
        self.assertEqual(learning_comparison({'baseline': baseline, 'candidate': candidate})['tokens_saved'], 20)
        candidate['gates'] = []
        self.assertFalse(learning_comparison({'baseline': baseline, 'candidate': candidate})['demonstrated'])
        baseline['counter_source'] = candidate['counter_source'] = 'estimated'
        self.assertFalse(learning_comparison({'baseline': baseline, 'candidate': candidate})['demonstrated'])
        baseline['includes_subagents'] = candidate['includes_subagents'] = False
        self.assertFalse(learning_comparison({'baseline': baseline, 'candidate': candidate})['demonstrated'])

    def test_sole_writer_revision_conflict_and_symlink_scope(self):
        with tempfile.TemporaryDirectory() as directory:
            script = str(SCRIPTS / 'ore_state.py')
            def invoke(*args):
                return subprocess.run([sys.executable, script, *args, '--repo', directory], capture_output=True, text=True)
            started = invoke('start', '--title', 'Runtime', '--objective', 'Verify', '--kind', 'general', '--task-id', 'runtime', '--acceptance', 'Safe', '--deliverable', 'Build:100')
            self.assertEqual(started.returncode, 0, started.stderr)
            revision = json.loads(started.stdout)['revision']
            common = ['runtime', '--task-id', 'runtime', '--expect-revision', str(revision), '--mod', 'ore-scope-lock']
            payload = json.dumps(dict(id='scope', owner='owner', evidence='confirmation', description='Source only', paths=['src/*']))
            denied = invoke(*common, '--action', 'scope', '--payload', payload)
            self.assertNotEqual(denied.returncode, 0)
            self.assertFalse((Path(directory) / '.ore/governance.json').exists())
            created = invoke(*common, '--action', 'scope', '--payload', payload, '--confirmed')
            self.assertEqual(created.returncode, 0, created.stderr)
            stale = invoke(*common, '--action', 'scope', '--payload', payload, '--confirmed')
            self.assertIn('revision conflict', stale.stderr.lower())
            checked = invoke(*common, '--payload', json.dumps({'paths': ['../outside']}))
            self.assertFalse(json.loads(checked.stdout)['runtime_result']['allowed'])


@unittest.skipUnless(shutil.which('node'), 'Node 24 required for native TypeScript handlers')
class NativeRuntimeAdapters(unittest.TestCase):
    def run_handler(self, **data):
        task = dict(schema_version=1, id='fixture', title='Fixture', objective='Safe operation', status='active', revision=1,
                    deliverables=[dict(name='Build', weight=100, completion=0, status='pending', evidence=[])], gates={}, roles={}, blockers=[], events=[])
        data.setdefault('task', task)
        result = subprocess.run(['node', str(SCRIPTS.parents[2] / 'evals/runtime_mods_harness.mjs')], input=json.dumps(data), capture_output=True, text=True, cwd=SCRIPTS.parents[2])
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_absent_state_is_inert(self):
        result = self.run_handler(mod='ore-flow-intelligence', missing=True)
        self.assertEqual(result['processes'], 0)

    def test_durable_rule_requires_ui_confirmation(self):
        result = self.run_handler(mod='ore-never-again', request={'action': 'rule', 'payload': {}}, answer='Cancel')
        self.assertEqual(result['asks'], 1)
        self.assertEqual(result['processes'], 0)

    def test_scope_denial_corrupt_state_and_runtime_failure(self):
        governance = initial_governance('project')
        governance = apply_governance(governance, 'scope', dict(id='scope', owner='owner', evidence='approved', description='Source only', paths=['src/*']), 'project', NOW, True)
        denied = self.run_handler(mod='ore-scope-lock', tool='Write', governance=governance, result={'runtime_result': {'allowed': False, 'violations': ['scope']}})
        self.assertIn('deny', denied['result'])
        corrupt = self.run_handler(mod='ore-scope-lock', tool='Edit', corruptGovernance=True)
        self.assertEqual(corrupt['passed'], 1)
        unavailable = self.run_handler(mod='ore-scope-lock', tool='Write', governance=governance, runtimeUnavailable=True)
        self.assertIn('deny', unavailable['result'])

    def test_usage_uses_native_counter_without_process(self):
        result = self.run_handler(mod='ore-cost-controller')
        self.assertEqual(result['processes'], 0)
        self.assertIn('usage', json.loads(result['result']['text']))


if __name__ == '__main__':
    unittest.main()
