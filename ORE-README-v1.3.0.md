# ORE — Orchestrated Runtime Engineering

**One request. The right specialists. Minimum sufficient context. Production-grade engineering.**

ORE is an Agent Skill that turns a coding assistant into an adaptive software-agency operating system. It uses an Agency Brain to classify work, route only necessary specialists, build compact context packs, generate an internal looping execution brief, enforce quality gates, and repeat only the failed parts of the workflow.

**v1.4 catalog:** 78 directly routable Lead/specialist agents, 9 micro-specialists across Forms and Learning (87 role cards total), and 18 workflows.

## What makes ORE different

- Agency-style specialist roles without forcing every role into every task.
- Adaptive risk levels L0–L5.
- Context Engineer + Token Governor to control context/token waste.
- Prompt Architect that creates the looping execution plan from one user command.
- Targeted repair loops instead of restarting the full pipeline.
- Quality gates with veto authority for security, tests, build, data safety, and release readiness.
- Subagent mode when available; deterministic single-agent fallback when not.
- Persistent compact `.ore/` project memory plus Brain Memory Draft hot cache.
- Continuous Learning & Failure Intelligence that records verified mistakes, recurrence patterns, and prevention rules without unsafe silent self-modification.
- Evidence-based weighted progress percentage throughout substantial work.
- Exact/estimated token-savings accounting with no fabricated precision.
- Code Quality & Style Normalizer for clean project-native code without falsifying provenance.
- Stack packs for common environments.
- Workflows for features, bugs, hotfixes, migrations, integrations, incidents, releases, and new projects.

## Example

```text
ORE: Add Stripe subscriptions with monthly/yearly plans, customer portal,
webhook reconciliation, Supabase persistence, and Vercel deployment.
```

ORE internally decides the risk level, loads the relevant project context, selects architecture/backend/frontend/integration/testing/security/deployment/release roles as needed, validates the result, and loops only failed gates.

## ORE intelligence features

### Brain Memory Draft

`.ore/brain-memory-draft.md` is the Brain's hot cache. ORE reads it before broad repository discovery, validates it against current repository state, and refreshes only affected facts. Repository evidence always wins over memory.

### Progress tracking

For substantial work ORE maintains `.ore/progress.json` and reports weighted engineering completion, for example `ORE 64% · Verification · 5/8 gates passing`. The percentage is based on observable deliverables and gates, not elapsed time.

### Token savings

`.ore/token-ledger.json` records defensible optimization events. ORE reports exact savings when authoritative runtime counters exist; otherwise it reports a clearly labeled estimate. If savings cannot be measured defensibly, ORE says so.

### Code quality normalization

The Code Quality & Style Normalizer removes low-value conversational comments, dead scaffolding, and style inconsistencies from changed code while preserving licenses, generated-file markers required by tooling, audit data, and authorship/provenance metadata. It is a quality feature, not an authorship-concealment feature.



## New in v1.4: Continuous Learning & Failure Intelligence

ORE can now learn from **verified** failures, user corrections, regressions, incidents, rollbacks, repeated repair loops, and recurring known defects. The Learning & Failure Intelligence Lead can selectively invoke Root Cause Analyst, Lessons Memory Curator, Recurrence Detector, and Improvement Evaluator.

Project-scoped learning is kept in:

```text
.ore/
├── failure-ledger.jsonl
├── lessons-learned.md
├── prevention-rules.md
├── recurring-patterns.md
└── improvement-proposals.md
```

Future tasks receive only relevant prevention rules. A lesson must contain semantics, scope, exceptions, and verification evidence—ORE does not blindly memorize literal patches. If a known error recurs, ORE diagnoses why its prevention mechanism failed. General lessons may produce an ORE improvement proposal plus regression eval, but ORE does **not** silently rewrite `SKILL.md` or core policy.

## New in v1.3: Lead Agents + Form Intelligence

