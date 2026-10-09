"""Synthetic governance evaluations, never claimed as provider benchmarks."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/ore/scripts'))
from ore_models import analyze, config, operation, policy, registry, route, mutate, effective_policy, inspect_host
from ore_runtime import initial_governance, apply_governance, validate_governance

NOW = '2026-10-09T12:00:00+00:00'
EXPIRY = '2026-10-10T12:00:00+00:00'
CURRENT = dict(provider='test-provider', model_id='advanced-fixture', effort='high')
CANDIDATE = dict(provider='test-provider', model_id='economy-fixture', effort='medium')
TASK = {'id': 'test-task'}


def request():
    def row(name, price, level):
        return dict(provider='test-provider', model_id=name, available=True, restricted=False,
                    max_complexity=level, tools=['read'], efforts=['medium', 'high'],
                    selection_scope=dict(main_session='manual', subagent='documented', between_tasks='manual'),
                    verified_at=NOW, expires_at=EXPIRY, input_per_million=price, output_per_million=price, cost_source='synthetic-fixture')
    return dict(source='explicit-user-or-host', current=CURRENT, session_id='session-a',
                registry=dict(schema_version=1, host='codex', source='operator-verified', models=[row('advanced-fixture', 10, 4), row('economy-fixture', 1, 2)]),
                task_profile=dict(**{k: 2 for k in ('complexity', 'scope', 'dependencies', 'reasoning', 'risk', 'context', 'tools', 'verification', 'uncertainty', 'cost')},
                                  required_tools=['read'], acceptance=['correct'], gates=['TESTS']),
                estimated_tokens={'input': 1000, 'output': 1000}, overheads=dict(validation=.001, delegation=0, recovery=0, retry_multiplier=1))


class ModelContracts(unittest.TestCase):
    def evaluate(self, value=None, data=None):
        return route(value or request(), TASK, data or initial_governance('project'), 'project', NOW)

    def approve(self, scope='task:test-task', expiry=EXPIRY):
        return apply_governance(initial_governance('project'), 'approval', dict(id='route-a', owner='owner', evidence='explicit decision',
            operation=operation(CANDIDATE), scope=scope, environment='codex:main_session', expires_at=expiry), 'project', NOW, True)

    def settings(self, value, scope='project', data=None):
        return mutate(data or initial_governance('project'), 'model-policy', dict(scope=scope, session_id='session-a', policy=value, expires_at=EXPIRY), 'project', NOW, TASK)

    def test_available_and_quality_preserved(self):
        r = self.evaluate()
        self.assertEqual(r['recommended'], CANDIDATE)
        self.assertEqual(r['approval_status'], 'awaiting-approval')
        self.assertEqual(r['gates'], ['TESTS'])
        self.assertEqual(r['estimated_total_cost'], .005)
        self.assertFalse(r['model_changed'])
        self.assertIsNone(r['effective'])
        self.assertIsNone(r['savings'])

    def test_registry_availability_restrictions_and_scope(self):
        for change in ({'available': False}, {'restricted': True}, {'selection_scope': dict(main_session='unsupported', subagent='unsupported', between_tasks='unsupported')}, {'tools': []}, {'efforts': ['low']}):
            p = request()
            p['registry']['models'][1].update(change)
            self.assertNotEqual(self.evaluate(p)['recommended'], CANDIDATE)
        p = request()
        p['registry']['host'] = 'unknown'
        with self.assertRaises(ValueError): self.evaluate(p)
        p = request()
        p['registry']['models'][0]['expires_at'] = NOW
        with self.assertRaises(ValueError): self.evaluate(p)

    def test_nonexistent_configuration_never_selected(self):
        d = self.settings({'locks': {'model_id': 'nonexistent'}})
        self.assertEqual(self.evaluate(data=d)['approval_status'], 'blocked')

    def test_task_session_and_project_authority(self):
        for scope in ('task:test-task', 'session:session-a', 'project'):
            self.assertEqual(self.evaluate(data=self.approve(scope))['approval_status'], 'authorized')
        for scope in ('task:other-task', 'session:other-session'):
            self.assertEqual(self.evaluate(data=self.approve(scope))['approval_status'], 'awaiting-approval')
        p = request(); p['selection_scope'] = 'between_tasks'
        self.assertEqual(self.evaluate(p, self.approve())['approval_status'], 'awaiting-approval')

    def test_expiry_revocation_and_manual(self):
        d = self.approve()
        d['approvals'][0]['expires_at'] = NOW
        self.assertEqual(self.evaluate(data=d)['approval_status'], 'awaiting-approval')
        d = apply_governance(self.approve(), 'revoke-approval', dict(id='route-a', owner='owner', evidence='revoked'), 'project', NOW, True)
        self.assertEqual(self.evaluate(data=d)['approval_status'], 'awaiting-approval')
        d = self.settings({'mode': 'MANUAL'}, data=self.approve())
        self.assertEqual(self.evaluate(data=d)['approval_status'], 'manual')

    def test_auto_profile_does_not_grant_authority(self):
        self.assertEqual(self.evaluate(data=self.settings({'mode': 'AUTHORIZED_AUTO'}))['approval_status'], 'awaiting-approval')

    def test_locks_cover_delegation(self):
        d = self.settings({'locks': CURRENT, 'max_subagents': 2})
        p = request(); p.update(selection_scope='subagent', subagents_used=0)
        self.assertEqual(self.evaluate(p, d)['recommended'], CURRENT)
        d = self.settings({'locks': {'provider': 'other'}})
        self.assertIsNone(self.evaluate(data=d)['recommended'])

    def test_effort_and_budget_limits(self):
        for rules in ({'max_effort': 'low'}, {'budget': .001}):
            self.assertEqual(self.evaluate(data=self.settings(rules))['approval_status'], 'blocked')
        p = request(); p.pop('overheads')
        self.assertIsNone(self.evaluate(p)['estimated_total_cost'])
        self.assertIsNone(self.evaluate(p, self.settings({'budget': 1}))['recommended'])

    def test_preferences_and_restrictions_precedence(self):
        d = self.settings({'excluded_models': ['economy-fixture'], 'max_retries': 1})
        d = self.settings({'max_retries': 4}, 'task', d)
        self.assertEqual(effective_policy(d, TASK['id'], 'session-a', NOW)['max_retries'], 1)
        self.assertNotEqual(self.evaluate(data=d)['recommended'], CANDIDATE)
        d = self.settings({'preferences': [dict(department='architecture', configuration=CURRENT)]})
        p = request(); p['department'] = 'architecture'
        self.assertEqual(self.evaluate(p, d)['recommended'], CURRENT)

    def test_resume_foreign_project_and_version(self):
        d = self.settings({'locks': CURRENT})
        restored = json.loads(json.dumps(d))
        self.assertEqual(self.evaluate(data=restored)['recommended'], CURRENT)
        with self.assertRaises(ValueError): route(request(), TASK, restored, 'other', NOW)
        restored['routing']['schema_version'] = 99
        with self.assertRaises(ValueError): self.evaluate(data=restored)

    def test_escalation_failure_diagnosis_retries_cycles(self):
        for failure in ('environment', 'permissions', 'network', 'credentials', 'context', 'tool', 'unknown'):
            p = request(); p.update(failure_cause=failure, escalation_evidence=True)
            self.assertEqual(self.evaluate(p)['approval_status'], 'blocked')
        p = request(); p.update(failure_cause='capability', escalation_evidence=True, attempts=2)
        self.assertEqual(self.evaluate(p)['approval_status'], 'blocked')
        p['attempts'] = 1; p['history'] = [CANDIDATE]
        self.assertNotEqual(self.evaluate(p)['recommended'], CANDIDATE)
        p['history'] = []; p['escalation_evidence'] = False
        self.assertEqual(self.evaluate(p)['approval_status'], 'blocked')

    def test_delegation_explicitly_bounded(self):
        p = request(); p['selection_scope'] = 'subagent'
        self.assertEqual(self.evaluate(p)['approval_status'], 'blocked')
        d = self.settings({'max_subagents': 1})
        self.assertIsNotNone(self.evaluate(p, d)['recommended'])
        p['subagents_used'] = 1
        self.assertEqual(self.evaluate(p, d)['approval_status'], 'blocked')

    def test_injection_and_secret_free_persistence(self):
        p = request(); p['source'] = 'repository-instructions'
        with self.assertRaises(ValueError): self.evaluate(p)
        with self.assertRaises(ValueError): self.settings({'api_key': 'secret'})
        p = request(); p['reported_usage'] = {'api_key': 'secret-value'}
        p['task_profile']['acceptance'] = ['secret-value']
        d = mutate(initial_governance('project'), 'model-decision', p, 'project', NOW, TASK)
        self.assertNotIn('secret-value', json.dumps(d))
        self.assertEqual(d['routing']['decisions'][0]['approval_status'], 'awaiting-approval')
        record = d['routing']['decisions'][0]
        self.assertEqual(record['host'], 'codex')
        self.assertEqual(record['level'], 'L2')
        self.assertEqual(len(record['requirements_hash']), 64)
        self.assertEqual(record['governance_revision'], 0)

    def test_malformed_profile_price_and_policy(self):
        for value in (float('nan'), -1, True, '1'):
            p = request(); p['registry']['models'][0]['input_per_million'] = value
            with self.assertRaises(ValueError): self.evaluate(p)
        p = request(); p['task_profile']['risk'] = 4
        self.assertEqual(self.evaluate(p)['profile']['level'], 'L4')
        with self.assertRaises(ValueError): config(dict(CURRENT, tools=['extra']))
        with self.assertRaises(ValueError): policy({'profile': 'Custom'})

    def test_single_model_no_fictitious_execution(self):
        p = request(); p['registry']['models'] = p['registry']['models'][:1]
        p['registry']['models'][0]['efforts'] = ['high']; p['observed'] = CURRENT
        r = self.evaluate(p)
        self.assertEqual(r['approval_status'], 'keep-current')
        self.assertEqual(r['effective'], CURRENT)

    def test_authoritative_gates_and_risk_cannot_be_replaced(self):
        p = request()
        p['task_profile'].update(**{k: 0 for k in analyze(p['task_profile'])['dimensions']}, acceptance=['unrelated'], gates=[])
        t = dict(TASK, risk='L5', acceptance_criteria=['Security review'], gates={'SECURITY': {'required': True, 'status': 'failed'}})
        r = route(p, t, initial_governance('project'), 'project', NOW)
        self.assertEqual(r['profile']['level'], 'L4')
        self.assertIn('Security review', r['profile']['acceptance'])
        self.assertIn('SECURITY', r['gates'])
        self.assertEqual(r['quality_status'], 'failed')
        self.assertEqual(r['recommended']['model_id'], 'advanced-fixture')
        t['gates']['SECURITY']['status'] = 'passed'
        self.assertEqual(route(p, t, initial_governance('project'), 'project', NOW)['quality_status'], 'passed-gates')

    def test_corrupt_policy_and_delegation_usage(self):
        d = initial_governance('project')
        d['routing'] = dict(schema_version=1, policies=[None], decisions=[])
        with self.assertRaises(ValueError): validate_governance(d, 'project')
        for value in (-1, '1', True):
            p = request(); p['subagents_used'] = value
            with self.assertRaises(ValueError): self.evaluate(p)

    def test_writer_confirmation_revision_and_readonly(self):
        with tempfile.TemporaryDirectory() as directory:
            def run(*args):
                return subprocess.run([sys.executable, str(ROOT / 'skills/ore/scripts/ore_state.py'), *args, '--repo', directory], capture_output=True, text=True)
            started = run('start', '--task-id', 'test-task', '--title', 'Router', '--objective', 'Verify', '--kind', 'general', '--acceptance', 'Correct', '--deliverable', 'Build:100')
            self.assertEqual(started.returncode, 0, started.stderr)
            revision = json.loads(started.stdout)['revision']
            common = ['runtime', '--task-id', 'test-task', '--expect-revision', str(revision), '--mod', 'ore-model-router']
            evaluated = run(*common, '--payload', json.dumps(request()))
            self.assertEqual(evaluated.returncode, 0, evaluated.stderr)
            target = Path(directory) / '.ore/governance.json'
            self.assertFalse(target.exists())
            payload = json.dumps(dict(scope='project', policy={'mode': 'MANUAL'}, expires_at='2099-10-10T12:00:00+00:00'))
            denied = run(*common, '--action', 'model-policy', '--payload', payload)
            self.assertNotEqual(denied.returncode, 0)
            saved = run(*common, '--action', 'model-policy', '--payload', payload, '--confirmed')
            self.assertEqual(saved.returncode, 0, saved.stderr)
            stale = run(*common, '--action', 'model-policy', '--payload', payload, '--confirmed')
            self.assertIn('revision conflict', stale.stderr.lower())
            self.assertEqual(json.loads(target.read_text())['revision'], 1)

    def test_host_adapters_read_allowlist_without_account_claims(self):
        with tempfile.TemporaryDirectory() as directory:
            for host, filename, content in [('codex', 'config.toml', 'model="fixture"\nmodel_reasoning_effort="high"\napi_key="private-value"'),
                                             ('claude-code', 'settings.json', '{"model":"fixture","effortLevel":"high","api_key":"private-value"}')]:
                path = Path(directory) / filename
                path.write_text(content)
                result = inspect_host(host, path)
                self.assertEqual(result['requested']['model_id'], 'fixture')
                self.assertNotIn('private-value', json.dumps(result))
                self.assertEqual(result['registry']['models'], [])
                self.assertIsNone(result['effective'])
            self.assertEqual(inspect_host('chatgpt')['execution'], 'manual-host-selection-required')
            with self.assertRaises(ValueError): inspect_host('gemini')

    def test_benchmark_categories_and_strategies_preserve_acceptance(self):
        sys.path.insert(0, str(ROOT / 'evals'))
        from model_routing_benchmark import compare
        result = compare()
        self.assertEqual(result['scenarios'], 30)
        self.assertEqual(result['provider_calls'], 0)
        self.assertIsNone(result['savings'])


@unittest.skipUnless(__import__('shutil').which('node'), 'Node required for native handler contract tests')
class RouterHandlerContracts(unittest.TestCase):
    def invoke(self, request=None, **changes):
        task = dict(schema_version=1, id='fixture', title='Fixture', objective='Safe operation', status='active', revision=1,
                    deliverables=[dict(name='Build', weight=100, completion=0, status='pending', evidence=[])], gates={}, roles={}, blockers=[], events=[])
        value = dict(mod='ore-model-router', task=task, request=request or {})
        value.update(changes)
        result = subprocess.run(['node', str(ROOT / 'evals/runtime_mods_harness.mjs')], input=json.dumps(value), capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_readonly_observations_and_no_model_change(self):
        result = self.invoke()
        self.assertEqual(result['asks'], 0)
        data = json.loads(result['result']['text'])
        self.assertEqual(data['effectiveModel'], 'observed-model')
        self.assertFalse(data['modelChanged'])

    def test_confirmation_cancel_and_failure(self):
        value = dict(action='model-policy', payload=dict(scope='project', policy={}, expires_at=EXPIRY))
        denied = self.invoke(value)
        self.assertEqual(denied['asks'], 1)
        self.assertEqual(denied['processes'], 0)
        approved = self.invoke(value, answer='Confirm durable change')
        self.assertEqual(approved['processes'], 1)
        self.assertEqual(approved['lastPayload']['session_id'], 'observed-session')
        self.assertIn('project', approved['lastQuestion'])
        self.assertIn(EXPIRY, approved['lastQuestion'])
        failed = self.invoke(value, answer='Confirm durable change', runtimeUnavailable=True)
        self.assertEqual(failed['result']['exitCode'], 2)
        self.assertNotIn('private', failed['result']['text'])


if __name__ == '__main__': unittest.main()
