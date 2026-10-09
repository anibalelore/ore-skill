# ORE — Orchestrated Runtime Engineering

> Durable state, visible progress, the right specialists, and evidence before completion.

ORE is an installable company of Agent Skills for substantial product and software work. Version 3.0 preserves the existing 26 skills and adds six optional Claude Code mods for visible state and per-action confirmation.

## Claude Code mods (optional)

Requires Claude Code CLI **2.1.287+**; tested with **2.1.295**. ORE skills work
unchanged in Codex and other hosts without these plugins.

| Mod | Behavior |
| --- | --- |
| `ore-progress` | Shows the persisted task, computed percentage and current/next deliverable above the prompt. |
| `ore-guard` | Confirms configurable high-impact tool actions, showing task context and declared arguments. |
| `ore-resume` | Prints the active task's objective, progress, next deliverable and blockers on session start. |
| `ore-gates` | Shows pending required gates/blockers and warns at turn end or an explicit completion command. |
| `ore-stale-window` | Warns when an observed task/revision changes; it cannot identify which window wrote it. |
| `ore-departments` | Shows recorded department, command chain and recent specialists; old state shows only `ORE lead`. |

From a local clone, add its `mods` directory as a marketplace, then install
each desired plugin:

```text
/plugin marketplace add ./mods
/plugin install ore-progress@ore-mods
/plugin install ore-guard@ore-mods
/plugin install ore-resume@ore-mods
/plugin install ore-gates@ore-mods
/plugin install ore-stale-window@ore-mods
/plugin install ore-departments@ore-mods
```

Or try one session with `claude --plugin-dir mods/ore-progress` (substitute any
of the six names). Use `/reload-plugins` after installing in an open session.
Keep the clone in place when using the local marketplace. Nothing is published
by these instructions.

**Mods run with your user permissions and have no sandbox.** These six mods
request only file reads, timers, UI and status commands; they never write
`.ore/`, access the network or start external processes. Missing/corrupt state
is ignored. Updates are polled every second. Only terminal/Desktop show the
band; `/<plugin-name>-status` provides an explicit textual handoff elsewhere.

The guard is pattern-based, cannot measure remote effects or hidden scripts,
and does not bypass host permissions after confirmation. Gates never infer
completion claims from conversation text. Specialist identity must be recorded
through the optional `ore_state.py update` arguments. See
[mod options, state contract, API provenance and validation](mods/README.md).

## What is now enforceable

- **Cross-window continuation:** ORE writes `.ore/active.json`, task state and a resumption handoff. Another ORE-enabled window in the same workspace reloads it before planning.
- **Automatic percentage:** explicit ORE work reports evidence-based progress without the user asking. The percentage is computed from persisted weighted deliverables.
- **Concurrency protection:** state writes can require the last observed revision so a stale window cannot silently overwrite a newer one.
- **Form quality:** material forms require an authoritative field contract and tests for semantics, validation, reference lists, roles, accessibility, drafts and idempotency.
- **Department routing:** ORE selects accountable specialists across product, experience, application engineering, AI/data, integration quality, security/governance, platform/operations and code health.
- **Change-impact protection:** cross-module changes require a blast-radius map, affected-consumer verification and appropriately widened tests before completion.
- **Workflow continuity:** any entity or work item keeps canonical identity, field provenance and durable progress across modules instead of duplicating entry at every stage.
- **Governed memory:** project knowledge carries provenance, typed relationships, staleness and approval-based promotion rather than treating raw history as policy.
- **Context efficiency:** working sets are reduced only when the same evidence gates still pass; token savings are never invented.
- **Evidence gates:** completion is blocked by unfinished deliverables, unresolved blockers or required gates without evidence.

The persistence guarantee applies only when windows share the same repository storage and load ORE. ORE does not claim invisible global memory across unrelated clients or workspaces.

## Agent departments