ORE now supports **shallow hierarchical delegation**: Agency Brain → Lead Agent → selected specialist. Security, QA, Architecture, Release, and Forms can coordinate sub-specialties without broadcasting the whole repo/context to every worker. The maximum depth is intentionally capped; child agents never spawn more children.

The new **Forms & Data Entry Lead** treats forms as workflow/data contracts rather than generic input screens. It can invoke five micro-specialists for role/step ownership, field validation, reference/geographic data, completion efficiency, and draft/collaboration state. Material forms are protected by the `FORM_INTELLIGENCE` gate.

Example:

```text
Work Order (one canonical record)
  ├─ Administration / Planner step
  ├─ Mechanic step
  └─ Supervisor / QA step
```

Shared data is referenced once; each role edits its own fields. Bounded values use controlled/reference inputs instead of repeated free text, and jurisdiction-specific location hierarchies are configurable rather than globally hard-coded.

## Skill format

This repository is intentionally rooted at one `SKILL.md` so the `ore/` directory can be packaged directly as a compatible Agent Skill bundle. Supporting material lives in `core/`, `agents/`, `workflows/`, `references/`, `stacks/`, `templates/`, `scripts/`, and `evals/`.

## Install / package

Zip the top-level `ore/` folder:

```bash
python scripts/validate_ore.py .
cd ..
zip -r ore-skill.zip ore
```

Hosts that support Agent Skills can ingest the directory or zip. See the documentation for your host for installation details.

## Optional project bootstrap

Inside a software project:

```bash
python /path/to/ore/scripts/bootstrap_project.py .
```

This creates `.ore/` memory files, Brain Memory Draft, progress state, and token ledger without modifying application code.

Useful helpers:

```bash
python /path/to/ore/scripts/memory_status.py .
python /path/to/ore/scripts/progress_report.py .
python /path/to/ore/scripts/token_savings_report.py .
python /path/to/ore/scripts/learning_report.py .
```

## Principles

1. Correctness before token savings.
2. Security gates cannot be bypassed by convenience.
3. Read before write.
4. Prefer project conventions over invented conventions.
5. Small task = small team.
6. Complex/risky task = deeper review.
7. Internal chatter is waste; structured evidence is useful.
8. Passing tests without running them is not a pass.
9. Production-ready is an evidence claim, not a tone of voice.

## Repository map

- `core/`: agency intelligence layer and execution protocol.
- `agents/`: specialist role cards.
- `workflows/`: adaptive execution playbooks.
- `references/`: routing, gate, severity, context, and budget guidance.
- `stacks/`: stack-specific checklists.
- `templates/`: project memory and operational templates.
- `scripts/`: bootstrap and validation helpers.
- `evals/`: scenario-based checks for ORE behavior.

## License

MIT. See `LICENSE`.

## v1.2 — Intelligence, workflow coherence, and production hardening

ORE now includes 18 additional high-value specialists: Repository Archaeologist, Synthetic User, Spec Guardian, Autonomous Bug Hunter, Chaos Engineer, AI Cost Optimizer, Migration Specialist, Data Integrity Auditor, Production Detective, Accessibility Auditor, Localization/Internationalization, Compliance Agent, Build-vs-Buy Advisor, API Contract Guardian, UI Consistency Inspector, Dead Code & Complexity Hunter, Release Confidence Agent, and Workflow Coherence / Domain Flow Architect.

### The workflow-coherence rule

Business modules must not become isolated mini-apps. ORE models canonical entities and linked lifecycle records so information is entered once and reused through the workflow. Example:

```text
Supplier → PurchaseOrder → Receipt → InventoryTransaction → SupplierInvoice
```

The same `supplier_id` and `purchase_order_id` remain traceable across the system. Receiving references the existing PO; it does not recreate it. Intentional historical snapshots remain linked and documented. Project memory stores these facts in `.ore/domain-model.md` and `.ore/workflow-map.md`.



### Form intelligence memory

Projects initialized by ORE can retain `.ore/form-catalog.md` and `.ore/reference-data-map.md` so the Brain remembers field/role/reference-data decisions instead of redesigning the same form semantics on every task.
