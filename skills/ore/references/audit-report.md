# ORE audit report and validation contract

## Human report template

Use the user's language and include the following after every audit, including stopped/partial runs.

```text
ORE — AUDIT REPORT
Project: <verified name>
Detected technologies: <actual stack and versions; unknowns>
Date: <user-local date and timezone>
Scope: <paths, services, environments, revision and authority>
Jurisdictions/business: <verified facts, sources and unresolved applicability>

Executive summary
Confirmed unresolved: P0 <count>, P1 <count>, P2 <count>, P3 <count>
Suspected findings: <separate count and missing evidence>
Resolved: <count with passing retest/regression evidence>
Fixed but unvalidated / accepted risks / pending: <separate counts>
Authorization or legal review required: <specific remaining actions/questions>

Technical findings (repeat per stable ID)
ID / linked control IDs / severity / confidence and status:
Path or component / environment / evidence (redacted):
Risk / exploit conditions / impact:
Applied or recommended repair / side effects / owner:
Validation: <baseline, retest, affected regression, result and revision>

Control coverage
ID / applicability / result / evidence / related findings / limitations
Distinguish evaluated, non-applicable, out-of-scope and unverified controls.

Test results
Command/check / environment / revision / passed, failed or not_run / artifact
Describe missing tools/access and exactly what remains unverified.

Production recommendations
Remaining priorities, dependencies, deployment/migration/recovery steps,
human/legal approvals, and exact next validation action.

Checkpoint
Run and iteration (0–5), baseline/current revision, verified progress,
stop reason, pending P0/P1, gate evidence, owner and next action.
Progress: <computed durable progress and gates>
Token efficiency: <supported accounting or 0 tokens demonstrated>
```

Accepted risks retain severity and residual-risk visibility; do not count them as resolved. Report no finding as resolved from a code change alone. Do not assert complete security, certification or exhaustive coverage. For strict no-write audits deliver this in conversation or the authorized external store.

## Optional machine-readable ledger

Use this when durable structured findings or automated report checking help. Keep it with the existing task artifacts (for example `.ore/audits/<task-id>.json`) and refer to it from the task's evidence/next action; do not change the existing task schema. This ledger is optional for short focused reviews. JSON fields:

- `project`, `date`, `scope`, `revision`: nonempty strings; `mode`: `audit`, `security`, `compliance`, `accessibility`, `fix`, `loop` or `report`.
- `iteration`: integer 0–5; `stop_reason`: nonempty description; `next_action`: concrete continuation or completion action.
- `controls`: array of `{id, status, evidence}`. `status` is `passed`, `failed`, `not_applicable`, `not_evaluated` or `out_of_scope`. Evidence is a nonempty redacted string, including an applicability reason or precise coverage gap. Integral `audit` includes all 36 IDs; focused modes explicitly state omitted coverage in scope/report.
- `tests`: array of `{id, status, evidence, revision}` with unique IDs; status is `passed`, `failed` or `not_run`. Evidence records command/environment/result or missing capability. Do not pass a check that was not executed.
- `findings`: array of `{id, controls, severity, status, component, evidence, risk, preconditions, impact, correction, side_effects, validation}`. `severity` is P0/P1/P2/P3. `status` is `suspected`, `confirmed`, `fixed_unvalidated`, `resolved` or `accepted_risk`. Each textual field is a nonempty redacted string. `validation` contains `retest` and `regression` arrays of test IDs. `resolved` requires both arrays nonempty and all referenced checks passed for the current report revision. An `accepted_risk` also has `acceptance: {owner, rationale, scope, expires}`; preserve this independently from validation.

Run `python <ore-skill>/scripts/validate_audit_report.py <ledger.json>` when using the ledger. The validator checks report consistency, control IDs, the five-iteration ceiling and current-state evidence links; it does **not** perform scanning, establish exploitability, verify evidence authenticity, redact arbitrary strings, determine legislation or execute fixes. Never supply it secrets or raw production data. Human assessment remains necessary for applicability, severity and truth of evidence.

## Iteration decision

Before each repair batch, record authority, selected confirmed findings and affected gates. After repair, retest/regression and re-audit establish progress. Continue only within the same requested scope, with verified progress and available authority, up to five counted iterations. On no progress or the limit, checkpoint unresolved priorities and stop. Do not reset the count inside a run. A failure or blocked test invalidates affected closure even if earlier tests passed; supersede stale evidence and reopen the gate/finding.
