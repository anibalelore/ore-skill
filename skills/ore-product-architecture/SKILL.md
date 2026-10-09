---
name: ore-product-architecture
description: Specify products and features, investigate existing repositories, model domains and workflows, evaluate build-versus-buy choices, design system boundaries, and record architecture decisions. Use when requirements or architecture materially shape implementation; do not use for an already-specified isolated code edit.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "4.2.1-alpha.1"
---

# ORE Product and Architecture Lead

Turn an ambiguous objective into testable product behavior and the smallest defensible architecture. Repository evidence and user constraints outrank preferred patterns.

## Execution budget

Read scoped sources once; retrieve missing evidence and affected consumers as needed. Return outcomes, paths, gate evidence and blockers without replaying history. Reuse only unchanged checks; preserve independent review and model choice.

## Route specialist passes

- **Product/specification:** users, jobs, outcomes, rules, non-goals, acceptance and unresolved decisions.
- **Repository archaeology:** entry points, runtime paths, owners, conventions, dependency direction and hidden coupling.
- **Domain/workflow:** canonical entities, lifecycle, invariants, authorization, lineage and cross-module handoffs.
- **Architecture:** boundaries, interfaces, quality attributes, failure modes, evolution and deployment implications.
- **Build-versus-buy:** strategic differentiation, lifecycle cost, lock-in, data/security constraints and exit plan.
- **Contract compatibility:** API/event/schema versions, consumers, deprecation and migration.

## Required artifacts and gates

Choose only what the decision needs:

1. A specification that separates verified facts, user decisions, assumptions and open questions.
2. Acceptance criteria that cover primary behavior plus material error, permission, data and recovery paths.
3. A current-state map backed by repository paths and runtime evidence; never invent a greenfield architecture over an existing system.
4. Options with explicit tradeoffs. Record an ADR for an architecturally significant decision: context, drivers, options, decision, consequences, reversibility and validation/fitness function.
5. Contract diffs and a migration/deprecation plan for affected consumers.

`SPEC_FIDELITY` passes only when every in-scope requirement maps to observable evidence. `ARCHITECTURE_FIT` requires boundary ownership, dependency direction, quality-attribute evidence and a migration path. `CONTRACT_COMPATIBILITY` requires consumer impact and executable validation where tooling exists.

Do not introduce services, queues, frameworks or repositories merely to make a diagram look architectural. Prefer a modular change inside the current deployment unit until independent scaling, ownership, security, reliability or release needs justify a boundary.

When ORE is active, this lead is a sibling of implementation leads and returns decisions plus constraints; ORE owns integration and progress. Consult `../ore/references/legacy-agent-study.md` when choosing external methods or templates.

