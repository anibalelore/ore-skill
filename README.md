# ORE — Orchestrated Runtime Engineering

> Durable state, visible progress, the right specialists, and evidence before completion.

ORE is an installable company of Agent Skills for substantial product and software work. Version 2.2 combines repository-backed state, computed progress and 23 externally researched specialists organized into accountable departments.

## What is now enforceable

- **Cross-window continuation:** ORE writes `.ore/active.json`, task state and a resumption handoff. Another ORE-enabled window in the same workspace reloads it before planning.
- **Automatic percentage:** explicit ORE work reports evidence-based progress without the user asking. The percentage is computed from persisted weighted deliverables.
- **Concurrency protection:** state writes can require the last observed revision so a stale window cannot silently overwrite a newer one.
- **Form quality:** material forms require an authoritative field contract and tests for semantics, validation, reference lists, roles, accessibility, drafts and idempotency.
- **Department routing:** ORE selects accountable specialists across product, experience, application engineering, AI/data, integration quality, security/governance, platform/operations and code health.
- **Change-impact protection:** cross-module changes require a blast-radius map, affected-consumer verification and appropriately widened tests before completion.
- **Evidence gates:** completion is blocked by unfinished deliverables, unresolved blockers or required gates without evidence.

The persistence guarantee applies only when windows share the same repository storage and load ORE. ORE does not claim invisible global memory across unrelated clients or workspaces.

## Agent departments

### Executive orchestration and product

| Agent | Responsibility |
| --- | --- |
| `$ore` | Accountable orchestration, durable progress, routing, gates and integration |
| `$ore-product-discovery` | User problems, assumptions, prototypes, outcomes and controlled experiments |
| `$ore-product-architecture` | Specification, repository archaeology, domain modeling and architecture decisions |

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

ORE favors official platform documentation and curated open-source references. See `skills/ore/references/ecosystem-sources.md`, `skills/ore/references/legacy-agent-study.md` and `skills/ore/references/department-agent-study.md`. Repositories are not bundled or silently installed; license, version, attribution and ORE evaluations must be checked before adoption.

For SEO/GEO/AEO, ORE improves eligibility, comprehension, authority, answerability and measurement. It never guarantees a ranking or recommendation by Google or an AI system.

## Safety and privacy

ORE operates within host permissions. Repository-edit authorization does not authorize production deployment, destructive data changes, credential rotation, publication, external communication or spending. High-impact boundaries still require explicit approval.

Licensed under Apache-2.0.
