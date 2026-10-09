# ORE 4 runtime adapters

**Prerelease candidate: 4.2.1-alpha.1.** All 22 additions are explicit command adapters,
not a certificate that the complete ORE 4 autonomous system is implemented.
The six ORE 3 display/guard mods retain their optional lifecycle. Guard presentation
uses the shared [4.2.1 approval experience](ore-4.2.1-approval-experience.md), as do
ledger, routing and scoped-review dialogs. Native permissions remain intact.

| Adapter | Executable behavior | Current limit |
| --- | --- | --- |
| ore-model-router | Observe main model/native usage; evaluate supplied routing; confirm scoped metadata using shared writer | Manual selection; no live verified switching or guaranteed savings; see [4.2 guide](ore-4.2-adaptive-routing.md) |
| ore-never-again | Confirm, persist, replace and revoke scoped path rules; intercept Write/Edit | Corrections must be supplied explicitly; shell commands and semantic policies are not enforced |
| ore-scope-lock | Confirm allow-list scopes and expiring exceptions; resolve actual filesystem paths | Write/Edit only; filesystem changes between review and execution remain possible |
| ore-approval-ledger | Confirm scoped approvals with owner, evidence and expiry; list active records | Records never grant native permissions or automatically approve a tool |
| ore-first-contact | Validate isolated scenarios, prepare, summarize or run a bounded loopback browser session; optionally export masked synthetic screenshots | Required Playwright and Chromium; deterministic exploration; no video or mutation requests |
| ore-flow-intelligence | Validate supplied identities, relationships, transitions, provenance and execution records | No automatic application discovery; passing a model is not application certification |
| ore-flow-watch | Analyze supplied authorized telemetry for evidence-backed alerts | Disconnected without telemetry; no live subscription or repair |
| ore-autopilot | Validate an explicit plan and compute the remaining maximum-five-step budget | Does not execute model turns; attempts are caller-supplied |
| ore-worktree-manager | Read actual Git worktree topology | Does not create, merge or delete worktrees |
| ore-smart-tests | Select tests from an explicit path map; require broad fallback for unknown coverage | No dependency discovery or test execution |
| ore-visual-qa | Prepare a scenario or summarize observed browser evidence | No pixel comparison, full accessibility audit or semantic visual certification |
| ore-context-sentinel | Show persisted handoff and native session usage | No compaction interception, checkpoint or context rewrite |
| ore-independent-review | Validate a declared distinct reviewer, immutable candidate and evidence | Does not spawn/authenticate a reviewer; records do not authorize promotion |
| ore-contract-watch | Compare explicit before/after structural contracts and affected consumers | No automatic extraction or live watching |
| ore-pr-pilot | Generate a local draft from recorded task validation and blockers | No commit, push, pull request creation or publication |
| ore-preview-certifier | Prepare or summarize supplied exploration evidence | Does not deploy previews or certify a release |
| ore-runtime-diagnostics | Summarize evidence-backed error observations | No automatic source connection, causal proof or repair |
| ore-cost-controller | Read native context, rate-limit and cost figures | No model downgrade, hard spend cap or unsupported counters |
| ore-project-router | Read known project manifest presence | Reports observations; does not automatically assign specialists |
| ore-signature-guard | Verify supplied FDA applicability, signed records and file-bound executed checks | Offline evaluator; trusted identity/storage adapters remain application-specific |
| ore-safeguards-monitor | Verify supplied FTC scope and control evidence; assess incident candidates | No live scanner/IdP connection or automatic legal notification |
| ore-learning-lab | Compare supplied runs with matching task/model/settings/gates and full counters | No synthetic savings claims or automatic policy changes; counters are declared evidence |

## Installation and commands

Use Claude Code **2.1.287+**. The generated **2.1.295** API declarations are the
contract used by this implementation. From the repository clone:

```text
/plugin marketplace add ./mods
/plugin install ore-flow-intelligence@ore-mods
```

Any plugin can be tried with `claude --plugin-dir mods/<name>`. Invoke
`/<name>-status` for persisted task state or `/<name> <JSON>` for an explicit
operation. These commands do not ask a model to infer input from conversation.
They require an active, valid ORE task. Missing/corrupt task state is inert.

