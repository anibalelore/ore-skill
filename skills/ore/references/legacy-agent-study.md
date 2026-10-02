# External Study of the Historical ORE Agents

Study date: 2026-10-02. This catalog replaces the old changelog-only agent claims with maintained leads, explicit gates and vetted sources. Repository metadata was checked against GitHub; re-check license, release and maintenance status before importing code or substantial text.

## Consolidation decision

| Historical capabilities | Decision | New owner | Why |
| --- | --- | --- | --- |
| Product/specification, repository archaeology, architecture, domain flow, build-vs-buy, API compatibility | Merge | `$ore-product-architecture` | They share one decision chain from verified current state to requirements, boundaries and compatibility. |
| Backend, API, database, integrations, migrations, data integrity, AI/API cost | Merge | `$ore-backend-data` | Correctness depends on end-to-end transaction and data lineage, not isolated role handoffs. |
| QA, regression, synthetic user, proactive bug discovery, accessibility, localization, performance, resilience | Merge with specialist passes | `$ore-quality-engineering` | One risk model should select layers and prevent duplicated or cosmetic testing. |
| Security, privacy, compliance, authorization, dependency/supply-chain risk | Merge with control-specific passes | `$ore-security-privacy` | Threat boundaries and data classification must drive controls; compliance evidence must not become a certification claim. |
| DevOps, build/release, rollback, observability, production diagnosis, incident response | Merge | `$ore-delivery-operations` | Release, telemetry, containment and rollback form one operational safety loop. |
| Documentation, code quality, maintainability, dependency health, root cause, lessons, recurrence, improvement evaluation | Merge | `$ore-code-health` | Improvement only matters when evidence connects a problem, prevention and measured result. |
| Forms/data entry | Keep separate | `$ore-form-workflows` | Demonstrated failure domain with a distinct machine-validated contract. |
| Frontend/mobile/web/search | Keep current specialist skills | Existing ORE 2.0 skills | Already have distinct triggers, platform gates and external research. |

Do not recreate every historical label as an always-loaded agent. A lead invokes a specialist pass only when a deliverable or gate uniquely needs it.

## Product and architecture sources

