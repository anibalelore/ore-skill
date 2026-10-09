# ORE 4.2 Adaptive Model Intelligence

This local alpha candidate adds a task rubric, versioned observed-model registry,
selection engine, scoped policy/lock persistence, approval-ledger lookup and an
optional model/usage diagnostic mod. No model is changed automatically. Live host
execution adapters, one-use grant consumption and provider benchmarks remain unverified.

## Implemented interfaces

Canonical runtime: `skills/ore/scripts/ore_models.py`. Persistence belongs exclusively
to `ore_state.py`, using its project lock, atomic governance write, task revision and
governance revision checks. The new optional `routing` section uses schema version 1;
old governance files remain valid. Older readers ignore the optional section, but do
not enforce routing policy. No migration replaces existing task or approval records.

| Component | Current behavior | Limit |
| --- | --- | --- |
| Task analyzer | Ten explicit 0–4 dimensions; authoritative acceptance/gate union and risk floor | Operator assessment; no trained classifier |
| Registry | Bounded, expiring, typed observed inventory | Supplied provenance is not authentication; no automatic account probe |
| Selection | Availability, tools, capability, scope, locks, exclusions, effort, cost, retries | Heuristic capability/price metadata; unknown costs are conservative |
| Approval | Existing exact-config hash ledger lookup with host/operation/task/session/project scope | Authorizes metadata only; no native switch |
| Preferences | Confirmed expiring project/session/task policies with restrictive intersection | No installation/organization writer |
| Claude adapter | Local JSON configuration inspection; native model and usage observation in mod | Live mod launch requires compatible host; manual selection |
| Codex adapter | Explicit local TOML model/effort/provider inspection | No active-task/config mutation or API access claim |
| ChatGPT adapter | Safe empty inventory and manual recommendation fallback | No UI automation |
| Other providers | Reject unsupported hosts | Extension design only |

The router never calls a model endpoint. It does not remove gates, change approvals
for sensitive tools or certify regulated systems. FDA/FTC contracts remain unchanged.

## Install, activate and remove

Agent Skills hosts discover `skills/ore-adaptive-model-routing/SKILL.md` through the
existing ORE package installation. Invoke `$ore-adaptive-model-routing` or ask `$ore`
for model selection. No global host files are edited by installation scripts here.

For Claude Code 2.1.287+ with the repository's mod API available:

```text
/plugin marketplace add ./mods
/plugin install ore-model-router@ore-mods
/plugin enable ore-model-router@ore-mods
/ore-model-router-status
```

CLI management equivalents below were checked through the installed CLI help;
marketplace registration and manifest were validated locally, live installation was
not performed against the user's global environment:

```text
claude plugin disable ore-model-router@ore-mods
claude plugin enable ore-model-router@ore-mods
claude plugin uninstall ore-model-router@ore-mods
```

Disabling the mod removes its commands and observations; other mods retain behavior.
It does not delete approved project policies. Explicitly replace or expire policies
before removing their governance metadata. Do not delete the shared governance file
to remove routing; it also contains unrelated rules and approvals.

Inspect an explicitly selected local host configuration without changes or secret echo:

```text
python skills/ore/scripts/ore_models.py codex
python skills/ore/scripts/ore_models.py codex --config .codex/config.toml
python skills/ore/scripts/ore_models.py claude-code --config .claude/settings.json
python skills/ore/scripts/ore_models.py chatgpt
```

Absent configuration files produce a safe error. These adapters report requested
configuration, never verified account access or effective execution. Read the actual
host picker/account inventory and build an expiring registry before evaluation.

## Policy and lock example

With a valid active ORE task, this real implemented mod command prompts before writing:

```text
/ore-model-router {"action":"model-policy","governanceRevision":0,"payload":{"scope":"task","expires_at":"2026-10-10T00:00:00Z","policy":{"mode":"APPROVAL_REQUIRED","profile":"Balanced","max_retries":2,"max_subagents":0}}}
```

Use a future expiry and the actual current governance revision. To lock the current
configuration, add `locks` containing verified provider, model_id and/or effort.
Do not use commercial example names without resolving actual identifiers. To unlock,
replace the policy at its original scope with explicit consent. A narrower scope
cannot override a broader lock, exclusion or ceiling.

`/ore-model-router <JSON>` uses evaluate by default. Input requires source
`explicit-user-or-host`, current provider/model_id/effort, session_id, an expiring
registry and the ten-dimension task_profile. Optional selection_scope, department,
estimated_tokens, complete overheads, reported_cost, failure_cause, attempts, history,
subagents_used and escalation_evidence refine a decision. The mod replaces the supplied
session_id with the actual host ID. Python callers must obtain it from a trusted host.

`model-decision` uses the same payload, confirmation and revision checks to save
allowlisted metadata. It records a recommendation, never an applied model switch.
The standalone state CLI uses existing `runtime` flags (`--repo`, `--task-id`,
`--expect-revision`, `--mod`, `--action`, `--payload`, `--confirmed`,
`--expect-governance-revision`); no new invented executable is required.

## Approval and effective model

Construct an existing `ore-approval-ledger` approval using the operation hash returned
by `ore_models.operation(configuration)`, environment `host:selection_scope`, and
scope `task:<id>`, `session:<actual-id>` or `project`. Keep owner, explicit evidence
and expiry. The ledger's existing UI asks before persistence. Revocation uses its
`revoke-approval` action. Reject/keep current makes no grant; if a grant already exists,
explicitly revoke it. Persistent policies and approvals are separate: a profile or
policy never grants model switching by itself.

For this alpha, manually select an approved configuration in the host. Claude's
`/model` and `/effort` are host controls, not actions performed by the ORE command.
Check `/ore-model-router-status` for the observed main model and native usage; use
Claude `/tasks` to inspect subagent substitution. Observed effort remains unknown
when the host does not expose it to the diagnostic. Codex/ChatGPT require their own
host observation. Do not call a requested or recommended value effective.

## Acceptance and limitations

Inventory and offline contracts pass. Native launch is not established: installed
Claude Code 2.1.267 is below the required 2.1.287; the TypeScript contract is 2.1.295.
No account credentials or provider inference were used. No paid benchmark, model
switch, global config change, release, tag, push or marketplace installation occurred.

The candidate remains **4.2.0-alpha.1**, with incomplete overall acceptance for the
master request: real install/launch, supported native switching, observed subagent
execution, one-use authorization, organization policy ingestion, calibrated success
rates, cross-model measured benchmarks and acceptance certification remain pending.
AUTHORIZED_AUTO is metadata lookup only, not an autonomous execution claim.

Offline regression includes existing browser, runtime, state, flow and regulatory
tests plus routing tests for availability/restrictions, host fallback, expiry/revocation,
locks, project/scope isolation, corruption, consent, budgets, context/environment
diagnosis, retry cycles, authoritative gates and secrets. Independent code review found
and prompted fixes for task requirement preservation, session binding, concrete scope
confirmation and malformed delegation/state validation. It is not a provider evaluation.

The benchmark methodology defines fixed/adaptive/escalating strategies over ten work
categories. Synthetic tests are not production results. Measured token savings: unknown.

## Sources

Official host guidance was fetched on 2026-10-09:
[Claude models](https://code.claude.com/docs/en/model-config),
[Claude subagents](https://code.claude.com/docs/en/sub-agents),
[Codex configuration](https://developers.openai.com/codex/config-reference),
[Codex subagents](https://developers.openai.com/codex/multi-agent).
See the skill's references for the maintained registry, consent and benchmark contracts.
