# ORE ? Orchestrated Runtime Engineering

> Turn a complex request into accountable work, visible progress and verified results.

**ORE gives your coding agent an engineering team:** a lead, 27 specialists,
durable project state and evidence gates. Use it in Codex, Claude Code or another
Agent Skills host. **We now also have Claude Code mods** to make progress,
approvals, blockers and specialist activity visible in the harness.

| Core team | Optional runtime layer | Current release |
| --- | --- | --- |
| 28 skills across 9 departments | 6 established mods + 21 runtime adapters | **4.1.0-alpha.1 ? prerelease** |

**Start here:** [Install ORE](#install) ? [Try the mods](#claude-code-mods-optional) ?
[Meet the team](#agent-departments) ? [Update history](#update-history)

## How ORE helps

1. **Understand the outcome.** Define the deliverables, constraints and acceptance criteria.
2. **Bring in the right specialists.** Load relevant expertise and the context needed for the work.
3. **Keep work resumable.** Persist weighted progress, decisions, blockers and the next action in the repository.
4. **Verify before closing.** Require evidence for applicable gates and report anything still unresolved.

```text
$ore Build the customer onboarding flow. Show progress, keep the industry list
exactly as supplied, and verify forms, accessibility, permissions and recovery.
```

ORE uses focused context and incremental handoffs to reduce unnecessary token
use while retaining required results and evidence. **Model-specific token savings
have not been measured.** It does not promise identical performance across models.

## Claude Code mods (optional)

**Already available:** six mods introduced in ORE 3.0 improve visibility and
confirmation directly in Claude Code. Skills continue to work in other hosts.

| Mod | What you see or control |
| --- | --- |
| `ore-progress` | Active task, calculated progress and next deliverable |
| `ore-guard` | Confirmation for configurable high-impact tool actions |
| `ore-resume` | Objective, progress, next action and blockers at startup |
| `ore-gates` | Pending evidence gates and warnings at attempted completion |
| `ore-stale-window` | Warning when the observed task or revision changes |
| `ore-departments` | Recorded department, specialist and command chain |

**New in the ORE 4 prerelease:** 19 command adapters add confirmed living rules,
path scopes, an approval ledger, isolated browser exploration, flow contract
analysis, telemetry analysis and supporting review/delivery tools. They have
**different levels of completeness**: autopilot does not execute autonomous turns,
worktree management currently lists topology, and visual/preview tools do not
certify a release. Read the [adapter inventory and examples](docs/runtime-mods.md)
and [capability matrix](docs/ore-4-capability-matrix.md) before relying on them.

Requires **Claude Code 2.1.287+**; API validation uses **2.1.295**.
From a local clone:

```text
/plugin marketplace add ./mods
/plugin install ore-progress@ore-mods
/plugin install ore-guard@ore-mods
/plugin install ore-resume@ore-mods
/plugin install ore-gates@ore-mods
/plugin install ore-stale-window@ore-mods
/plugin install ore-departments@ore-mods
```

Install only the mods you need. To try one session:

```text
claude --plugin-dir mods/ore-progress
```

Use `/reload-plugins` after installation in an open session. Keep the local clone
in place. These instructions do not publish a package or change your installed skills.

**Mods run with your user permissions and have no sandbox.** The six established
mods only read state and use timers/UI; they do not start processes or access the
network. New adapters invoke bundled Python tools when needed; the worktree
adapter reads Git topology and optional browser exploration starts Chromium
against an explicitly authorized isolated loopback application. Only
`ore_state.py` writes `.ore/`. Missing/corrupt task state is ignored.

The existing display band updates every second in terminal/Desktop;
`/<name>-status` provides a textual handoff. Risk matching cannot inspect hidden
scripts or measure remote effects. Specialist identity comes from recorded state;
legacy tasks show `ORE lead`. See the [original mod contract](mods/README.md).

## ORE 4: what is verified today

- **Preserved foundation:** the existing skills, revision-protected writer and six established mods.
- **Governed rules:** explicit confirmation, project isolation, owners, evidence, replacement, expiry and revocation; declared Write/Edit paths can be restricted.
- **Business flows:** executable synthetic factory and marketplace models exercise identity, provenance, partial quantities, retries, cancellation and recovery.
- **First Contact:** a real Chromium test completes a goal in a local fixture using visible controls; unavailable browser dependencies return a blocked result.
- **Honest evidence:** model validation does not certify a live application. Telemetry tools report disconnected without input. Estimated counters cannot demonstrate token savings.

ORE 4 is a **prerelease**, because full autonomous orchestration, application
discovery, live telemetry subscriptions, visual certification and multi-host/model
certification remain unfinished. The [update report](UPDATE_REPORT.md) records
actual checks and limits; the [acceptance contract](docs/ore-4-acceptance.md) defines
what must pass before a stable 4.0.0 release.

## ORE 4.1 regulatory extension

Adds `ore-signature-guard` and `ore-safeguards-monitor` through the shared runtime, six evidence-backed regulatory gates and reusable signature/flow contracts. Preserves all ORE 4.0 roadmap items and original mods. See [implementation and limits](docs/ore-4.1-regulatory.md). Offline package validation does not certify customer systems.

## Update history

| Version | Main improvement |
| --- | --- |
| **4.1.0-alpha.1** | Regulatory skills, signature patterns, safeguards evidence and notification readiness |
| **4.0.0-alpha.1** | Runtime governance, 19 explicit adapters, synthetic business-flow engine and isolated browser exploration; certification in progress |
| **3.0.0** | Six optional Claude Code mods and focused execution/context policies |
| **2.4.0** | Integrated security, privacy, compliance and bounded audit/repair workflows |
| **2.3.0** | Business lifecycle continuity, governed memory and context efficiency |
| **2.2.0** | Department specialists and change-impact protection |
| **2.1.0** | Historical agent research and workflow hardening |
| **2.0.0** | Durable repository state, resumable work and domain specialists |
| **1.5.x** | Audit, continuous improvement, progress and token reporting |
| **1.4.0** | Continuous learning and failure intelligence |
| **1.2?1.3** | Workflow intelligence and iteration improvements |
| **1.0?1.1** | Initial ORE skill and early operating protocol |

See the [complete changelog](CHANGELOG.md) for individual changes. Prior release
reports remain in [UPDATE_REPORT.md](UPDATE_REPORT.md).

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
| `$ore-fda-part11` | Assessed Part 11 applicability, record controls and signature integrity |
| `$ore-ftc-safeguards` | Assessed Part 314 applicability, security evidence and incident readiness |

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

### Required browser runtime

Playwright and Chromium are required for First Contact and full validation. Run
these commands from the ORE repository or the installed `ore` skill directory,
using the Python interpreter configured for the runtime:

```text
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Python dependencies are pinned in the bundled requirements file. Chromium is
installed separately for that Playwright version. Standalone Python runtime mods
include their own `requirements.txt`. Missing dependencies fail browser acceptance
rather than silently skipping it. See [First Contact](docs/first-contact.md).

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
