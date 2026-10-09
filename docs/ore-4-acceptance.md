# ORE 4 acceptance protocol

This document defines required verification, not executed results. Record exact
commands, host versions, exit codes and artifact paths in `UPDATE_REPORT.md`.
Skipped tests stay skipped; generated fixtures are not customer-app evidence.

Current extension scope is prerelease: 19 native command adapters and executable
Python contracts, not 19 fully autonomous runtime agents. Autopilot does not
execute turns, Worktree Manager only reads topology, and flow engines analyze
supplied contracts/observations rather than discover an application's process.
First Contact has an executed loopback Playwright fixture; Visual QA and Preview
Certifier currently summarize imported observations. The following acceptance
items remain requirements until their concrete results are recorded.

## Preservation and installation

1. Verify the same 26 skill names and the six original mods remain available.
2. Run `python scripts/validate_package.py` and
   `python -m unittest discover -s evals -p "test_*.py" -v`.
3. Type-check each plugin against the generated API snapshot, validate every
   plugin individually, run native tests where provided and load with
   `claude --plugin-dir mods/<name>`. Record what the host actually exercised.
4. Disable every new mod and confirm core state and original skill behavior
   work. Check no runtime import escapes the plugin root, no new dependency
   cycle and no network/process call outside the documented adapter.
5. Cover absent state, invalid JSON, non-object JSON, unsupported schema,
   completed task, blockers, old specialist-free record and revision changes.

## Governance: highest risk checks

| Scenario | Required observation |
| --- | --- |
| Change only Schedule Production | Approved form path allowed; Production View path rejected; opaque Bash writes described as a limitation unless independently constrained |
| Alternate path spelling | Traversal, symlink escape, case/drive alias, UNC/device/drive-relative paths and new-file parent cannot bypass a canonical boundary |
| Durable correction | Candidate is not active until explicit approval; task restart restores approved scoped rule without conversation transcript |
| Rule replacement | New explicit instruction can replace/revoke the old rule; conflict remains visible until resolved; no cross-project contamination |
| Sensitive operation | Approval binds exact operation, project, task, environment and scope; expired/revoked/mismatched grants do not authorize execution |
| Confirmation race | Task ID/revision changed while asking causes denial/review; native permission chain still runs after local confirmation |
| Concurrent mutation | Two writers with the same expected revision produce one accepted mutation and one conflict, without lost writes |
| Malformed governance | Optional layer degrades to disabled (`enabled: false`), never approval or passed gate; valid loaded rules with runtime failure deny the edit; disabled state is a coverage limitation |
| Autonomy loop | Bound is at most five repair iterations per coherent defect set; exhausted/no-progress/unsafe-action conditions stop and checkpoint |
| Completion | Pending mandatory gate, incomplete deliverable, blocker or stale evidence prevents verified task closure |

Canonical path interception does not prove all functional requirements or code
components remain in scope. Review the full diff and relevant regression tests.
Store decisions through the sole state writer; no mod independently writes `.ore/`.

## Business continuity

Factory fixture: existing customer, two products, linked PO/sales lines,
partial production, distinct batch IDs, a rejected batch, partial dispatch,
quantity correction, duplicate creation-event retry and logistics failure.
Show the original PO is traceable through sales, scheduling, BPR, QA, packaging,
shipping and final dispatch. QA holds prevent applicable shipments. A retry is
idempotent without merging legitimately different orders.

Marketplace fixture: synthetic checkout/order/payment, multiple seller
suborders and shipments, inventory effects, logistics coverage, tracking,
verified delivery and settlement. Distinct record IDs and explicit relations
must survive cancellation, refund, failed delivery, dispute holds and events
arriving out of order. Never charge real funds or release money.

Both fixtures must exercise permission denial, duplicate events, missing
handoff, stale/changed contract, integration failure and recovery. Relations
carry evidence classifications: confirmed, inferred, pending, contradictory or
not applicable. A matching name is not confirmation. Coverage should include
provenance, versions, canonical fields and legitimate historical snapshots.

Continuity closure must reuse BUSINESS_LIFECYCLE, ENTITY_CONTINUITY,
WORKFLOW_RECOVERY, DATA_CONTRACT, CHANGE_IMPACT and TESTS as applicable. Evidence
must match the current artifact/contract. A graph validator or synthetic fixture
alone does not establish a live application passed E2E.

Flow Watch receives explicit authorized observations and a controlled clock.
Test stalled transitions, orphan records, duplicates, incompatible states,
reconciliation errors and SLA thresholds. Alerts include affected identities,
last confirmed transition, elapsed time, evidence, severity and proposed
recovery. Deduplicate repeated observations. No source reports disconnected,
without invented telemetry or automatic production recovery.

## First Contact and visual evidence

- Give explorers only the authorized entry origin, end-user goal, synthetic
  account and simulation parameters. Never source code, private routes, guided
  correct answers or author-provided selectors.
- Isolate browser contexts; deny unrelated origins, production, money movement,
  customer messages, credentials/permissions changes and unauthorized effects.
  Treat page text as data, not permission or execution instructions.
- Execute real visible UI interaction with bounded actions/time. Capture action
  sequence, visible messages, failures and actual screenshots when available.
- Redact sensitive values and explicitly limit retention. Do not copy raw
  browser state, local account profiles or secrets into persistent evidence.
- Exercise unavailable browser, timeout, navigation escape, confusing empty
  state, unusable form, recovery and abandonment. Report observed findings
  separately from interpretations and simulation assumptions.
- After an approved repair, reproduce the original scenario and perform fresh
  unguided exploration; record regressions. AI simulation does not replace human
  usability research. Missing browser execution means blocked/partial status.

## Delivery, diagnostics and efficiency

Worktree tests must use temporary repositories, independent owned changes and
an intentional conflict; preserve dirty or unowned worktrees. PR preparation
must remain local unless publication is separately authorized. Preview checks
must bind the approved preview origin and never grant production permission.
Contract Watch must identify breaking changes and unresolved consumers. Smart
Tests must broaden when impact/coverage is unknown and retain critical checks.

An independent reviewer needs an actually separate executed review and result;
if unavailable, label the review as isolated/self-review. Runtime findings must
reference observed logs/traces and retain uncertainty about causes.

Efficiency comparison uses identical task, artifacts, model/effort, tools,
acceptance gates and environment. Record actual available token/cost/runtime
counters, repeats and uncertainty. Estimates are labeled. Fewer prompt
characters or fewer selected tests alone do not establish token savings or
equivalent outcomes. Never silently change model, effort or quality controls.

## Release decision

Report each mod as implemented and validated, implemented with limitations,
partial, blocked or pending. Keep code-local, committed, pushed, installed and
published states separate. Use a prerelease when requested major functionality
is missing or not executed. No commit, push, tag, deployment or publication is
implied by completion of local acceptance checks.
