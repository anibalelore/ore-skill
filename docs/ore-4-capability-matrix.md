# ORE 4 capability audit

This is a requirements and dependency map, not a completion certificate. The
audited baseline is ORE 3.0.0: 26 skills, six independent TypeScript mods,
schema-v1 durable tasks, and a revision-protected Python writer. Implementation
and test results belong in the update report and individual mod documentation.

## Verified host contract

The source of truth is the generated, unedited Claude Code 2.1.295 snapshot in
`mods/api-types/claude-code/index.d.ts`, with built-in tool inputs in the adjacent
`claude-code-tools` snapshot. Runtime compatibility must be checked again after
an upgrade. `/plugin-types` was rejected in the baseline; interactive mod loading
generated the snapshot. An event appearing in a design does not create a native
host event.

Verified baseline events: `session.start`, `session.end`, `ui.render`,
`command.run`, `tool.call`, and `turn.complete`. The declarations also expose
`agent.spawn`, `session.compact`, `process.spawn`, and prompt events; their
presence alone does not prove a new integration works. Verified methods relevant
to extension include `command.register`, `fs.read`, `fs.list`, `fs.stat`,
`session.cwd`, `session.usage`, `process.run`, `agent.spawn`, `agent.list`,
`clock.every`, `ui.ask`, `ui.log`, `ui.resolve`, and `ui.invalidate`.

There is no browser automation adapter in these declarations. An independently
authorized browser/Playwright adapter is required. Agent-spawn completion is
asynchronous: the spawn result is an identity, and `turn.complete` carries the
answer. Do not mistake a spawn acknowledgement for a review result.

## Original mods: preserve behavior

| Mod | Existing responsibility | Native integration | Minimum calls / proof |
| --- | --- | --- | --- |
| ore-progress | Weighted progress and next deliverable | session.start/end; ui.render; command.run | Read state; timer and UI; Python-equivalent rounding and completed-task display |
| ore-guard | Confirm configured high-impact tool calls | session.start; tool.call; command.run | Read state; ui.ask; cancellation, native permission continuation, unchanged revision |
| ore-resume | Persisted handoff at startup | session.start; command.run | Read state; ui.log; active-task-only summary |
| ore-gates | Pending gates/blockers and completion warning | session.start/end; ui.render; turn.complete; tool.call; command.run | Read state; timer/UI; writer still blocks invalid closure |
| ore-stale-window | Warn on observed revision changes | session.start/end; ui.render; command.run | Read state; timer/UI; no assertion about which window wrote |
| ore-departments | Persisted assignment and recent specialists | session.start/end; ui.render; command.run | Read state; timer/UI; legacy records show ORE lead |

The original reader performs pointer/task/pointer reads. This catches a changed
task ID, but is not a transaction for same-task revisions. Governance decisions
must re-read and require the same task ID and revision at execution.

## Requested additions: gaps and acceptance dependencies

`command.run` means an explicit typed command, not autonomous invocation or a
claim that the entire requested behavior has been delivered. Persistent writes
must go through `ore_state.py`, with task ID and expected revision. Pure engines
may analyze explicit input without host or filesystem permissions.