ORE 3.0 uses a minimum sufficient execution policy: conditional reference
loading, scoped specialist assignments, incremental handoffs, concise evidence
returns and reuse of checks only while their candidate/inputs/environment remain
valid. Required gates and independent reviews are preserved. The user's chosen
model and reasoning settings remain unchanged; no automatic downgrade is used.
Actual billed-token savings and equivalent model outcomes require a comparable
end-to-end benchmark. Smaller instructions alone do not establish either.

### Executive orchestration and product

| Agent | Responsibility |
| --- | --- |
| `$ore` | Accountable orchestration, durable progress, routing, gates and integration |
| `$ore-product-discovery` | User problems, assumptions, prototypes, outcomes and controlled experiments |
| `$ore-product-architecture` | Specification, repository archaeology, domain modeling and architecture decisions |

### Business process and workflow continuity

| Agent | Responsibility |
| --- | --- |
| `$ore-business-lifecycle` | Canonical identity, data continuity, durable progress and reconciliation for any cross-module domain workflow |

### Experience, design and discovery

| Agent | Responsibility |
| --- | --- |
| `$ore-mobile-design` | Mobile product design, UI, UX, accessibility and design systems |
| `$ore-form-workflows` | Role-aware, validated, accessible and persistent data-entry workflows |
| `$ore-creative-web` | Scroll stories, motion, WebGL/3D and playful interaction |
| `$ore-search-discovery` | Technical SEO, information architecture, structured data, AEO/GEO and measurement |

### Application engineering

| Agent | Responsibility |
| --- | --- |
| `$ore-web-engineering` | Web architecture, frontend/full-stack implementation, quality and release |
| `$ore-android` | Native Kotlin/Compose Android engineering |
| `$ore-ios` | Native Swift/SwiftUI/UIKit engineering |
| `$ore-flutter` | Flutter/Dart engineering and native integration |
| `$ore-backend-data` | Transactional APIs, services, databases, messaging, integrations and migrations |

### AI, data and decision systems

| Agent | Responsibility |
| --- | --- |
| `$ore-ai-engineering` | ML/LLM/RAG/agent evaluation, safety, observability, latency and cost |
| `$ore-data-analytics` | Analytics events, metric contracts, transformations, data quality and lineage |

### Integration, quality and release assurance

| Agent | Responsibility |
| --- | --- |
| `$ore-change-impact` | Dependency blast radius, affected consumers, compatibility and cross-module regressions |
| `$ore-quality-engineering` | Risk-based testing, synthetic users, accessibility, localization, performance and resilience |
| `$ore-release-certification` | Independent verification of immutable candidates, provenance, gates, rollout and rollback |

### Security, privacy and governance

| Agent | Responsibility |
| --- | --- |
| `$ore-security-privacy` | Threat modeling, authorization, privacy and supply-chain security |
| `$ore-compliance-governance` | Framework scope, control mapping, evidence, exceptions and audit traceability |

### Platform, operations and developer productivity

| Agent | Responsibility |
| --- | --- |
| `$ore-platform-cloud` | Cloud infrastructure, IaC, internal platforms, identity, capacity, cost and disaster recovery |
| `$ore-delivery-operations` | CI/CD, observability, progressive release, rollback and incident response |
| `$ore-developer-experience` | Onboarding, reproducible environments, feedback loops, self-service and measured friction |

### Code health and organizational learning

| Agent | Responsibility |
| --- | --- |
| `$ore-code-health` | Maintainability, documentation, dependencies, root cause and recurrence prevention |
| `$ore-organizational-memory` | Project-scoped decisions, lessons, relationship graphs, promotion, staleness and forgetting |
| `$ore-context-efficiency` | Minimum sufficient context, filtered evidence and defensible token accounting |

ORE routes only the skills the task needs. The hierarchy is shallow: ORE lead → domain lead → bounded specialist. The ORE lead remains accountable for integration and overall progress.

## Install

