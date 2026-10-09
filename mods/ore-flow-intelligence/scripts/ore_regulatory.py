"""ORE regulatory contracts: offline evidence verification, never legal notification.

Pure signature patterns require an application-owned transactional store and trusted
identity/authentication adapters. SHA256 binding detects edits; it is not a digital
signature or a substitute for tamper-resistant storage.
"""
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path

GATES = {
    'FDA_PART11_APPLICABILITY', 'FDA_SIGNATURE_INTEGRITY', 'FDA_RECORD_CONTROLS',
    'FTC_SAFEGUARDS_APPLICABILITY', 'FTC_SECURITY_CONTROLS', 'REGULATORY_EVIDENCE',
}
FDA_TESTS = {'legitimate', 'unauthorized', 'disabled', 'reuse', 'altered', 'versions',
             'incomplete', 'save_failure', 'retry', 'export', 'module_continuity'}
FTC_TESTS = {'authorized', 'unauthorized', 'tenant_isolation', 'mfa', 'secrets',
             'encryption', 'events', 'disposal', 'incident', 'integration_failure', 'recovery'}
FDA_RECORDS = {'audit_trail', 'history', 'access', 'segregation', 'versioning', 'retention',
               'retrieval', 'readable_copy', 'electronic_copy', 'integrity', 'documentation', 'validation'}
FTC_CONTROLS = {'mfa', 'least_privilege', 'encryption_rest', 'encryption_transit', 'secrets',
                'inventory', 'secure_development', 'monitoring', 'vulnerabilities', 'security_tests',
                'change_management', 'disposal', 'providers', 'unauthorized_detection', 'incident_response'}
DOCUMENTS = {'fda': {'identity_verification', 'training', 'signature_policy', 'agency_certification'},
             'ftc': {'risk_assessment', 'qualified_individual', 'training', 'provider_contracts',
                     'provider_oversight', 'incident_plan', 'management_report', 'exceptions'}}