Read-only flow analysis takes the complete actual document as its JSON payload.
For complete runnable documents, use the Python commands below; shell file
expansion is deliberately absent from plugin commands:

```text
python skills/ore/scripts/ore_flow.py analyze evals/fixtures/flows/factory.json
python skills/ore/scripts/ore_flow.py analyze evals/fixtures/flows/marketplace.json
python skills/ore/scripts/ore_first_contact.py demo
```

To propose a durable rule in Claude (the UI asks before saving):

```text
/ore-never-again {"action":"rule","governanceRevision":0,"payload":{"id":"protect-generated","description":"Do not edit generated files","paths":["generated/*"],"owner":"project owner","evidence":"explicit project decision","kind":"forbid-paths"}}
```

Use the current governance revision for every subsequent write. Replacing a
rule requires a new id and `replaces` naming the previous active rule. Exceptions
require an eligible rule, exact path and future `expires_at`; approvals require
operation, scope, environment, owner, evidence and expiry. Revocations are
explicit. Approval records never override Claude permissions or ore-guard.

An isolated browser operation additionally asks for permission:

```text
/ore-first-contact {"payload":{"run_browser":true,"scenario":{"url":"http://127.0.0.1:8080","goal":"Find support","environment":"isolated_test","isolated_environment_confirmed":true,"synthetic_accounts_confirmed":true,"authorized":true},"success_visible":"Support available"}}
```

`success_visible` belongs to the independent outcome evaluator; it is never
provided to action selection. Operator isolation assertions require truthful
input. Read the [browser contract](first-contact.md) before running an app.

## Permissions and persistence

**Mods run as the user and have no sandbox.** New runtime adapters need
`process.run` to invoke their bundled, audited Python tools. This is necessary
for sharing the single state writer and executing browser adapters; no shell
strings, arbitrary command execution, model calls or network API are used.
Worktree topology uses the fixed read-only `git worktree list --porcelain`
command. Browser exploration starts Chromium and makes only authorized same-origin
loopback GET/HEAD requests. Python, required Playwright and Chromium must be installed
separately; nothing installs them automatically. `pythonCommand` can select a
trusted interpreter executable.

Cost/context/project adapters are process-free. Screenshot export is opt-in,
requires explicit synthetic-screen approval and writes outside `.ore/`; its
retention is at most 24 hours, with scoped cleanup of only owned expired artifacts.
Pixel masking is not a general guarantee of personal-data removal. Never include
secrets in rule descriptions, owners or evidence. Display masking is best effort.

Only bundled copies of `ore_state.py` write `.ore/governance.json`. The copies
must match the canonical writer byte-for-byte; package validation checks this.
Governance uses the existing cross-process lock, project identity and expected
task/governance revisions. Internal versioned governance events are persisted
records, **not invented Claude events**. They contain record references rather
than conversation text. The read-only engines never write state. Governance
evaluation uses filesystem-resolved paths; hard-link aliases and TOCTOU races
are not solved. Missing/corrupt governance is inert; a valid rule whose runtime
cannot execute blocks the declared edit rather than silently skipping enforcement.

No extra persistent UI banners are installed by these 19 adapters. Use the
original progress/gates/departments band and explicit commands when relevant.

## Development

Edit `mods/sdk/register.ts` or canonical Python scripts, then run
`python scripts/build_mods.py`. Build copies remain self-contained for `/plugin`
installation. Run package, Python, TypeScript and native Claude validation.
The [capability matrix](ore-4-capability-matrix.md) and
[acceptance contract](ore-4-acceptance.md) track remaining certification work.

## Regulatory runtime additions (4.1)

`ore-signature-guard` and `ore-safeguards-monitor` accept `{"contract":"evidence/domain.json"}` through the same command/runtime API. They verify offline, authorized evidence and emit owned findings and gate results. They do not sign into IdPs, run remote scanners or notify agencies. Gate persistence uses the existing writer and requires reevaluation. See [contracts and roadmap](ore-4.1-regulatory.md).
