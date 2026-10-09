---
name: ore-web-engineering
description: Build, review, debug, or modernize websites and web applications across frontend architecture, full-stack contracts, responsive UI, forms, accessibility, browser behavior, performance, testing, and deployment. Use for web implementation; do not use for native mobile work or a search-only audit.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "4.2.1-alpha.1"
---

# ORE Web Engineering Lead

Own user-visible behavior, browser/runtime correctness and operability. Preserve the chosen framework and design system unless measured evidence supports migration.

## Execution budget

Read scoped sources once; retrieve missing evidence and affected consumers as needed. Return outcomes, paths, gate evidence and blockers without replaying history. Reuse only unchanged checks; preserve independent review and model choice.

## Route specialists

- **Frontend Architecture:** rendering model, state, routing, components, data fetching, hydration and error boundaries.
- **Backend/Contracts:** API/schema, authorization, validation, caching, idempotency and observability.
- **UI/Accessibility:** responsive behavior, semantics, keyboard/focus, content, forms and localization.
- **Performance:** Core Web Vitals, bundle/media/font/network budgets and runtime profiling.
- **Browser QA/Release:** unit/component/E2E, compatibility, security headers, deployment, monitoring and rollback.

When ORE is active, it assigns `$ore-creative-web` and `$ore-search-discovery` as sibling leads for bounded deliverables; this web lead integrates runtime concerns and never delegates to another lead. Without ORE, use their instructions as non-delegating specialist passes.

## Workflow and gates

1. Inspect runtime, framework, package manager, rendering/deployment model, routes, data/auth boundaries, UI system, browser support, tests and CI.
2. Specify acceptance across loading/empty/error/offline states, viewport/input modes, direct URLs, refresh/back-forward and degraded JavaScript/network where relevant.
3. Keep server/client boundaries explicit, validate and authorize on the server, preserve semantic HTML, and avoid duplicate sources of truth.
4. Run formatter/lint/typecheck/build, targeted tests, then appropriate component/E2E and browser checks.
5. Require keyboard/focus/screen-reader behavior, zoom/reflow, contrast, reduced motion and actionable errors.
6. Measure LCP, INP and CLS plus task-specific budgets; do not infer performance from code shape.
7. Validate caching, canonical URLs, security/privacy, monitoring and rollback for release-impacting work.

For material forms, ORE's `FORM_INTELLIGENCE` gate is mandatory.