SOURCES = {'fda': 'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11',
           'ftc': 'https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-314'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def time(value):
    require(isinstance(value, str), 'Timezone-aware timestamp required')
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(parsed.tzinfo is not None, 'Timezone required')
    return parsed


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def no_secrets(value):
    if isinstance(value, dict):
        for key, child in value.items():
            require(key.lower() not in {'password', 'token', 'secret', 'authorization', 'api_key',
                                        'access_token', 'refresh_token', 'credentials'}, 'Secrets forbidden in evidence')
            no_secrets(child)
    elif isinstance(value, list):
        for child in value:
            no_secrets(child)


def sign(record, identity, authentication, ledger, request_id, now):
    """Return candidate ledger; commit record + audit + ledger atomically in host.

    identity/authentication must come from server-side trusted adapters, not client
    booleans. No persistence or external authentication is performed here.
    """
    no_secrets([record, identity, authentication, ledger])
    require(isinstance(request_id, str) and bool(request_id), 'Request id required')
    require(all(record.get(k) for k in ('id', 'version', 'content', 'meaning')), 'Incomplete record')
    require(identity.get('enabled') is True and identity.get('verified') is True, 'Unverified/disabled signer')
    require(identity.get('id') and identity.get('name'), 'Individual identity required')
    require(record['id'] in identity.get('allowed_records', []), 'Signer lacks record permission')
    current = time(now)
    require(time(authentication['at']) <= current < time(authentication['expires_at']), 'Authentication expired/future')
    require(authentication.get('subject') == identity['id'], 'Authentication subject mismatch')
    mode = authentication.get('mode')
    if mode == 'biometric':
        require(authentication.get('owner_only') is True, 'Biometric owner controls required')
    else:
        require(mode == 'non-biometric', 'Explicit signature authentication mode required')
        components = authentication.get('components', [])
        require(isinstance(components, list) and all(isinstance(c, str) for c in components), 'Invalid components')
        continuous = authentication.get('continuous_session') is True
        if continuous:
            require(authentication.get('session_id'), 'Controlled session identity required')
        subsequent = continuous and authentication.get('first_signing') is False
        require(len(set(components)) >= (1 if subsequent else 2), '11.200 components missing')
        require(authentication.get('owner_only') is True and authentication.get('two_person_admin') is True,
                'Signature ownership/administration controls missing')
        if subsequent:
            require(authentication.get('session_initial_signature') in {s['id'] for s in ledger
                    if s['signer_id'] == identity['id'] and s.get('initial_signing') is True
                    and s.get('session_id') == authentication.get('session_id')},
                    'Continuous session first signature missing')
    require(authentication.get('evidence_ref'), 'Trusted authentication evidence required')
    binding = digest(record)
    prior = next((s for s in ledger if s['request_id'] == request_id), None)
    if prior:
        require(prior['record_digest'] == binding and prior['signer_id'] == identity['id'], 'Reused request/signature')
        return copy.deepcopy(ledger), copy.deepcopy(prior)
    signature = {'id': digest([request_id, binding, identity['id']]), 'request_id': request_id,
                 'record_id': record['id'], 'version': record['version'], 'record_digest': binding,
                 'signer_id': identity['id'], 'signer_name': identity['name'], 'at': now,
                 'meaning': record['meaning'], 'authentication_evidence': authentication['evidence_ref'],
                 'session_id': authentication.get('session_id'),
                 'initial_signing': authentication.get('first_signing') is not False, 'status': 'active'}
    return copy.deepcopy(ledger) + [signature], signature


def verify_signature(record, signature):
    try:
        time(signature.get('at'))
    except (ValueError, TypeError):
        return False
    return (signature.get('status') == 'active' and signature.get('record_id') == record.get('id')
            and signature.get('version') == record.get('version') and signature.get('record_digest') == digest(record)
            and signature.get('meaning') == record.get('meaning')
            and all(signature.get(k) for k in ('id', 'signer_id', 'signer_name', 'at', 'meaning', 'authentication_evidence')))


def supersede(ledger, signature_id, replacement, actor, reason, now):
    """Preserve approval history; only an authorized owner may supersede it."""
    require(actor.get('enabled') is True and actor.get('can_supersede') is True and actor.get('id'),
            'Supersession authorization required')
    require(isinstance(reason, str) and bool(reason.strip()), 'Supersession reason required')
    time(now)
    result = copy.deepcopy(ledger)
    prior = next((s for s in result if s['id'] == signature_id), None)
    successor = next((s for s in result if s['id'] == replacement), None)
    require(prior and successor and prior['status'] == successor['status'] == 'active'
            and prior['id'] != successor['id'] and prior['record_id'] == successor['record_id'],
            'Existing active replacement for same record required')
    prior.update(status='superseded', superseded_by=replacement, changed_by=actor['id'],
                 changed_at=now, reason=reason)
    return result


def transition(kind, before, after, signature=None):
    """Flow precondition; application must call it at every relevant transition."""
    if kind == 'fda':
        return bool(signature and verify_signature(before, signature) and verify_signature(after, signature))
    require(kind == 'ftc', 'Unknown regulatory transition')
    return (set(after.get('privileges', [])) <= set(before.get('privileges', []))
            and set(after.get('data_fields', [])) <= set(before.get('data_fields', []))
            and after.get('authorized') is True and after.get('protected') is True
            and before.get('tenant') is not None and after.get('tenant') == before['tenant'])


def incident_readiness(event):
    no_secrets(event)
    count = event.get('consumers')
    require(count is None or type(count) is int and count >= 0, 'Invalid consumer count')
    discovery = time(event['discovered_at'])
    exposed = event.get('encrypted') is False or event.get('key_compromised') is True
    acquisition = event.get('unauthorized_acquisition') is True or (
        event.get('unauthorized_access') is True and not event.get('reliable_no_acquisition_evidence'))
    uncertain = count is None or event.get('encrypted') is None or (
        event.get('unauthorized_access') is None and event.get('unauthorized_acquisition') is None)
    candidate = count is not None and count >= 500 and exposed and acquisition
    return {'status': 'potential_notification_event' if candidate else 'review_required' if uncertain else 'threshold_not_established',
            'deadline': (discovery + timedelta(days=30)).isoformat(), 'discovered_at': event['discovered_at'],
            'timeline': event.get('timeline', []), 'evidence': event.get('evidence', []),
            'owner': event.get('owner', 'unassigned'), 'notify_as_soon_as_possible': candidate,
            'notification_submitted': False, 'authorized_review_required': True}


def evidence(root, item):
    require(isinstance(item, dict), 'Evidence descriptor required')
    relative = item.get('path')
    require(isinstance(relative, str) and relative and not Path(relative).is_absolute()
            and ':' not in relative and '..' not in relative.replace('\\', '/').split('/'), 'Unsafe evidence path')
    path = (root / relative).resolve()
    require(path.is_relative_to(root) and path.is_file(), 'Evidence missing/outside repository')
    require(hashlib.sha256(path.read_bytes()).hexdigest() == item.get('sha256'), 'Evidence digest mismatch')
    require(item.get('owner') and item.get('validation') and item.get('limitations') is not None,
            'Evidence needs owner, executed validation and limitations')
    time(item.get('at'))
    return {'path': relative, 'sha256': item['sha256']}


def evaluate_document(document, repo):
    """Verify file-bound assertions, not their provenance or full legal adequacy."""
    root = Path(repo).resolve()
    require(isinstance(document, dict) and document.get('schema_version') == 1, 'Invalid regulatory contract')
    no_secrets(document)
    domain = document.get('domain')
    require(domain in SOURCES, 'Invalid regulatory domain')
    require(isinstance(document.get('risk'), str) and document['risk'].strip(), 'Risk assessment required')
    scope = document.get('scope', {})
    require(scope.get('status') in {'applicable', 'not_applicable', 'pending'}, 'Applicability decision required')
    required_scope = ('activity', 'predicate_rules', 'electronic_records', 'exclusions', 'fda_enforcement_policy') if domain == 'fda' else (
        'activity', 'jurisdiction', 'financial_institution_analysis', 'entity_role', 'protected_data', 'providers', '314_6_analysis')
    require(all(k in scope for k in required_scope), 'Incomplete applicability analysis')
    require(scope.get('owner') and scope.get('rationale') and scope.get('citations'), 'Scope review evidence required')
    source = document.get('source', {})
    require(source.get('url') == SOURCES[domain] and source.get('version'), 'Official source/version required')
    time(source.get('checked_at'))
    dependencies = [evidence(root, e) for e in scope.get('evidence', [])]
    decided = scope['status'] != 'pending' and bool(dependencies)
    applicable = scope['status'] == 'applicable'
    names = ['FDA_PART11_APPLICABILITY', 'FDA_SIGNATURE_INTEGRITY', 'FDA_RECORD_CONTROLS'] if domain == 'fda' else [
        'FTC_SAFEGUARDS_APPLICABILITY', 'FTC_SECURITY_CONTROLS']
    findings, gates = [], {}
    def gate(name, ok):
        gates[name] = {'status': ('blocked' if not decided else 'not_applicable' if not applicable and name != names[0]
                                  else 'passed' if ok else 'failed'), 'source': source, 'applicability': scope,
                       'risk': document.get('risk', 'unassessed'), 'evidence_required': 'hash-bound executed checks and owner review',
                       'validation': 'ore_regulatory.evaluate_document', 'limitations': ['Offline artifact checks; provenance and legal adequacy need authorized review'],
                       'owner': scope['owner'], 'exception': document.get('exception')}
    gate(names[0], decided)
    controls = document.get('controls', {})
    tests = document.get('tests', {})
    required = FDA_RECORDS if domain == 'fda' else FTC_CONTROLS
    def check(identifier, collection):
        item = collection.get(identifier, {})
        refs = item.get('evidence', [])
        proofs = [evidence(root, e) for e in refs]
        dependencies.extend(proofs)
        exception = item.get('exception', {})
        exempt = (collection is not tests and item.get('result') == 'not_applicable' and exception.get('owner') and exception.get('citation')
                  and exception.get('rationale') and proofs)
        executed = True
        if collection is controls or collection is tests:
            executed = False
            for proof in proofs:
                try:
                    artifact = json.loads((root / proof['path']).read_text(encoding='utf-8'))
                    observation = artifact['checks'][identifier]
                    if (artifact.get('schema_version') == 1 and observation.get('result') == 'passed'
                            and observation.get('validation') and observation.get('subject')
                            and observation.get('owner')):
                        time(observation.get('at'))
                        executed = True
                except (ValueError, KeyError, TypeError, AttributeError):
                    continue
        ok = bool(proofs and executed and item.get('result') == 'passed') or bool(exempt)
        if not ok and applicable:
            findings.append({'control': identifier, 'severity': item.get('severity', 'high'),
                             'owner': item.get('owner', scope['owner']), 'status': 'missing_or_failed_evidence'})
        return ok
    control_ok = all([check(c, controls) for c in sorted(required)])
    test_ok = all([check(c, tests) for c in sorted(FDA_TESTS if domain == 'fda' else FTC_TESTS)])
    doc_ok = all([check(c, document.get('documents', {})) for c in sorted(DOCUMENTS[domain])])
    if domain == 'fda':
        pairs = document.get('signed_records', [])
        signature_ok = bool(pairs) and all(verify_signature(p['record'], p['signature']) for p in pairs)
        gate(names[1], signature_ok and test_ok)
        gate(names[2], control_ok)
    else:
        gate(names[1], control_ok and test_ok)
    gate('REGULATORY_EVIDENCE', doc_ok and control_ok and test_ok and all(g['status'] == 'passed' for g in gates.values()))
    dependencies = list({d['path']: d for d in dependencies}.values())
    return {'gates': gates, 'findings': findings, 'dependencies': dependencies,
            'verified': all(g['status'] in {'passed', 'not_applicable'} for g in gates.values()),
            'certified': False, 'notification': incident_readiness(document['incident']) if 'incident' in document else None}


def evaluate_file(repo, relative):
    root = Path(repo).resolve()
    require(isinstance(relative, str) and not Path(relative).is_absolute() and ':' not in relative,
            'Repository-relative regulatory contract required')
    path = (root / relative).resolve()
    require(path.is_relative_to(root) and path.is_file(), 'Contract missing/outside repository')
    result = evaluate_document(json.loads(path.read_text(encoding='utf-8')), root)
    result['dependencies'].append({'path': relative, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    return result
