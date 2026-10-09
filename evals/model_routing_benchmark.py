"""Reproducible SYNTHETIC policy comparison, not an inference benchmark.

Run: python evals/model_routing_benchmark.py
No network, credentials, billed tokens or quality claims.
"""
import json
from test_ore_models import request, NOW, EXPIRY, TASK, CURRENT, CANDIDATE
from ore_models import route, mutate
from ore_runtime import initial_governance

CATEGORIES = {'code-search': 0, 'documentation': 1, 'frontend': 2, 'backend': 2,
              'debugging': 3, 'refactoring': 3, 'architecture': 3, 'security': 4,
              'business-flows': 4, 'change-verification': 3}


def compare():
    records = []
    for category, level in CATEGORIES.items():
        for strategy in ('fixed', 'adaptive', 'adaptive-escalation'):
            payload = request()
            payload['task_profile'].update(complexity=level, risk=level, reasoning=level, uncertainty=level)
            payload['task_profile']['acceptance'] = ['Same fixture acceptance for all strategies']
            data = initial_governance('project')
            if strategy == 'fixed':
                data = mutate(data, 'model-policy', dict(scope='task', policy={'locks': CURRENT}, expires_at=EXPIRY), 'project', NOW, TASK)
            elif strategy == 'adaptive-escalation':
                payload.update(failure_cause='capability', escalation_evidence=True, attempts=1, history=[CANDIDATE])
            result = route(payload, TASK, data, 'project', NOW)
            assert result['gates'] == ['TESTS']
            assert result['profile']['acceptance'] == payload['task_profile']['acceptance']
            assert result['model_changed'] is False
            records.append({'category': category, 'strategy': strategy, 'recommendation': result['recommended'],
                            'approval_status': result['approval_status'], 'model_changed': False,
                            'acceptance': result['profile']['acceptance'], 'gates': result['gates']})
    return {'kind': 'synthetic-policy-contracts', 'fixture_version': 1, 'scenarios': len(records),
            'provider_calls': 0, 'measured_tokens': None, 'measured_cost': None,
            'task_success_rate': None, 'savings': None, 'records': records}


if __name__ == '__main__':
    print(json.dumps(compare(), indent=2))
