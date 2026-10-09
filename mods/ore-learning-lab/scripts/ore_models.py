"""Versioned adaptive routing contracts. No provider calls; ore_state is sole writer.

Registry entries are observations supplied by a trusted host operator, never
instructions scraped from repositories. Native execution adapters remain unverified.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import re

from ore_runtime import require, timestamp, valid_now, validate_governance

VERSION = 1
HOSTS = {'claude-code', 'codex', 'chatgpt'}
EFFORTS = ['minimal', 'low', 'medium', 'high', 'xhigh', 'max', 'ultra']
DIMENSIONS = ('complexity', 'scope', 'dependencies', 'reasoning', 'risk',
              'context', 'tools', 'verification', 'uncertainty', 'cost')
ACTIONS = {'model-policy', 'model-decision'}


def inspect_host(host, path=None):
    """Read explicitly named configuration; no environment, secrets or account probe."""
    require(host in HOSTS, 'Unsupported host adapter')
    sources = {
        'claude-code': 'https://code.claude.com/docs/en/model-config',
        'codex': 'https://developers.openai.com/codex/config-reference',
        'chatgpt': 'manual model picker; no verified conversation-switch API',
    }
    requested = {'provider': None, 'model_id': None, 'effort': None}
    if path is not None:
        from pathlib import Path
        file = Path(path)
        require(file.is_file() and file.stat().st_size <= 1_000_000, 'Configuration must be a bounded local file')
        if host == 'codex':
            import tomllib
            data = tomllib.loads(file.read_text(encoding='utf-8'))
            requested = {'provider': data.get('model_provider'), 'model_id': data.get('model'), 'effort': data.get('model_reasoning_effort')}
        elif host == 'claude-code':
            data = json.loads(file.read_text(encoding='utf-8'))
            require(isinstance(data, dict), 'Invalid host configuration')
            requested = {'provider': None, 'model_id': data.get('model'), 'effort': data.get('effortLevel')}
        else:
            raise ValueError('ChatGPT has no local configuration adapter')
        for field in ('provider', 'model_id'):
            if requested[field] is not None:
                identifier(requested[field])
        require(requested['effort'] in EFFORTS or requested['effort'] is None, 'Unrecognized configured effort')
    return {'schema_version': VERSION, 'host': host, 'requested': requested, 'effective': None,
            'registry': {'schema_version': VERSION, 'host': host, 'source': 'host-observation', 'models': []},
            'documented_source': sources[host], 'adapter_status': 'experimental-not-live-verified',
            'execution': 'manual-host-selection-required', 'account_availability': 'unknown', 'model_changed': False}


def identifier(value):
    require(isinstance(value, str) and bool(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:/\[\]-]{0,159}', value)), 'Invalid model identifier')
    return value


def number(value):
    require(type(value) in (int, float) and math.isfinite(value) and value >= 0, 'Invalid nonnegative finite metric')
    return value


def config(value):
    require(isinstance(value, dict) and set(value) == {'provider', 'model_id', 'effort'}, 'Configuration requires provider, model_id, effort only')
    identifier(value['provider'])
    identifier(value['model_id'])
    require(value['effort'] in EFFORTS or value['effort'] is None, 'Unknown effort')
    return copy.deepcopy(value)


def operation(value):
    return 'model-route:' + hashlib.sha256(json.dumps(config(value), sort_keys=True).encode()).hexdigest()


def registry(value, now):
    require(isinstance(value, dict) and value.get('schema_version') == VERSION, 'Invalid registry version')
    require(value.get('host') in HOSTS, 'Unsupported provider host; recommendation only')
    require(value.get('source') in {'host-observation', 'operator-verified'}, 'Untrusted routing registry source')
    require(isinstance(value.get('models'), list) and len(value['models']) <= 100, 'Invalid registry models')
    seen = set()
    for row in value['models']:
        require(isinstance(row, dict), 'Invalid registry entry')
        key = (identifier(row.get('provider')), identifier(row.get('model_id')))
        require(key not in seen, 'Duplicate model')
        seen.add(key)
        require(type(row.get('available')) is bool and type(row.get('restricted')) is bool, 'Availability must be observed explicitly')
        require(type(row.get('max_complexity')) is int and 0 <= row['max_complexity'] <= 4, 'Invalid evaluated capability')
        require(isinstance(row.get('tools'), list) and all(isinstance(t, str) for t in row['tools']), 'Invalid model tools')
        require(isinstance(row.get('efforts'), list) and all(e in EFFORTS or e is None for e in row['efforts']), 'Invalid model efforts')
        require(isinstance(row.get('selection_scope'), dict) and set(row['selection_scope']) == {'main_session', 'subagent', 'between_tasks'}, 'Invalid selection scopes')
        require(all(v in {'manual', 'documented', 'unsupported'} for v in row['selection_scope'].values()), 'Invalid scope support')
        timestamp(row.get('verified_at'))
        require(timestamp(row['verified_at']) <= timestamp(now) < timestamp(row.get('expires_at')), 'Stale or future registry observation')
        for key in ('input_per_million', 'output_per_million'):
            if row.get(key) is not None:
                number(row[key])
                require(bool(row.get('cost_source')), 'Price needs source')
    return value


def analyze(value):
    require(isinstance(value, dict) and all(type(value.get(k)) is int and 0 <= value[k] <= 4 for k in DIMENSIONS), 'Task profile needs ten explicit dimensions rated 0..4')
    require(isinstance(value.get('required_tools'), list) and all(isinstance(t, str) for t in value['required_tools']), 'Task tools required')
    require(isinstance(value.get('acceptance'), list) and bool(value['acceptance']) and all(isinstance(a, str) and a for a in value['acceptance']), 'Acceptance must be preserved')
    require(isinstance(value.get('gates'), list) and all(isinstance(g, str) for g in value['gates']), 'Quality gates required')
    level = max(value['complexity'], value['reasoning'], value['risk'], value['uncertainty'])
    if max(value['scope'], value['dependencies'], value['context']) >= 3:
        level = max(level, 3)
    return {'level': f'L{level}', 'minimum_capability': level, 'dimensions': {k: value[k] for k in DIMENSIONS},
            'required_tools': value['required_tools'], 'acceptance': value['acceptance'], 'gates': value['gates'],
            'classification_source': 'explicit-rubric', 'uncertainty': 'not benchmark calibrated'}


def policy(value):
    require(isinstance(value, dict), 'Policy must be an object')
    allowed = {'mode', 'profile', 'locks', 'excluded_models', 'excluded_providers', 'max_effort', 'budget',
               'max_retries', 'max_subagents', 'preferences'}
    require(set(value) <= allowed, 'Unknown policy field')
    result = {'mode': 'APPROVAL_REQUIRED', 'profile': 'Balanced', 'locks': {}, 'excluded_models': [],
              'excluded_providers': [], 'max_effort': 'ultra', 'budget': None, 'max_retries': 2, 'max_subagents': 0, 'preferences': []}
    result.update(copy.deepcopy(value))
    require(result['mode'] in {'MANUAL', 'APPROVAL_REQUIRED', 'AUTHORIZED_AUTO'}, 'Invalid authorization mode')
    require(result['profile'] in {'Economy', 'Balanced', 'Quality', 'Custom'}, 'Invalid routing profile')
    require(result['max_effort'] in EFFORTS, 'Invalid effort ceiling')
    require(isinstance(result['locks'], dict) and set(result['locks']) <= {'provider', 'model_id', 'effort'}, 'Invalid locks')
    for k, v in result['locks'].items():
        require(v in EFFORTS or v is None, 'Invalid effort lock') if k == 'effort' else identifier(v)
    for name in ('excluded_models', 'excluded_providers'):
        require(isinstance(result[name], list), 'Invalid exclusions')
        for item in result[name]:
            identifier(item)
    for name in ('max_retries', 'max_subagents'):
        require(type(result[name]) is int and 0 <= result[name] <= 20, 'Invalid operation limit')
    if result['budget'] is not None:
        number(result['budget'])
    require(isinstance(result['preferences'], list), 'Invalid preferences')
    for preference in result['preferences']:
        require(isinstance(preference, dict) and set(preference) == {'department', 'configuration'}, 'Invalid preference')
        identifier(preference['department'])
        config(preference['configuration'])
    require(result['profile'] != 'Custom' or result['preferences'], 'Custom profile requires explicit preferences')
    return result


def validate_routing(value):
    require(isinstance(value, dict) and value.get('schema_version') == VERSION, 'Invalid routing state version')
    require(isinstance(value.get('policies'), list) and isinstance(value.get('decisions'), list), 'Invalid routing state')
    for record in value['policies']:
        require(isinstance(record, dict), 'Invalid policy record')
        require(record.get('scope') in {'project', 'session', 'task'}, 'Invalid preference scope')
        require(isinstance(record.get('scope_id'), str) and bool(record['scope_id']), 'Invalid scope id')
        policy(record.get('policy'))
        timestamp(record.get('expires_at'))
        require(record.get('status') in {'active', 'replaced'}, 'Invalid policy status')
    for record in value['decisions']:
        require(isinstance(record, dict) and record.get('model_changed') is False, 'Invalid decision observation')
        for key in ('requested', 'effective', 'recommended'):
            if record.get(key) is not None:
                config(record[key])
    return value


def effective_policy(data, task_id, session_id, now):
    records = data.get('routing', {}).get('policies', [])
    active = [r for r in records if valid_now(r, now) and (r['scope'] == 'project' or
              r['scope'] == 'task' and r['scope_id'] == task_id or r['scope'] == 'session' and r['scope_id'] == session_id)]
    result = policy({})
    # More specific preferences override; restrictions always accumulate.
    for index, r in enumerate(sorted(active, key=lambda r: ['project', 'session', 'task'].index(r['scope']))):
        new = policy(r['policy'])
        require(not any(k in new['locks'] and new['locks'][k] != v for k, v in result['locks'].items()), 'Conflicting locks; ask user')
        new['locks'] = {**result['locks'], **new['locks']}
        for field in ('excluded_models', 'excluded_providers'):
            new[field] = sorted(set(result[field] + new[field]))
        new['max_effort'] = EFFORTS[min(EFFORTS.index(result['max_effort']), EFFORTS.index(new['max_effort']))]
        for field in ('budget', 'max_retries', 'max_subagents'):
            old = result[field]
            if index and old is not None:
                new[field] = old if new[field] is None else min(old, new[field])
        if result['mode'] == 'MANUAL':
            new['mode'] = 'MANUAL'
        result = new
    return result


def approval_for(data, candidate, host, scope, task_id, session_id, now):
    for record in data['approvals']:
        if not valid_now(record, now) or record['operation'] != operation(candidate) or record['environment'] != f'{host}:{scope}':
            continue
        target = record['scope']
        if target == f'task:{task_id}' or target == f'session:{session_id}' and session_id or target == 'project':
            return record['id']
    return None


def expected_cost(row, payload):
    if any(row.get(k) is None for k in ('input_per_million', 'output_per_million')):
        return None
    usage = payload.get('estimated_tokens')
    if not isinstance(usage, dict) or not {'input', 'output'} <= set(usage):
        return None
    initial = (number(usage['input']) * row['input_per_million'] + number(usage['output']) * row['output_per_million']) / 1_000_000
    costs = payload.get('overheads')
    if not isinstance(costs, dict) or not {'retry_multiplier', 'validation', 'delegation', 'recovery'} <= set(costs):
        return None
    # Costs include validation, delegation, recovery and bounded retries; no fabricated success rate.
    return initial * (1 + number(costs.get('retry_multiplier', 0))) + sum(number(costs.get(k, 0)) for k in ('validation', 'delegation', 'recovery'))


def route(payload, task, governance, project, now):
    validate_governance(governance, project)
    require(isinstance(payload, dict) and payload.get('source') == 'explicit-user-or-host', 'Routing input must come from an explicit user or host observation')
    current = config(payload.get('current'))
    catalog = registry(payload.get('registry'), now)
    profile = analyze(payload.get('task_profile'))
    # The operational risk scale remains distinct; conservatively map its top
    # two levels to L4 routing and retain every authoritative requirement.
    risk = task.get('risk', 'L0')
    require(risk in {f'L{i}' for i in range(6)}, 'Invalid authoritative task risk')
    floor = min(int(risk[1:]), 4)
    profile['minimum_capability'] = max(profile['minimum_capability'], floor)
    profile['level'] = f"L{profile['minimum_capability']}"
    profile['acceptance'] = list(dict.fromkeys(task.get('acceptance_criteria', []) + profile['acceptance']))
    profile['gates'] = list(dict.fromkeys([k for k, v in task.get('gates', {}).items() if v.get('required')] + profile['gates']))
    session_id = payload.get('session_id', '')
    require(isinstance(session_id, str), 'Invalid session id')
    scope = payload.get('selection_scope', 'main_session')
    require(scope in {'main_session', 'subagent', 'between_tasks'}, 'Invalid selection scope')
    rules = effective_policy(governance, task['id'], session_id, now)
    attempts = payload.get('attempts', 0)
    require(type(attempts) is int and attempts >= 0, 'Invalid retry count')
    subagents_used = payload.get('subagents_used', 0)
    require(type(subagents_used) is int and subagents_used >= 0, 'Invalid delegation count')
    history = payload.get('history', [])
    require(isinstance(history, list), 'Invalid routing history')
    for item in history:
        config(item)
    failure = payload.get('failure_cause')
    blocked = None
    if failure in {'environment', 'permissions', 'network', 'credentials', 'tool', 'external', 'ambiguous', 'context'}:
        blocked = 'Repair the failure cause before model escalation'
    elif failure and failure not in {'capability', 'implementation', 'test'}:
        blocked = 'Unknown failure cause; diagnose first'
    elif failure and attempts >= rules['max_retries']:
        blocked = 'Retry limit reached'
    elif failure and payload.get('escalation_evidence') is not True:
        blocked = 'Escalation lacks capability evidence'
    if scope == 'subagent' and (rules['max_subagents'] == 0 or subagents_used >= rules['max_subagents']):
        blocked = 'Delegation limit reached; explicit delegation authorization required'
    candidates = []
    rejected = []
    for row in catalog['models']:
        reasons = []
        if not row['available'] or row['restricted']:
            reasons.append('unavailable or restricted')
        if row['selection_scope'][scope] == 'unsupported':
            reasons.append('scope unsupported')
        if row['max_complexity'] < profile['minimum_capability'] or not set(profile['required_tools']) <= set(row['tools']):
            reasons.append('insufficient evaluated capability or tools')
        if row['provider'] in rules['excluded_providers'] or row['model_id'] in rules['excluded_models']:
            reasons.append('excluded')
        for effort in row['efforts']:
            candidate = {'provider': row['provider'], 'model_id': row['model_id'], 'effort': effort}
            local = list(reasons)
            if any(candidate[k] != v for k, v in rules['locks'].items()):
                local.append('locked')
            if effort is not None and EFFORTS.index(effort) > EFFORTS.index(rules['max_effort']):
                local.append('effort ceiling')
            minimum_effort = 'high' if profile['dimensions']['reasoning'] >= 3 else 'medium' if profile['dimensions']['reasoning'] >= 2 else 'low'
            if effort is not None and EFFORTS.index(effort) < EFFORTS.index(minimum_effort):
                local.append('insufficient reasoning effort')
            if failure and candidate in history:
                local.append('cycle prevention')
            cost = expected_cost(row, payload)
            spent = number(payload.get('reported_cost', 0))
            if rules['budget'] is not None and (cost is None or spent + cost > rules['budget']):
                local.append('budget exceeded or estimate unavailable')
            if local:
                rejected.append({'configuration': candidate, 'reasons': local})
            else:
                candidates.append((candidate, row, cost))
    preferred = next((r['configuration'] for r in rules['preferences'] if r['department'] == payload.get('department')), None)
    def rank(entry):
        c, row, cost = entry
        preference = 0 if preferred is None or c == preferred else 1
        capacity = -row['max_complexity'] if rules['profile'] == 'Quality' else row['max_complexity']
        price = float('inf') if cost is None else cost
        conservative = 0 if c == current else 1
        return (preference, capacity, cost is None, price, conservative) if rules['profile'] == 'Quality' else (preference, cost is None, conservative if cost is None else price, capacity, conservative)
    candidates.sort(key=rank)
    chosen = candidates[0] if candidates and not blocked else None
    recommended = chosen[0] if chosen else None
    approval = approval_for(governance, recommended, catalog['host'], scope, task['id'], session_id, now) if recommended else None
    status = 'blocked' if not chosen else 'keep-current' if recommended == current else 'manual' if rules['mode'] == 'MANUAL' else 'authorized' if approval else 'awaiting-approval'
    effective = payload.get('observed')
    if effective is not None:
        effective = config(effective)
    gate_records = [g for g in task.get('gates', {}).values() if g.get('required')]
    quality = 'failed' if any(g.get('status') == 'failed' for g in gate_records) else 'passed-gates' if gate_records and all(g.get('status') in {'passed', 'not_applicable'} for g in gate_records) else 'verification required'
    return {'schema_version': VERSION, 'requested': current, 'effective': effective, 'effective_source': 'host-observation' if effective else 'unknown',
            'profile': profile, 'policy': rules, 'recommended': recommended, 'approval_status': status, 'approval_id': approval,
            'estimated_total_cost': chosen[2] if chosen else None, 'reported_usage': None,
            'savings': None, 'budget_enforcement': 'advisory; no host spend control', 'quality_status': quality,
            'gates': profile['gates'], 'reason': blocked or ('Eligible within rubric, tools, locks and budget' if chosen else 'No eligible configuration'),
            'rejected': rejected, 'execution': 'manual-host-selection-required', 'model_changed': False,
            'adapter_status': 'experimental-not-live-verified', 'uncertainty': 'Costs are estimates; success rates need provider benchmarks'}


def mutate(data, action, payload, project, now, task):
    """Called only after ore_state confirmation, locking and revision checks."""
    validate_governance(data, project)
    require(action in ACTIONS, 'Unknown routing action')
    result = copy.deepcopy(data)
    routing = result.setdefault('routing', {'schema_version': VERSION, 'policies': [], 'decisions': []})
    if action == 'model-policy':
        require(payload.get('scope') in {'project', 'session', 'task'}, 'Only project, session and task persistence is supported')
        scope = payload['scope']
        scope_id = project if scope == 'project' else task['id'] if scope == 'task' else identifier(payload.get('session_id'))
        expiry = payload.get('expires_at')
        require(timestamp(expiry) > timestamp(now), 'Policy must have future expiry')
        value = policy(payload.get('policy'))
        for r in routing['policies']:
            if r['scope'] == scope and r['scope_id'] == scope_id:
                r['status'] = 'replaced'
        routing['policies'].append({'scope': scope, 'scope_id': scope_id, 'policy': value, 'expires_at': expiry, 'status': 'active'})
    else:
        decision = route(payload, task, data, project, now)
        # Persist allowlisted metadata only. No free text, keys, prompts or usage blobs.
        record = {k: decision[k] for k in ('requested', 'effective', 'recommended', 'approval_status', 'approval_id', 'model_changed', 'estimated_total_cost')}
        record.update(policy_version=VERSION, host=payload['registry']['host'], selection_scope=payload.get('selection_scope', 'main_session'),
                      task_id=task['id'], at=now, reason=decision['reason'], level=decision['profile']['level'],
                      dimensions=decision['profile']['dimensions'], governance_revision=data['revision'],
                      requirements_hash=hashlib.sha256(json.dumps({'acceptance': decision['profile']['acceptance'], 'gates': decision['gates']}, sort_keys=True).encode()).hexdigest(),
                      registry_hash=hashlib.sha256(json.dumps(payload['registry'], sort_keys=True).encode()).hexdigest())
        routing['decisions'].append(record)
    result['revision'] += 1
    result['events'].append({'schema_version': VERSION, 'kind': action, 'at': now, 'project': project,
                             'origin': 'ore_state.py', 'permission': 'explicit-user-confirmation'})
    validate_routing(routing)
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Inspect requested host configuration without account probing or changes')
    parser.add_argument('host', choices=sorted(HOSTS))
    parser.add_argument('--config', help='Explicit local JSON (Claude) or TOML (Codex) configuration path')
    args = parser.parse_args()
    try:
        print(json.dumps(inspect_host(args.host, args.config), indent=2))
        return 0
    except (OSError, ValueError, TypeError):
        print('Host configuration cannot be safely inspected', file=__import__('sys').stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
