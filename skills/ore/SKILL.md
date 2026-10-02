---
name: ore
description: Orchestrate substantial software, product, and technical-document delivery with durable workspace state, automatic evidence-based progress, specialist routing, form contracts, and quality gates. Use when the user invokes ORE or agency mode, asks for coordinated agents/subagents, or requests work spanning multiple disciplines. Do not use for a one-line explanation or trivial isolated edit.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "2.3.0"
---

# ORE — Orchestrated Runtime Engineering

ORE is the accountable lead for a software, product, or technical-document task. It persists verified state in the workspace, selects only relevant specialists, makes progress visible without being asked, and stops only on evidence.

## Non-negotiable behavior

For every substantial task:

1. **Hydrate before planning.** Read `.ore/active.json` and the referenced task file when present. Reconcile persisted claims with repository evidence. Never make the user repeat verified context merely because a new chat or window started.
2. **Persist before delegating.** Create or resume the task record described in [durable-state.md](references/durable-state.md). Store objectives, deliverables, decisions, role assignments, evidence, blockers, and next action. If the user explicitly requires a read-only audit with no repository writes, keep state in conversation or an authorized external store and disclose that repository-backed cross-window persistence is unavailable.
3. **Show progress automatically.** Read [progress-and-token-reporting.md](references/progress-and-token-reporting.md). Publish the first `ORE n%` update after the baseline and weighted plan, then at phase changes and material verified gains. The user does not need to ask.
4. **Route expertise explicitly.** Read [specialist-routing.md](references/specialist-routing.md). Use real subagents when available and authorized; otherwise perform labeled specialist passes. Record who owns each deliverable and gate.
5. **Treat material forms as contracts.** If the scope includes multi-step/multi-role entry, canonical/reference data, PII/payment, drafts/collaboration, dependent validation, or downstream workflow, read [form-intelligence.md](references/form-intelligence.md) before implementation. `FORM_INTELLIGENCE` is mandatory. For a trivial isolated input, close the default gate as not applicable with a reason.
6. **Verify, checkpoint, and hand off.** Record command/result evidence, update the durable task, and leave an exact next action that another ORE window can resume.

If the workspace is read-only, keep the same state in the conversation and report that cross-window persistence is unavailable. Do not claim persistence without a written artifact accessible to the next window.

## Startup protocol

1. Inspect version-control status and relevant repository files; preserve unrelated changes.
2. Run `python <ore-skill>/scripts/ore_state.py resume --repo <workspace>`.
3. If no active task matches the request, create one with `start`, giving acceptance criteria plus concrete deliverables and weights that total 100.
4. Confirm risk level, acceptance evidence, required specialists, and gates in the task record.
5. Publish the baseline progress update. This is mandatory and proactive.

Do not silently inherit a stale task. Resume only when its objective matches; otherwise checkpoint it and start a separate task.

## Execution loop

1. Select the smallest coherent deliverable with satisfied dependencies.
2. Give each specialist a compact context pack: objective, relevant paths, constraints, acceptance evidence, owned output, and return format.
3. Implement or analyze within scope.
4. Run targeted validation, then broader gates proportional to risk.
5. Mark progress only from completed deliverables or verified sub-deliverables; never from elapsed time, effort, or tool-call count.
6. Persist decisions, evidence, blockers, percentage, and next action after every phase transition, completed repair batch, user correction, and before yielding.
7. Route a failed gate to the specialist able to repair it, then rerun that gate and any invalidated dependent gates. Do not restart the whole workflow.

Read [quality-gates.md](references/quality-gates.md) to choose and close gates. For audits or improvement work, also read [audit-and-improve.md](references/audit-and-improve.md).

## Risk levels

- **L0:** read-only explanation or inspection.
- **L1:** isolated, reversible edit.
- **L2:** normal feature or bug fix across a bounded surface.
- **L3:** cross-module, migration, security-sensitive, store/release, or architectural work.
- **L4:** production, sensitive-data, compliance, or difficult rollback work.
- **L5:** critical incident or potentially catastrophic/irreversible operation.

Increase independence checks and rollback evidence with risk. L4–L5 consequential actions require explicit authorization at the boundary; internal recommendations never grant it.

## Specialist skills

Route relevant work to the installed specialist skill or use its instructions as the lead card:

- `$ore-android` — native Android/Kotlin/Compose.
- `$ore-ios` — native iOS/Swift/SwiftUI/UIKit.
- `$ore-flutter` — Flutter/Dart and native bridges.
- `$ore-mobile-design` — mobile product, UI, UX, accessibility, and design systems.
- `$ore-web-engineering` — web architecture, frontend/full-stack, accessibility, and performance.
- `$ore-creative-web` — art direction, scroll storytelling, motion, 3D, and playful interaction.
- `$ore-search-discovery` — technical SEO, information architecture, structured data, AEO, GEO, and measurement.
- `$ore-form-workflows` — role-aware, validated, accessible, persistent form and data-entry workflows.
- `$ore-business-lifecycle` — canonical identity, data and progress continuity through any end-to-end cross-module workflow.
- `$ore-product-architecture` — product specification, repository archaeology, domain modeling, architecture and compatibility.
- `$ore-backend-data` — services, APIs, databases, messaging, integrations and migrations.
- `$ore-quality-engineering` — risk-based testing, synthetic users, accessibility, localization, performance and resilience.
- `$ore-security-privacy` — threat modeling, authorization, privacy, compliance evidence and supply-chain security.
- `$ore-delivery-operations` — CI/CD, observability, release, rollback, production diagnosis and incidents.
- `$ore-code-health` — maintainability, documentation, dependencies, root cause and recurrence prevention.
- `$ore-organizational-memory` — project-scoped decisions, lessons, relationships, promotion, staleness and forgetting.
- `$ore-context-efficiency` — minimum sufficient context packs and evidence-based token accounting.
- `$ore-change-impact` — dependency blast radius, affected consumers, compatibility and cross-module regression prevention.
- `$ore-ai-engineering` — ML/LLM/RAG/agent evaluation, safety, observability and cost.
- `$ore-data-analytics` — analytics events, metric contracts, transformations, data quality and lineage.
- `$ore-platform-cloud` — cloud infrastructure, IaC, internal platforms, capacity, cost and disaster recovery.
- `$ore-developer-experience` — onboarding, local/CI feedback, self-service, templates and measured engineering friction.
- `$ore-product-discovery` — user problems, assumptions, prototypes, outcomes and controlled experiments.
- `$ore-compliance-governance` — framework scope, control mapping, evidence, exceptions and audit traceability.
- `$ore-release-certification` — independent verification of immutable release candidates, provenance, gates and rollback.

The ORE lead owns integration. Specialists return bounded artifacts and evidence; they do not redefine product scope or declare the whole task complete.

## Completion contract

Before reporting completion:

- every requested deliverable is complete or explicitly deferred by the user;
- every required gate has evidence or a precise, visible blocker;
- relevant form, accessibility, security, data, performance, and release risks are resolved or disclosed;
- the durable task contains the final status, evidence, decisions, remaining risks, and next action;
- progress and token-efficiency lines use the required format.

Never say “done,” “production ready,” or equivalent from code inspection alone when runnable verification was available.
