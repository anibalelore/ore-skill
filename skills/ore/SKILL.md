---
name: ore
description: Orchestrate substantial software, product, and technical-document delivery with durable workspace state, automatic evidence-based progress, specialist routing, form contracts, and quality gates. Use when the user invokes ORE or agency mode, asks for coordinated agents/subagents, or requests work spanning multiple disciplines. Do not use for a one-line explanation or trivial isolated edit.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "4.0.0-alpha.1"
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

## Minimum sufficient execution

Use this default on every model, including high-capability models; retain the user's chosen model and reasoning settings. Optimize repeated context and work, not required outcomes.

- Read this protocol and each applicable reference once per working context. Reopen only after a relevant change, missing detail, compaction, or evidence conflict. Links are conditional resources, not instructions to recursively read every linked file or research catalog.
- Search paths/symbols first; read the relevant implementation, callers, contracts and decisive tests. Expand when dependencies or risk require it. Keep full evidence artifacts available; return decisive lines, exit status and paths rather than complete logs.
- Begin with one accountable lead. Add a specialist pass for distinct expertise and a real agent only when authorized and its owned output or required independent review justifies duplicated context. No ceremonial roster or extra coordinator for a single worker. Independence for L3+ remains mandatory.
- Share objective, task id/revision, owned paths, decisions, acceptance criteria and gates. Send changes since the last handoff, not the whole transcript; recipients verify source evidence and retrieve missing details before acting.
- Once relevant checks pass, rerun only after a change invalidates their inputs/environment or independence requires reproduction. Never reuse a pass for a different artifact, scope or configuration.
- Keep progress updates to the required percentage, new evidence and next action; specialists return outcomes, affected paths, gate evidence, blockers and integration decisions. Expand for requested detail or material risks. No hidden evidence, fixed universal token cap, automatic model downgrade, or fabricated savings.

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

## Conditional audit modes

For `ORE audit`, `security`, `compliance`, `accessibility`, `fix`, `loop`, or `report`, read [audit-modes.md](references/audit-modes.md). It preserves ORE SECURITY, ORE PRIVACY & COMPLIANCE, ORE ACCESSIBILITY & TRUST, ORE OBSERVABILITY, and ORE AUTOFIX & VALIDATION, mode authority, all 36 controls for integral audits, proportional surface checks, and the five-iteration repair ceiling. Load only relevant control/playbook sections after establishing applicability; an integral audit still accounts for every control. Audit does not imply repair or publication authority.

For ordinary development, review the affected trust/data/UI/release boundaries and their required gates. Load the surface table when selecting those checks; do not load the full audit catalog for an irrelevant edit. Unexecuted checks remain visible coverage limitations.

## Risk levels

- **L0:** read-only explanation or inspection.
- **L1:** isolated, reversible edit.
- **L2:** normal feature or bug fix across a bounded surface.
- **L3:** cross-module, migration, security-sensitive, store/release, or architectural work.
- **L4:** production, sensitive-data, compliance, or difficult rollback work.
- **L5:** critical incident or potentially catastrophic/irreversible operation.

Increase independence checks and rollback evidence with risk. L4–L5 consequential actions require explicit authorization at the boundary; internal recommendations never grant it.

## Specialist skills

Load only the selected skill. Domain scope and handoff composition are in [specialist-routing.md](references/specialist-routing.md).

- `$ore-android` ? Android/Kotlin/Compose.
- `$ore-ios` ? iOS/Swift.
- `$ore-flutter` ? Flutter/Dart.
- `$ore-mobile-design` ? mobile UI/UX.
- `$ore-web-engineering` ? web/full-stack.
- `$ore-creative-web` ? motion/3D/storytelling.
- `$ore-search-discovery` ? SEO/AEO/GEO.
- `$ore-form-workflows` ? forms/data entry.
- `$ore-business-lifecycle` ? cross-module workflow continuity.
- `$ore-product-architecture` ? specification/domain/architecture.
- `$ore-backend-data` ? services/APIs/storage/migrations.
- `$ore-quality-engineering` ? testing/accessibility/resilience.
- `$ore-security-privacy` ? security/privacy.
- `$ore-delivery-operations` ? CI/CD/operations/incidents.
- `$ore-code-health` ? maintainability/root cause.
- `$ore-organizational-memory` ? project knowledge/provenance.
- `$ore-context-efficiency` ? context and token measurement.
- `$ore-change-impact` ? dependencies/consumers/compatibility.
- `$ore-ai-engineering` ? ML/LLM/RAG/agents.
- `$ore-data-analytics` ? metrics/data quality/lineage.
- `$ore-platform-cloud` ? cloud/IaC/platforms/DR.
- `$ore-developer-experience` ? onboarding/feedback/tooling.
- `$ore-product-discovery` ? discovery/experiments.
- `$ore-compliance-governance` ? governance/control evidence.
- `$ore-release-certification` ? independent release verification.

The ORE lead owns integration. Specialists return bounded artifacts and evidence; they do not redefine product scope or declare the whole task complete.

## Completion contract

Before reporting completion:

- every requested deliverable is complete or explicitly deferred by the user;
- every required gate has evidence or a precise, visible blocker;
- relevant form, accessibility, security, data, performance, and release risks are resolved or disclosed;
- the durable task contains the final status, evidence, decisions, remaining risks, and next action;
- progress and token-efficiency lines use the required format.

Never say “done,” “production ready,” or equivalent from code inspection alone when runnable verification was available.
