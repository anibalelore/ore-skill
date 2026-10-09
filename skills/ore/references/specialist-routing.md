# Specialist Routing and Handoffs

ORE uses a shallow hierarchy:

```text
ORE accountable lead
└── domain lead (only when needed)
    └── bounded specialist reviewers/workers
```

Maximum delegation depth is two below ORE. Children do not fan out. One owner is accountable for each deliverable and each gate.

Domain leads are siblings under ORE. A web lead does not delegate to a creative/search/form lead; ORE assigns each bounded sibling deliverable. Without ORE, choose one accountable lead from the primary objective and treat any second domain as a bounded specialist pass with no further fan-out.

## Routing rules

- Select specialists from actual scope and risks, not from a fixed ceremonial roster.
- Use parallel workers only for independent outputs that will not edit overlapping files.
- Keep architecture and integration decisions with the accountable lead.
- For cross-platform products, share product rules, API contracts, analytics events, accessibility goals, and design tokens; keep platform navigation, lifecycle, storage, and conventions native.
- Require an independent reviewer for L3+ architecture/security/data/release decisions or when a user correction reveals a systematic failure.

## Context pack

Every assignment contains exactly:

1. objective and non-goals;
2. owned deliverable;
3. relevant paths and current evidence;
4. constraints and decisions already made;
5. acceptance criteria and required commands/gates;
6. requested return: findings/changes, evidence, risks, and next handoff.

Do not broadcast the entire repository when a path-scoped pack is enough.

Send this pack once, then only changed facts and source identifiers. Do not load all sibling skills or their research catalogs. The receiving specialist requests missing consequential context and verifies the source before relying on a summary. A pass performed by the implementer is not an independent review.

## Return contract

Specialists return outcome and affected paths, evidence, assumptions and risks, owned gate status, and integration notes. Only ORE updates overall completion.

Return decisive command results and artifact paths, not raw logs or repeated plans. Reuse evidence already supplied when its candidate, inputs, scope and environment remain valid. ORE integrates once and reruns invalidated checks; certification and other independent gates may require fresh reproduction. Add another agent only for a distinct owned output or required independent review, within host authorization.

## Typical composition

- **Android:** Android lead → architecture/data, Compose/UI, platform/release, test/accessibility.
- **iOS:** iOS lead → architecture/concurrency, SwiftUI/UIKit, platform/release, test/accessibility.
- **Flutter:** Flutter lead → architecture/state, adaptive UI, native integration, test/performance.
- **Mobile product:** mobile design lead → research/flows, interaction/UI system, accessibility/content, validation.
- **Web:** web lead → frontend architecture, backend/contracts, performance/accessibility, QA.
- **Creative web:** creative lead → narrative/art direction, motion/scroll/3D, performance/accessibility, graceful fallback.
- **Discovery:** search lead → technical SEO, information architecture/content, structured data/entities, AEO/GEO evidence, analytics.
- **Forms:** form lead → workflow/role, field validation, reference data, state/collaboration, accessibility/UX.
- **Workflow continuity (`$ore-business-lifecycle`):** lifecycle lead → domain-specific stages, canonical identity, state/ownership, field continuity, durable handoffs, recovery/reconciliation, end-to-end evidence.
- **Product/architecture (`$ore-product-architecture`):** product lead → specification, archaeology, domain/workflow, architecture, build-vs-buy, compatibility.
- **Backend/data (`$ore-backend-data`):** backend lead → service/API, database/integrity, migration, messaging, integration, capacity/cost.
- **Quality (`$ore-quality-engineering`):** quality lead → strategy, regression, contract/integration, synthetic user, accessibility/localization, performance/resilience.
- **Security/privacy (`$ore-security-privacy`):** security lead → threat model, identity/access, application/API, privacy, supply chain, compliance evidence.
- **Delivery/operations (`$ore-delivery-operations`):** operations lead → build/CI, infrastructure, observability/SRE, release, diagnosis, incident/learning.
- **Code health (`$ore-code-health`):** health lead → maintainability, dependencies, documentation, decisions, root cause/recurrence, improvement evaluation.
- **Organizational memory (`$ore-organizational-memory`):** memory curator → capture/provenance, typed relationships, promotion, contradiction/staleness, retention/forgetting, recovery.
- **Context efficiency (`$ore-context-efficiency`):** efficiency lead → baseline, minimum context pack, output filtering, durable handoff, quality-preserving comparison.
- **Change impact (`$ore-change-impact`):** impact guardian → diff/surfaces, dependency graph, runtime coupling, consumers/owners, affected tests, compatibility matrix.
- **AI engineering (`$ore-ai-engineering`):** AI lead → evaluation/data, model/prompt, RAG, tools/agents, safety, operations/cost.
- **Data/analytics (`$ore-data-analytics`):** analytics lead → instrumentation, metric semantics, transformations, quality, lineage, privacy/backfills.
- **Platform/cloud (`$ore-platform-cloud`):** platform lead → IaC/state, identity/network, policy, self-service, capacity/cost, DR.
- **Developer experience (`$ore-developer-experience`):** DX lead → journey baseline, clean setup, feedback loops, templates/docs, self-service, outcome measurement.
- **Product discovery (`$ore-product-discovery`):** discovery lead → problem evidence, assumptions, prototype, outcomes/guardrails, experiment integrity, decision.
- **Compliance/governance (`$ore-compliance-governance`):** governance lead → framework/scope, control mapping, evidence, exceptions, audit traceability.
- **Release certification (`$ore-release-certification`):** independent verifier → artifact identity, provenance/SBOM, gate replay, compatibility, rollout/rollback, waivers.