| Mod | Reuse existing skills / modules | Real integration candidate | Gap and minimum dependency | Required proof |
| --- | --- | --- | --- | --- |
| ore-never-again | organizational-memory; guard; gates | command.run; tool.call | Approved project-scoped rules, conflicts, exceptions, revisions; writer bridge only for explicit mutations | Rule approval/revocation/replacement, restart recovery, scope violation, no transcript storage |
| ore-first-contact | quality-engineering; form-workflows; product-discovery | command.run plus external browser adapter | Synthetic accounts, isolated browser context, visible UI only, bounded exploration and replay | Real UI interaction; denied unsafe destinations; redacted evidence; absent adapter reported |
| ore-flow-intelligence | business-lifecycle; backend-data; form-workflows; change-impact | command.run; pure contract engine | Evidence-classified graph, distinct entity IDs, handoff contracts, continuity evidence | Factory and marketplace synthetic journeys, partial operations, retries, denied permissions |
| ore-flow-watch | business-lifecycle; data-analytics; delivery-operations | command.run; optional bounded polling | Authorized observation source, clock, idempotent alerts; no automatic production repair | Missing source reports disconnected; stalled/duplicate/orphan/SLA evidence; deduplication |
| ore-scope-lock | change-impact; guard; product-architecture | tool.call; command.run | Canonical workspace paths and approved scope; post-diff review for opaque tools | Traversal, symlink, case/drive alias, new-file parent, Bash limitation and state-race tests |
| ore-autopilot | core execution loop; quality-engineering | command.run; optional turn.complete | Explicit bounded iteration and resource budget, checkpoint and stop policy | Five-iteration ceiling; no-progress stop; critical-action confirmation; no background infinite loop |
| ore-worktree-manager | delivery-operations; developer-experience | command.run; process.run when opted in | Git argument-vector adapter, ownership and recovery | Independent worktrees, conflict detection, preservation of dirty/unowned trees |
| ore-smart-tests | quality-engineering; change-impact | command.run; pure selection engine | Explicit test dependency graph and critical set | Unknown coverage selects broad suite; critical tests retained; changed dependency invalidates evidence |
| ore-visual-qa | creative-web; web-engineering; mobile-design | command.run plus browser adapter | Viewports, screenshot evidence, accessibility and functioning checks | Real before/after artifacts; distinguish observed defect and aesthetic preference |
| ore-context-sentinel | context-efficiency; durable state; resume | command.run; session.compact only if verified | Checkpoint recovery; optional session.usage without fabricated counts | Missing/stale checkpoint; exact revision resume; estimates explicitly labeled |
| ore-independent-review | quality-engineering; release-certification; security-privacy | command.run; agent.spawn/turn.complete if implemented | Separate reviewer context, bounded completion and evidence | Actual independent agent or declared isolation limitation; spawn acknowledgement never passes gate |
| ore-contract-watch | backend-data; change-impact; product-architecture | command.run; pure contract comparison | Versioned contracts, consumer ownership, compatibility evidence | Additive/breaking changes and unknown consumers require suitable tests |
| ore-approval-ledger | security-privacy; compliance-governance; guard | command.run; tool.call | Exact operation/environment/scope/expiry/revocation, explicit approval | No native privilege bypass; mismatched/expired/revoked approval denied; race recheck |
| ore-pr-pilot | delivery-operations; release-certification | command.run; read-only Git adapter optional | Local PR evidence assembly; publication requires separate authorization | Accurate diff/tests/risks; no push, PR creation, merge or publication by local preparation |
| ore-preview-certifier | quality-engineering; release-certification | command.run plus browser adapter | Explicit preview origin and synthetic smoke scenarios | Real preview checks; no implicit production authorization |
| ore-runtime-diagnostics | delivery-operations; data-analytics; backend-data | command.run; pure evidence analysis | Authorized redacted observations, provenance and bounded input | Evidence linked to findings; uncertainty shown; no fabricated causality |
| ore-cost-controller | context-efficiency; core reporting | command.run; session.usage optional | Measured counters or labeled estimates; configurable budget | Missing counters remain unknown; no silent model/effort downgrade; comparable benchmark |
| ore-project-router | core routing; product-architecture | command.run; bounded fs.read/list optional | Project fingerprint, scoped conventions and skills | Cross-project rule isolation; load only relevant skills; ambiguity shown |
| ore-learning-lab | organizational-memory; AI-engineering; quality-engineering | command.run; pure evaluation engine | Comparable results, regression fixtures, approval and rollback | Same acceptance criteria across strategies; global policy unchanged without approval |

## Implementation checkpoint: prerelease scope

This checkpoint distinguishes native command integration from full requirement
completion. Nineteen new plugin adapters expose explicit commands through the
generated native API. They invoke packaged Python contracts or read-only host
diagnostics. Installation/type validation and commands are not autonomous agent
turns, independent review execution or production observability.