### Codex CLI / coding agent

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
git clone https://github.com/anibalelore/ore-skill.git "$env:USERPROFILE\.codex\skills\ore"
```

Start a new session and invoke `$ore`.

### Plugin marketplace

```text
codex plugin marketplace add anibalelore/ore-skill
```

Restart the client, select **ORE Skills**, install **ORE**, and start a new conversation.

### Other Agent Skills hosts

Clone the repository where the host discovers Agent Skills. Direct-skill hosts read the root `SKILL.md`; plugin-aware hosts discover all folders under `skills/`.

## Example

```text
$ore Build the customer onboarding flow for Android, iOS and web. Persist the
workflow, show progress automatically, use the supplied industry list exactly,
and close accessibility, form, security and release gates with evidence.
```

## Integrated audit usage

Invoke `$ore` with `ORE audit`, `ORE security`, `ORE compliance`, `ORE accessibility`, `ORE fix`, `ORE loop` or `ORE report` in the request. These are natural-language capabilities, not new CLI commands. Audit/security/compliance/accessibility inspect and report by default; fix/loop authorize relevant repository repairs while preserving external-action boundaries. A strictly read-only audit creates no repository state or reports on disk.

The five capabilities share [29 original controls and seven advanced controls](skills/ore/references/audit-controls.md), [stack/business/jurisdiction playbooks](skills/ore/references/audit-stack-playbooks.md), and an [audit report contract](skills/ore/references/audit-report.md). Applicable checks also run proportionally when ORE develops forms, login, APIs, tables, payments, uploads, AI, subscriptions, interfaces or deployments. Looping stops after at most five iterations or earlier without verified progress. Applied changes remain unvalidated until affected retest and regression checks pass.

Example: `$ore ORE loop: audit this repository and repair confirmed security findings using local tests; keep production actions out of scope.` Legal applicability requires actual jurisdiction facts and current authoritative sources. Missing evidence remains pending; ORE does not claim complete security or legal certification.

For optional JSON evidence ledgers, run `python skills/ore/scripts/validate_audit_report.py <ledger.json>`. This validates coverage, status and evidence links; it does not scan an application. See [UPDATE_REPORT.md](UPDATE_REPORT.md) for this update's discovery, validation and remaining limits.

## Durable state lifecycle

ORE uses `skills/ore/scripts/ore_state.py`:

```text
python skills/ore/scripts/ore_state.py resume --repo .
python skills/ore/scripts/ore_state.py start --repo . --title "Feature" --objective "..." --kind general --acceptance "observable result" --deliverable "Baseline:10" --deliverable "Build:55" --deliverable "Verify:30" --deliverable "Handoff:5"
```

Writes use atomic replacement. Updates accept `--expect-revision` and reject stale writers. State contains no secrets by design; teams decide whether `.ore/` belongs in version control.

## Validation

```text
python -m unittest discover -s evals -p "test_*.py" -v
python scripts/validate_package.py
```

Behavioral scenarios live in `evals/behavioral-scenarios.md`. The package validator checks structure, references, versions and unfinished scaffolding; the state tests cover resume, computed progress, stale-window conflicts and completion blockers.

## External references

ORE favors official platform documentation and curated open-source references. See `skills/ore/references/ecosystem-sources.md`, `skills/ore/references/legacy-agent-study.md`, `skills/ore/references/department-agent-study.md` and `skills/ore/references/workflow-memory-study.md`. The latter documents the requested self-improving-agent, MemoryGraph, token-optimization and Graphify review plus durable-workflow references. Repositories are not bundled or silently installed; license, version, attribution, data boundaries and ORE evaluations must be checked before adoption.

For SEO/GEO/AEO, ORE improves eligibility, comprehension, authority, answerability and measurement. It never guarantees a ranking or recommendation by Google or an AI system.

## Safety and privacy

ORE operates within host permissions. Repository-edit authorization does not authorize production deployment, destructive data changes, credential rotation, publication, external communication or spending. High-impact boundaries still require explicit approval.

Licensed under Apache-2.0.
