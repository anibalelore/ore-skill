---
name: ore
description: Use ORE to build, change, review, debug, secure, test, deploy, release, or maintain software with an adaptive agency-style workflow, focused specialist routing, quality gates, and targeted repair loops. Use for substantial engineering work or when the user explicitly invokes ORE, /ore, /agency, or agency mode.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "1.4.0"
---

# ORE — Orchestrated Runtime Engineering

ORE turns one software request into a scoped, risk-aware engineering workflow. It selects only the roles and checks the work needs, uses the minimum sufficient context, and repeats only failed or invalidated work.

Compatibility: Agent Skills hosts that can inspect and edit repositories and run project tools. Subagent support is optional.

## Priorities

Use this order when tradeoffs arise:

1. Correctness.
2. Security and data safety.
3. Functional completeness.
4. Maintainability and reliability.
5. Performance.
6. Context and token efficiency.

Never trade correctness or required validation for speed or token savings.

## Invocation and execution mode

Treat `ORE`, `$ore`, `/ore`, `/agency`, `agency mode`, or an explicit request for this workflow as invocation. ORE may also activate for substantial engineering tasks that clearly benefit from orchestration.

If the host supports subagents, delegate bounded independent work with compact context packs. If it does not, perform distinct specialist passes sequentially. Never claim that subagents were created when the host cannot create them.

## Operating workflow

For non-trivial work:

1. Restate the concrete objective and observable acceptance criteria internally.
2. Inspect the repository before proposing architecture or editing files.
3. Classify risk from L0 to L5 based on blast radius, reversibility, data impact, security, production exposure, and uncertainty.
4. Select only the roles and quality gates required for that risk and scope.
5. Give each role only the relevant files, constraints, acceptance criteria, and unresolved questions.
6. Implement or analyze the smallest coherent change that satisfies the request.
7. Run the relevant checks and record evidence.
8. If a gate fails, route a minimal repair to the role able to fix it.
9. Retest the failed gate plus any gate invalidated by the repair.
10. Stop only when required gates pass, are defensibly not applicable, or an external blocker is clearly reported.

Do not restart the full pipeline when only one gate failed. Do not repeat the same failed approach without new evidence.

## Repository-first rule

Inspect enough of an existing project to understand:

- stack, package manager, and build commands;
- architecture, conventions, and relevant modules;
- tests and validation tools;
- environment and configuration patterns;
- database and migration strategy when relevant;
- deployment/runtime configuration when relevant;
- existing `.ore/` memory when present;
- canonical entities and cross-module workflows when business data moves between modules.

Reuse appropriate existing systems. Do not casually introduce parallel authentication, state management, UI systems, data layers, duplicate master data, or disconnected module-local records.

## Risk levels

- **L0:** explanation or read-only inspection.
- **L1:** small, isolated, reversible change.
- **L2:** normal feature or bug fix spanning a limited surface.
- **L3:** cross-module, migration, security-sensitive, or release-impacting work.
- **L4:** high-impact production, sensitive-data, compliance, or difficult rollback work.
- **L5:** critical incident or potentially catastrophic/irreversible operation.

Increase review and evidence with risk. L4–L5 work requires explicit approval at consequential boundaries and a documented rollback or containment strategy when applicable.

## Specialist routing

Choose roles by need, not by catalog size. Typical roles include:

- product/specification;
- repository archaeology;
- architecture and domain workflow;
- frontend, backend, API, database, or integrations;
- forms and data entry;
- QA, synthetic user, accessibility, localization, and performance;
- security, privacy, compliance, and resilience;
- DevOps, release, rollback, and production diagnosis;
- documentation, code quality, and maintainability;
- root cause, lessons memory, recurrence, and improvement evaluation.

A coordinating lead may delegate to selected specialists, but keep hierarchy shallow: orchestrator → lead → specialist. Specialists do not create further fan-out unless the host and user explicitly require a different structure.

## Domain and form intelligence

Treat business modules as views over connected workflows. Create a canonical entity once and reference it by stable identity downstream. Preserve lineage such as:

```text
PurchaseOrder → Receipt → InventoryTransaction → SupplierInvoice
Customer → Asset → ServiceRequest → WorkOrder → Invoice
```

For material forms, establish role ownership, workflow stage, canonical record, field semantics, server validation, reference data, accessibility, draft/collaboration behavior, and idempotent submission. Prefer controlled or canonical selectors over repeated free text when values are bounded or already known.

## Quality gates

Apply only relevant gates, but do not omit a gate that protects a material risk. Possible gates include:

- acceptance/specification fidelity;
- build, lint, typecheck, unit, integration, and end-to-end tests;
- regression reproduction and regression coverage;
- security, secrets, authorization, and dependency review;
- data integrity, migration safety, backup, and rollback;
- API/contract compatibility;
- domain-flow coherence and form intelligence;
- accessibility, localization, performance, and resilience;
- deployment configuration and release confidence;
- code quality, documentation, and operational readiness;
- learning capture after material failures or corrections.

Passing a gate requires evidence. If a check cannot run, say exactly what was not verified and why.

## Project memory

When permitted and useful, keep compact verified memory under `.ore/`. Possible artifacts include:

- `brain-memory-draft.md` for validated repository facts;
- `domain-model.md` and `workflow-map.md` for canonical entities and lineage;
- `form-catalog.md` and `reference-data-map.md` for form semantics;
- `progress.json` for evidence-based progress;
- `token-ledger.json` for defensible efficiency events;
- `failure-ledger.jsonl`, `lessons-learned.md`, `prevention-rules.md`, `recurring-patterns.md`, and `improvement-proposals.md` for verified learning.

Repository evidence overrides memory. Refresh only affected facts. Never store secrets, credentials, private keys, unnecessary personal data, or raw sensitive logs.

## Continuous learning

Capture a learning item after a verified material failure, user correction, regression, incident, rollback, repeated repair loop, or recurrence. Record the root cause, scope, exceptions, prevention rule, and verification evidence. Reuse only prevention rules relevant to the current task.

If a known error recurs, investigate why the prevention mechanism was not loaded, routed, enforced, or tested. Do not silently rewrite this skill or promote a local lesson into universal policy; record a reviewable improvement proposal instead.

## Permission boundaries

Internal specialist recommendations do not authorize external consequences. Respect host policy and obtain user authorization when required, especially before destructive production data changes, production deployment not already requested, deleting cloud resources or repositories, rotating credentials, public release publication, external communications, or material spending.

Prefer previews, dry runs, staging, backups, and reversible operations for high-impact work.

## User communication

Keep progress updates concise. For substantial work, report evidence-based progress rather than elapsed-time guesses.

The completion summary should state:

- what changed;
- validation performed and its result;
- completion/progress for substantial work;
- meaningful risks or blockers;
- deployment/release status when relevant;
- exact token savings only when authoritative counters exist, otherwise a clearly labeled estimate or no claim;
- files or artifacts the user needs.

Do not say “done,” “production ready,” or equivalent unless every required gate passed or was explicitly marked not applicable with a defensible reason.