| Component group | Executable scope | Remaining requirement / status |
| --- | --- | --- |
| Scope Lock, Never Again, Approval Ledger | Revision-controlled project governance, task-bound approval metadata, durable rules/approvals/exceptions; declared Write/Edit interception with confirmation recheck | Partial: opaque tools and functional scope need diff review; approvals are records, not native permissions or universal enforcement |
| Autopilot | Bounded controller result for 1..5 supplied steps | Partial: never executes model turns, tests or repairs autonomously |
| Flow Intelligence, Flow Watch | Supplied typed flow-contract and observation analysis, synthetic factory/marketplace fixtures | Partial: no automatic application discovery, live telemetry connection or application E2E certification |
| First Contact | Real bounded Playwright exploration of an explicitly isolated loopback fixture; synthetic browser demo executed | Limited: deterministic visible-name heuristic, operator-trusted backend isolation, no staging/production adapter or human usability equivalence |
| Visual QA, Preview Certifier | Imported observation summaries and browser-readiness contract | Partial: no native screenshot comparison, automatic visual inspection or executed preview certification |
| Smart Tests, Contract Watch | Supplied test-map selection including critical tests, required broad-suite availability, and contract comparison | Partial: do not discover dependency graphs or execute selected tests |
| Context Sentinel, Cost Controller | Actual host usage query and persisted task handoff | Limited: no automatic checkpoint creation, context-loss recovery certification or demonstrated savings |
| Independent Review | Supplied immutable candidate/reviewer/evidence record | Partial: no native independent agent spawn/result integration |
| Worktree Manager | Read-only `git worktree list --porcelain` topology | Partial: no creation, concurrent ownership, integration or conflict resolution |
| PR Pilot | Local persisted-task PR-description preparation | Partial: no verified full diff/test assembly or external publication |
| Runtime Diagnostics | Supplied observations with evidence and unverified cause | Partial: no direct log/trace/metric collectors or executed incident recovery |
| Project Router | Read-only discovery of recognized root manifests | Partial: no stack-version resolution, convention inference or automatic specialist routing |
| Learning Lab | Supplied comparable-result analysis accepting measured-host/provider-usage sources for demonstrated savings | Limited: no benchmark execution or policy promotion; supplied provenance and environment must be independently verified |

State mutations remain in `ore_state.py`. Read-only evaluation neither creates
`.ore/` nor uses a creating repository lock. Browser evidence stays outside
`.ore/` unless explicitly imported through the state authority. The loopback
adapter blocks off-origin requests and restricts HTTP methods, but this does not
prove that a local GET handler cannot cause production effects. Operators must
provide an isolated synthetic backend; these restrictions are not a sandbox.

## Shared boundaries (required hardening)

- Package shared pure contracts inside each plugin; cross-plugin relative imports
  do not work reliably under the host's plugin-root import restriction.
- An internal event envelope needs schema version, source, correlation ID,
  permissions and redaction policy. It is not a native event, and polling a state
  record is not an event bus. Durable publication stays with the Python writer.
- Filesystem and process access are user-level execution with no sandbox.
  Limit call sites and inputs; do not market declared permissions as OS isolation.
- No state means original mods are inert. Malformed optional governance disables
  that optional layer; writer evaluation returns `enabled: false`. This is safe
  session degradation, not proof that configured scope remained enforced.
  Once valid governance is loaded, runtime enforcement errors deny the edit.
  Disabled governance must never be reported as an approval or passed gate.
- Hash-bound, current evidence is needed for a business continuity gate. A
  free-form string saying a test passed is not proof that records flowed.
- A warning hook is advisory; opaque shell scripts, remote actions, external
  tools and files changed outside Claude can evade a path-based interception.
- Repeated polling should be bounded and cancel on exit. Shared SDK packaging
  must not introduce runtime coupling or resident services for small tasks.

## Baseline writer review

The writer serializes read-check-write on Windows/POSIX and replaces task JSON
atomically. Expected revisions are mandatory for update/checkpoint/complete.
Task, active pointer and handoff are separate files, so they are not one atomic
transaction. Errors after task replacement can leave a stale handoff; task JSON
is authoritative. Root JSON type and nested optional fields need validation
before mutation. Approval facts must not be inferred from text or user-provided
booleans without an explicit authorization boundary. A completed task can still
receive updates in the baseline: governance lifecycle tests must define whether
this is allowed and must never silently reuse a completed task's approval.

Stable ORE 4.0.0 requires the requested executable behaviors and acceptance
evidence. Partial engines, missing browser execution, unimplemented adapters or
manual integrations require a prerelease and a candid inventory.

## ORE 4.1 additive regulatory roadmap

Both regulatory adapters are implemented offline artifact evaluators using the audited SDK and shared writer. Signature patterns and flow preconditions are executable; production authentication, atomic record/audit storage, tamper resistance, scanner/IdP integrations and complete transition coverage remain host-specific acceptance work. Preserve every existing 4.0 item and original mod. Stable release additionally requires applicability-owner review and application executions for all regulatory scenarios. See [extension report](ore-4.1-regulatory.md).

## ORE 4.2 model routing extension

`ore-model-router` adds native model/usage diagnostics and pure routing/consent
contracts. `ore-adaptive-model-routing` joins the existing AI/data department.
Live execution adapters remain experimental; manual fallback preserves the current
configuration. See [4.2 compatibility and acceptance](ore-4.2-adaptive-routing.md).
