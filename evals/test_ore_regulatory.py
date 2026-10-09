import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/ore/scripts'))
import ore_regulatory as r

NOW = '2026-10-09T12:00:00+00:00'


class RegulatoryTests(unittest.TestCase):
    def setUp(self):
        self.record = {'id': 'batch-1', 'version': 1, 'content': {'result': 'accepted'}, 'meaning': 'release'}
        self.identity = {'id': 'alice', 'name': 'Alice Example', 'verified': True, 'enabled': True,
                         'allowed_records': ['batch-1']}
        self.auth = {'subject': 'alice', 'at': NOW, 'expires_at': '2026-10-09T12:05:00+00:00',
                     'mode': 'non-biometric', 'components': ['id', 'password-component'],
                     'owner_only': True, 'two_person_admin': True, 'evidence_ref': 'auth-event-1'}

    def sign(self, ledger=None, request='request-1'):
        return r.sign(self.record, self.identity, self.auth, ledger or [], request, NOW)

    def test_legitimate_export_and_module_continuity(self):
        ledger, signature = self.sign()
        exported = json.loads(json.dumps({'record': self.record, 'signature': signature}))
        self.assertTrue(r.verify_signature(**exported))
        self.assertTrue(r.transition('fda', self.record, copy.deepcopy(self.record), signature))
        self.assertFalse(r.transition('fda', self.record, self.record))
        self.assertEqual(len(ledger), 1)

    def test_unauthorized_disabled_and_subject_mismatch(self):
        for key, value in [('allowed_records', []), ('enabled', False), ('verified', False)]:
            with self.subTest(key=key):
                identity = dict(self.identity, **{key: value})
                with self.assertRaises(ValueError):
                    r.sign(self.record, identity, self.auth, [], 'a', NOW)
        with self.assertRaises(ValueError):
            r.sign(self.record, self.identity, dict(self.auth, subject='bob'), [], 'a', NOW)

    def test_reuse_altered_versions_and_retry(self):
        ledger, signature = self.sign()
        retried, same = self.sign(ledger)
        self.assertEqual(ledger, retried)
        self.assertEqual(signature, same)
        for changed in [dict(self.record, version=2), dict(self.record, content={'result': 'rejected'})]:
            self.assertFalse(r.verify_signature(changed, signature))
            self.assertFalse(r.transition('fda', self.record, changed, signature))
            with self.assertRaises(ValueError):
                r.sign(changed, self.identity, self.auth, ledger, 'request-1', NOW)

    def test_incomplete_secrets_save_failure_and_recovery(self):
        for record in [dict(self.record, content=None), dict(self.record, password='forbidden')]:
            with self.assertRaises(ValueError):
                r.sign(record, self.identity, self.auth, [], 'a', NOW)
        ledger = []
        candidate, first = self.sign(ledger)
        # Simulate transaction failing before commit: original state remains unchanged.
        self.assertEqual(ledger, [])
        retried, second = self.sign(ledger)
        self.assertEqual(candidate, retried)
        self.assertEqual(first, second)

    def test_11200_sessions_reauthentication_and_biometrics(self):
        with self.assertRaises(ValueError):
            r.sign(self.record, self.identity, dict(self.auth, components=['id']), [], 'a', NOW)
        with self.assertRaises(ValueError):
            r.sign(self.record, self.identity, dict(self.auth, expires_at=NOW), [], 'a', NOW)
        self.auth['session_id'] = 'session-1'
        ledger, first = self.sign()
        self.auth.update(continuous_session=True, first_signing=False, components=['id'], session_initial_signature=first['id'])
        self.sign(ledger, 'request-2')
        with self.assertRaises(ValueError):
            self.sign([], 'request-2')
        biometric = dict(self.auth, mode='biometric', owner_only=False)
        with self.assertRaises(ValueError):
            r.sign(self.record, self.identity, biometric, [], 'a', NOW)

    def test_supersession_preserves_history(self):
        ledger, first = self.sign()
        ledger, second = self.sign(ledger, 'request-2')
        with self.assertRaises(ValueError):
            r.supersede(ledger, first['id'], second['id'], {}, 'revision', NOW)
        updated = r.supersede(ledger, first['id'], second['id'],
                             {'id': 'quality', 'enabled': True, 'can_supersede': True}, 'revision', NOW)
        self.assertEqual(ledger[0]['status'], 'active')
        self.assertEqual(updated[0]['status'], 'superseded')
        self.assertFalse(r.verify_signature(self.record, updated[0]))

    def test_ftc_authorized_unauthorized_tenants_and_integration_failure(self):
        before = {'tenant': 'a', 'privileges': ['read'], 'data_fields': ['id']}
        after = dict(before, authorized=True, protected=True)
        self.assertTrue(r.transition('ftc', before, after))
        for change in [{'tenant': 'b'}, {'authorized': False}, {'protected': False},
                       {'privileges': ['read', 'admin']}, {'data_fields': ['id', 'secret']}]:
            self.assertFalse(r.transition('ftc', before, dict(after, **change)))

    def test_incident_threshold_key_access_presumption_and_unknowns(self):
        event = {'consumers': 500, 'discovered_at': NOW, 'encrypted': False, 'unauthorized_access': True}
        result = r.incident_readiness(event)
        self.assertEqual(result['status'], 'potential_notification_event')
        self.assertEqual(result['deadline'], '2026-11-08T12:00:00+00:00')
        self.assertFalse(result['notification_submitted'])
        self.assertEqual(r.incident_readiness(dict(event, encrypted=True, key_compromised=True))['status'], result['status'])
        self.assertEqual(r.incident_readiness(dict(event, consumers=499))['status'], 'threshold_not_established')
        self.assertEqual(r.incident_readiness(dict(event, consumers=None))['status'], 'review_required')
        self.assertEqual(r.incident_readiness(dict(event, reliable_no_acquisition_evidence='forensic-report'))['status'], 'threshold_not_established')


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        names = r.FDA_TESTS | r.FTC_TESTS | r.FDA_RECORDS | r.FTC_CONTROLS
        artifact = {'schema_version': 1, 'checks': {name: {'result': 'passed', 'validation': 'synthetic fixture',
                    'subject': 'isolated fixture', 'owner': 'tester', 'at': NOW} for name in names}}
        (self.root / 'proof.txt').write_text(json.dumps(artifact), encoding='utf-8')
        self.proof = {'path': 'proof.txt', 'sha256': hashlib.sha256((self.root / 'proof.txt').read_bytes()).hexdigest(),
                      'owner': 'reviewer', 'validation': 'synthetic fixture', 'limitations': ['fixture only'], 'at': NOW}

    def tearDown(self):
        self.tmp.cleanup()

    def contract(self, domain):
        scope = {'status': 'applicable', 'owner': 'regulatory-owner', 'rationale': 'synthetic scope only',
                 'citations': ['11.1' if domain == 'fda' else '314.1'], 'evidence': [self.proof]}
        fields = ('activity', 'predicate_rules', 'electronic_records', 'exclusions', 'fda_enforcement_policy') if domain == 'fda' else (
            'activity', 'jurisdiction', 'financial_institution_analysis', 'entity_role', 'protected_data', 'providers', '314_6_analysis')
        scope.update({k: 'synthetic reviewed fixture' for k in fields})
        def entries(names):
            return {k: {'result': 'passed', 'owner': 'tester', 'evidence': [self.proof]} for k in names}
        document = {'schema_version': 1, 'domain': domain, 'risk': 'high',
                    'source': {'url': r.SOURCES[domain], 'version': 'eCFR 2026-10-07', 'checked_at': NOW},
                    'scope': scope, 'controls': entries(r.FDA_RECORDS if domain == 'fda' else r.FTC_CONTROLS),
                    'tests': entries(r.FDA_TESTS if domain == 'fda' else r.FTC_TESTS),
                    'documents': entries(r.DOCUMENTS[domain])}
        if domain == 'fda':
            fixture = RegulatoryTests()
            fixture.setUp()
            _, signature = fixture.sign()
            document['signed_records'] = [{'record': fixture.record, 'signature': signature}]
        return document

    def test_every_control_test_and_document_requires_proof(self):
        for domain in ('fda', 'ftc'):
            original = self.contract(domain)
            self.assertTrue(r.evaluate_document(original, self.root)['verified'])
            for collection in ('controls', 'tests', 'documents'):
                for identifier in original[collection]:
                    with self.subTest(domain=domain, collection=collection, identifier=identifier):
                        broken = copy.deepcopy(original)
                        broken[collection][identifier]['evidence'] = []
                        self.assertFalse(r.evaluate_document(broken, self.root)['verified'])

    def test_unknown_scope_na_exceptions_and_modified_evidence(self):
        doc = self.contract('ftc')
        doc['scope']['status'] = 'pending'
        self.assertEqual(r.evaluate_document(doc, self.root)['gates']['FTC_SAFEGUARDS_APPLICABILITY']['status'], 'blocked')
        doc['scope']['status'] = 'not_applicable'
        self.assertTrue(r.evaluate_document(doc, self.root)['verified'])
        doc['scope']['status'] = 'applicable'
        doc['controls']['mfa']['result'] = 'not_applicable'
        self.assertFalse(r.evaluate_document(doc, self.root)['verified'])
        doc['controls']['mfa']['exception'] = {'owner': 'QI', 'citation': '314.4(c)(5)', 'rationale': 'approved equivalent access fixture'}
        self.assertTrue(r.evaluate_document(doc, self.root)['verified'])
        (self.root / 'proof.txt').write_text('modified')
        with self.assertRaises(ValueError):
            r.evaluate_document(doc, self.root)

    def test_path_escape_and_false_document_claim(self):
        with self.assertRaises(ValueError):
            r.evidence(self.root, dict(self.proof, path='../outside'))
        doc = self.contract('fda')
        doc['documents']['training'] = {'result': 'passed', 'evidence': []}
        self.assertFalse(r.evaluate_document(doc, self.root)['verified'])

    def test_mandatory_scenario_cannot_be_waived_and_runtime_matches_domain(self):
        doc = self.contract('ftc')
        doc['tests']['tenant_isolation'].update(result='not_applicable', exception={
            'owner': 'reviewer', 'citation': '314', 'rationale': 'skip test'})
        self.assertFalse(r.evaluate_document(doc, self.root)['verified'])
        path = self.root / 'contract.json'
        path.write_text(json.dumps(self.contract('ftc')))
        from ore_runtime import evaluate
        report = evaluate('ore-safeguards-monitor', {'_repo': str(self.root), 'contract': 'contract.json'}, {})
        self.assertTrue(report['verified'])
        with self.assertRaises(ValueError):
            evaluate('ore-signature-guard', {'_repo': str(self.root), 'contract': 'contract.json'}, {})

    def test_flow_analyzer_rejects_regulatory_precondition_failure(self):
        from ore_flow import analyze_flow
        doc = json.loads((ROOT / 'evals/fixtures/flows/factory.json').read_text(encoding='utf-8'))
        doc['regulatory_transitions'] = [{'domain': 'ftc', 'before': {'tenant': 'a', 'privileges': ['read']},
                                         'after': {'tenant': 'b', 'privileges': ['admin'], 'authorized': True, 'protected': True}}]
        result = analyze_flow(doc)
        self.assertFalse(result['continuity_verified'])
        self.assertTrue(any(f['code'] == 'regulatory_transition_blocked' for f in result['findings']))

    def test_free_form_or_failed_observation_cannot_pass_technical_control(self):
        doc = self.contract('ftc')
        artifact = json.loads((self.root / 'proof.txt').read_text())
        artifact['checks']['mfa']['result'] = 'failed'
        (self.root / 'proof.txt').write_text(json.dumps(artifact))
        self.proof['sha256'] = hashlib.sha256((self.root / 'proof.txt').read_bytes()).hexdigest()
        self.assertFalse(r.evaluate_document(doc, self.root)['verified'])
        (self.root / 'proof.txt').write_text('All controls passed, trust me')
        self.proof['sha256'] = hashlib.sha256((self.root / 'proof.txt').read_bytes()).hexdigest()
        self.assertFalse(r.evaluate_document(doc, self.root)['verified'])

    def cli(self, *args):
        result = subprocess.run([sys.executable, str(ROOT / 'skills/ore/scripts/ore_state.py'),
                                 *args, '--repo', str(self.root)], capture_output=True, text=True)
        return result

    def test_gate_cli_rejects_claims_and_rechecks_completion(self):
        (self.root / 'contract.json').write_text(json.dumps(self.contract('ftc')))
        started = self.cli('start', '--title', 'Synthetic', '--objective', 'Verify gates', '--kind', 'general',
                           '--acceptance', 'Evidence checked', '--deliverable', 'Build:100', '--gate', 'FTC_SECURITY_CONTROLS')
        self.assertEqual(started.returncode, 0, started.stderr)
        state = json.loads(started.stdout)
        def update(*args):
            return self.cli('update', '--task-id', state['task_id'], '--expect-revision', str(state['revision']), *args)
        claimed = update('--gate', 'FTC_SECURITY_CONTROLS=passed', '--evidence', 'FTC_SECURITY_CONTROLS:trust me')
        self.assertNotEqual(claimed.returncode, 0)
        args = ['--deliverable', 'Build=done', '--evidence', 'Build:implemented']
        for name in ['SPEC_FIDELITY', 'FORM_INTELLIGENCE', 'HANDOFF']:
            args += ['--gate', name + '=not_applicable', '--evidence', name + ':synthetic task']
        args += ['--gate', 'FTC_SECURITY_CONTROLS=passed', '--evidence', 'FTC_SECURITY_CONTROLS:contract.json']
        updated = update(*args)
        self.assertEqual(updated.returncode, 0, updated.stderr)
        state = json.loads(updated.stdout)
        (self.root / 'proof.txt').write_text('tampered')
        completed = self.cli('complete', '--task-id', state['task_id'], '--expect-revision', str(state['revision']))
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn('Regulatory evidence changed', completed.stderr)


if __name__ == '__main__':
    unittest.main()
