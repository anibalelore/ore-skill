"""Cross-host writer tests and real TypeScript reader/handler regression tests."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / 'evals/mods_harness.mjs'
FIXTURE = dict(schema_version=1, id='fixture', title='Fixture', objective='Verify ORE', status='active', revision=1,
               progress=99, deliverables=[dict(name='Build', weight=50, completion=1, status='in_progress'), dict(name='Verify', weight=50, completion=0, status='pending')],
               gates={'TESTS': dict(required=True, status='pending')}, blockers=[], events=[])
MODS = ['progress', 'guard', 'resume', 'gates', 'stale-window', 'departments']


class ModsStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which('node'):
            raise RuntimeError('Node.js 24+ is required to test the TypeScript mods')

    def run_mod(self, **data):
        data.setdefault('task', copy.deepcopy(FIXTURE))
        result = subprocess.run(['node', str(HARNESS)], input=json.dumps(data), capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_absent_and_corrupt_are_inert_for_every_mod(self):
        for name in MODS:
            for args in ({'missing': True}, {'pointer': '{'}, {'task': '{'}):
                with self.subTest(mod=name, args=args):
                    result = self.run_mod(mod=f'ore-{name}', tool='rm -rf cache' if name == 'guard' else None, **args)
                    self.assertEqual(result['logs'], [])
                    if name == 'guard':
                        self.assertEqual(result['asks'], 0)
                    elif result['drawing']:
                        self.assertEqual(result['drawing']['type'], 'Base')

    def test_pointer_rejects_traversal_and_schema(self):
        for pointer in ('{}', 'null', '{"schema_version":1,"task_id":"../secret"}', '{"schema_version":2,"task_id":"fixture"}'):
            self.assertIsNone(self.run_mod(mode='projection', pointer=pointer))

    def test_progress_uses_python_ties_to_even(self):
        result = self.run_mod(mode='projection')
        self.assertEqual(result['task']['progress'], 0)
        self.assertEqual(result['next'], 'Build')
        task = copy.deepcopy(FIXTURE)
        task['deliverables'][0]['completion'] = 3
        self.assertEqual(self.run_mod(mode='projection', task=task)['task']['progress'], 2)

    def test_complete_and_blockers(self):
        task = copy.deepcopy(FIXTURE)
        task.update(status='complete')
        for d in task['deliverables']:
            d.update(completion=100, status='done')
        task['gates']['TESTS']['status'] = 'passed'
        result = self.run_mod(mode='projection', task=task)
        self.assertEqual(result['task']['progress'], 100)
        self.assertEqual(result['next'], 'None remaining')
        self.assertEqual(result['gates'], [])
        self.assertEqual(self.run_mod(mod='ore-resume', task=task)['logs'], [])
        task.update(status='blocked', blockers=['Missing approval'])
        result = self.run_mod(mod='ore-gates', task=task, endTurn=True)
        self.assertIn('Missing approval', result['logs'][0])

    def test_revision_changes_update_display_and_warn(self):
        changed = copy.deepcopy(FIXTURE)
        changed.update(revision=2, title='Updated')
        self.assertTrue(self.run_mod(mode='projection', task=changed, previous=FIXTURE)['changed'])
        result = self.run_mod(mod='ore-stale-window', updated=changed)
        self.assertIn('r1', result['logs'][0])
        self.assertIn('r2', result['logs'][0])
        self.assertIn('Updated', json.dumps(self.run_mod(mod='ore-progress', updated=changed)['drawing']))

    def test_specialist_change_and_old_state(self):
        self.assertEqual(self.run_mod(mode='projection')['department'], 'ORE lead')
        task = copy.deepcopy(FIXTURE)
        task.update(revision=2, active_specialist=dict(specialist='ore-security-privacy', department='Security & Governance', domain_lead='Security lead', revision=2))
        task['events'] = [dict(kind='specialist_changed', specialist='ore-security-privacy', revision=2)]
        result = self.run_mod(mod='ore-departments', updated=task)
        self.assertIn('Security & Governance', json.dumps(result['drawing']))
        self.assertIn('ore-security-privacy', self.run_mod(mode='projection', task=task)['department'])

    def test_guard_requires_explicit_action_approval(self):
        commands = ['rm -rf cache', 'psql -c "DROP TABLE orders"', 'prisma migrate reset', 'git push origin main --force', 'git push origin main -f', 'vercel deploy --prod', 'rotate credential token', 'npm publish', 'npm\npublish']
        for command in commands:
            with self.subTest(command=command):
                denied = self.run_mod(mod='ore-guard', tool=command)
                self.assertEqual(denied['asks'], 1)
                self.assertIn('deny', denied['result'])
                allowed = self.run_mod(mod='ore-guard', tool=command, answer='Proceed once')
                self.assertEqual(allowed['passed'], 1)
        self.assertEqual(self.run_mod(mod='ore-guard', tool='git status')['asks'], 0)
        for args in ({'dismiss': True}, {'aborted': True}, {'changeDuringAsk': True}):
            self.assertIn('deny', self.run_mod(mod='ore-guard', tool='npm publish', answer='Proceed once', **args)['result'])

    def test_guard_configurable_patterns(self):
        self.assertEqual(self.run_mod(mod='ore-guard', tool='release-live', options={'patterns': '["release-live"]'})['asks'], 1)
        self.assertEqual(self.run_mod(mod='ore-guard', tool='git status', options={'patterns': '['})['asks'], 1)

    def test_specialist_writer_is_optional_revision_protected(self):
        script = ROOT / 'skills/ore/scripts/ore_state.py'
        with tempfile.TemporaryDirectory() as repo:
            def cli(*args):
                return subprocess.run([sys.executable, str(script), *args, '--repo', repo], capture_output=True, text=True)
            started = cli('start', '--title', 'Identity', '--objective', 'Verify routing', '--kind', 'general', '--acceptance', 'Routing persists', '--deliverable', 'Build:100')
            self.assertEqual(started.returncode, 0, started.stderr)
            task_id = json.loads(started.stdout)['task_id']
            args = ('update', '--task-id', task_id, '--expect-revision', '1', '--active-specialist', 'ore-security-privacy', '--department', 'Security & Governance', '--domain-lead', 'Security lead')
            self.assertEqual(cli(*args).returncode, 0)
            task = json.loads((Path(repo) / '.ore/tasks' / f'{task_id}.json').read_text())
            self.assertEqual(task['active_specialist']['revision'], 2)
            self.assertEqual(task['events'][-1]['kind'], 'specialist_changed')
            self.assertNotEqual(cli(*args).returncode, 0)
            invalid = cli('update', '--task-id', task_id, '--expect-revision', '2', '--active-specialist', 'ore-backend-data')
            self.assertNotEqual(invalid.returncode, 0)
            self.assertEqual(json.loads((Path(repo) / '.ore/tasks' / f'{task_id}.json').read_text())['revision'], 2)