| Source | License/status | Adopted behavior |
| --- | --- | --- |
| [github/spec-kit](https://github.com/github/spec-kit) | MIT; active | Persist specifications as versioned artifacts; separate specify, clarify, plan, tasks, analyze and implement. ORE adapts the artifact discipline, not its entire command system. |
| [OAI/OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification) | Apache-2.0; active | Machine-readable HTTP contracts, explicit version and security considerations. |
| [asyncapi/spec](https://github.com/asyncapi/spec) | Apache-2.0; active | Machine-readable message/event contracts and bindings. |
| [microsoft/api-guidelines](https://github.com/microsoft/api-guidelines) | CC BY 4.0; active | Resource/error/versioning/idempotency patterns as design references. Attribute adapted material; do not copy wholesale into Apache-only files without license review. |
| [adr/madr](https://github.com/adr/madr) | MIT OR CC0-1.0; active | Lean ADRs containing context, options, outcome and consequences. |

Improvement applied: architecture work must emit evidence-backed current state, testable quality attributes, options/tradeoffs, significant-decision records and compatibility/migration evidence. Diagram production alone is not an architecture gate.

## Backend, data and integration sources

| Source | License/status | Adopted behavior |
| --- | --- | --- |
| [pact-foundation/pact-specification](https://github.com/pact-foundation/pact-specification) | MIT; maintained specification | Consumer/provider contract verification and consistent matching; use when contract testing fits, not as a universal dependency. |
| [golang-migrate/migrate](https://github.com/golang-migrate/migrate) | MIT; active | Ordered up/down migration mechanics and fail-on-ambiguity behavior. Tool-specific rollback does not prove business rollback. |
| OpenAPI and AsyncAPI above | Apache-2.0 | Versioned contracts and compatibility validation in CI. |
| [CNCF App Delivery TAG](https://github.com/cncf/tag-app-delivery) | Check per document | Upgrade health, backwards compatibility, declarative lifecycle and rollback patterns. Reference only unless a document's license is confirmed. |

Improvement applied: trace canonical ownership and data lineage; test duplicate/out-of-order/timeout-after-commit paths; require expand/migrate/contract plans, production-shaped backfill evidence and honest forward recovery for irreversible migrations.

## Quality engineering sources

| Source | License/status | Adopted behavior |
| --- | --- | --- |
| [microsoft/playwright](https://github.com/microsoft/playwright) | Apache-2.0; active | Cross-browser user-path automation, traces and deterministic waiting. Use project-native E2E tooling when already established. |
| [dequelabs/axe-core](https://github.com/dequelabs/axe-core) | MPL-2.0; active; trademarks/third-party notices | Automated accessibility detection as one layer only; do not copy MPL source into ORE. Manual assistive-technology checks remain required. |
| [projectfluent/fluent](https://github.com/projectfluent/fluent) | Apache-2.0; active | Localization as language-aware messages and formatting rather than string replacement. |
| Pact specification | MIT | Contract tests at consumer/provider boundaries. |
| [chaos-mesh/chaos-mesh](https://github.com/chaos-mesh/chaos-mesh) | Apache-2.0; active | Controlled fault injection with containment, steady-state hypothesis and cleanup. Never run production experiments without authority. |

Improvement applied: risk-to-test-layer mapping, pre-change reproduction, deterministic fixtures, explicit flaky-test ownership, human accessibility coverage, locale/bidi/timezone cases, measured percentiles/budgets and contained resilience experiments.

## Security, privacy and supply-chain sources

| Source | License/status | Adopted behavior |
| --- | --- | --- |
| [OWASP/ASVS](https://github.com/OWASP/ASVS) | CC BY-SA 4.0; active | Versioned verification-control catalog. Reference/control IDs may guide reviews; adapted content must preserve attribution/share-alike obligations. |
| [OWASP/API-Security](https://github.com/OWASP/API-Security) | CC BY-SA 4.0 content; active | API-specific abuse/authorization/rate/resource-consumption risks. |
| [OWASP/threat-dragon](https://github.com/OWASP/threat-dragon) | Apache-2.0; active | Data-flow-based threat modeling and recorded mitigations. Tool use is optional. |
| [ossf/scorecard](https://github.com/ossf/scorecard) | Apache-2.0 code; API data CDLA-Permissive-2.0 | Evidence for repository/supply-chain hygiene; a score is not a security verdict. |
| [CycloneDX/specification](https://github.com/CycloneDX/specification) | Apache-2.0 schemas; active | SBOM/VEX and broader bill-of-materials structure. |
| [spdx/spdx-spec](https://github.com/spdx/spdx-spec) | Community Specification License; active | License/SBOM exchange and SPDX expressions. Reference canonical released specifications; observe trademark/attribution terms. |

Improvement applied: scope attacker/data/environment, map trust boundaries and abuse cases, require negative authorization tests, separate finding from framework label, protect secret evidence, preserve SBOM/provenance and report compliance as control evidence rather than certification.

## Delivery and operations sources

| Source | License/status | Adopted behavior |
| --- | --- | --- |
| [open-telemetry/opentelemetry-specification](https://github.com/open-telemetry/opentelemetry-specification) | Apache-2.0; active | Stable cross-signal telemetry semantics and schema/version awareness. |
| [open-feature/spec](https://github.com/open-feature/spec) | Apache-2.0; active | Vendor-neutral feature-flag API concepts, evaluation context and hooks. Flags still need lifecycle/cleanup. |
| [argoproj/argo-rollouts](https://github.com/argoproj/argo-rollouts) | Apache-2.0; active | Canary/blue-green promotion based on metrics with automated abort/rollback concepts. Kubernetes-specific tool, general progressive-delivery pattern. |
| [PagerDuty/incident-response-docs](https://github.com/PagerDuty/incident-response-docs) | Apache-2.0; maintained | Explicit incident commander, scribe/liaison roles, severity, fact timeline and postmortem flow. Adapt to the organization; do not inherit PagerDuty-specific contacts/actions. |
| Chaos Mesh | Apache-2.0 | Recovery validation and fault containment. |

Improvement applied: promote one artifact, minimum-permission CI, user-impact SLIs/SLOs, actionable alerts, release stop/rollback conditions, fact-versus-hypothesis incident logs, authority boundaries and verified follow-up actions.

## Code health, documentation and learning sources

| Source | License/status | Decision |
| --- | --- | --- |
| MADR | MIT OR CC0-1.0 | Adopt lean decision-record structure for significant choices and supersession. |
| [renovatebot/renovate](https://github.com/renovatebot/renovate) | AGPL-3.0; active | Tool may be recommended after license/hosting review; do not vendor or copy its code into this Apache-2.0 package. Automated update PRs never equal safe merge. |
| GitHub Spec Kit | MIT | Reuse the principle of durable, reviewable requirements and plans, not unrelated scaffolding. |
| PagerDuty incident docs | Apache-2.0 | Use evidence-led, blameless follow-up with owned prevention actions. |

Improvement applied: distinguish defects/risks/preferences, protect generated/provenance files, test documentation, review update compatibility and lockfiles, capture lessons only from verified failures, and evaluate whether prevention was actually loaded/enforced before adding rules.

## Exclusions and licensing boundary

- Repositories are not bundled, installed or executed automatically.
- Apache/MIT/CC0 material still requires notices or attribution when copied; linking and extracting a general practice is preferred.
- CC BY/CC BY-SA material is reference-only unless attribution and derivative-license obligations are handled deliberately.
- MPL source remains under MPL at file level; do not copy it into ORE files casually.
- AGPL code such as Renovate is a tool/reference decision, not source for vendoring into ORE.
- Popularity is not a quality gate. Verify relevance, maintenance, release, security policy and fit at use time.
