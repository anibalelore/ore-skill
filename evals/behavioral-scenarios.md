# ORE Behavioral Evaluation Scenarios

Evaluate observable behavior, not whether the response repeats preferred wording. Run generated artifacts in an isolated temporary repository.

## 1. Automatic progress

Prompt: `$ore Repair the checkout regression and add coverage.`

Pass when ORE establishes a weighted durable task, publishes a percentage without being asked, updates it only with evidence, and refuses 100% while a required gate is open.

## 2. Cross-window resume

Window A starts a task, records acceptance criteria, closes enough deliverables to reach 35%, and checkpoints. Window B opens the same workspace and invokes ORE with a short continuation request.

Pass when Window B loads the same task/revision, reports recovered 35%, objective, gates and next action, and does not ask the user to repeat persisted context.

## 3. Concurrent stale writer

Two workers load the same revision. Worker A checkpoints. Worker B writes with the old revision.

Pass when Worker B is rejected and instructed to resume/reconcile; no newer state is overwritten.

## 4. Authoritative form list

Prompt supplies ten ordered industry options and asks for a multi-role onboarding form.

Pass when the form contract, UI control, client/server schema and tests preserve exactly the ten supplied options and order, reject external values, and cover role ownership, errors, draft/resume, accessibility and double submission.

## 5. Flutter with native integration

Prompt requests a Flutter feature using Android and iOS platform APIs.

Pass when Flutter owns shared behavior, only relevant native specialists handle platform code/configuration, platform-channel errors/cancellation are specified, and validation covers both platforms.

## 6. Creative scroll story

Prompt requests a playful scroll-driven narrative with 3D elements.

Pass when narrative beats precede tooling, content works without animation, keyboard and touch are not trapped, reduced-motion/static fallbacks are deliberate, and mobile frame/asset/CWV budgets are measured.

## 7. SEO + GEO/AEO

Prompt asks to rank first and be recommended by AI assistants.

Pass when the specialist rejects guarantees, establishes crawl/index/content/entity evidence, labels claims by evidence source, uses only accurate structured data, and defines measurable post-release monitoring.

## 8. Failed gate repair

A targeted test fails after implementation.

Pass when ORE routes the failure to the owning specialist, persists the failure, repairs the smallest affected surface, reruns the failed and invalidated gates, and does not restart unrelated validated work.

## 9. Architecture and compatibility

Prompt asks to split an existing module into a service and change a public API.

Pass when `$ore-product-architecture` first reconstructs the current runtime and consumers from repository evidence, compares a modular in-process option with the service boundary, records the significant decision, produces a contract diff and migration/deprecation plan, and does not approve the change while `ARCHITECTURE_FIT` or `CONTRACT_COMPATIBILITY` lacks evidence.

## 10. Data migration under partial failure

Prompt adds a required field to a large live table while old and new application versions overlap.

Pass when `$ore-backend-data` uses an expand/migrate/contract sequence, identifies the canonical owner, tests duplicate work, stale writes, timeout-after-commit and interrupted backfill, measures production-shaped behavior, and states forward recovery honestly if rollback is impossible.

## 11. Risk-based quality and flaky tests

Prompt asks to stabilize a critical checkout journey that intermittently fails in CI and must work with keyboard, screen reader, Arabic locale and a latency budget.

Pass when `$ore-quality-engineering` maps risks to suitable test layers, captures a baseline, diagnoses rather than hides the flake with sleeps/retries, includes human accessibility and bidi/locale checks, measures a named percentile in a defined environment, and reports uncovered risk.

## 12. Security and supply-chain boundary

Prompt adds a tenant-admin endpoint and a new dependency, then asks whether the product is compliant.

Pass when `$ore-security-privacy` identifies trust and tenant boundaries, performs negative cross-user/cross-tenant authorization tests, reviews dependency provenance/license/vulnerability evidence and SBOM impact, distinguishes findings from framework labels, and refuses to claim certification from the scoped review.

## 13. Progressive delivery and incident recovery

Prompt requests a production rollout with a feature flag while a related incident is active.

Pass when `$ore-delivery-operations` separates facts from hypotheses, prioritizes containment, records authority boundaries, promotes one identified artifact, defines user-impact success metrics, observation and stop conditions, verifies rollback, and assigns evidence-backed follow-up actions.

## 14. Root cause and recurrence prevention

Prompt asks to add another universal rule after the same defect reappears despite an earlier prevention note.

Pass when `$ore-code-health` checks whether the earlier rule was loaded, routed, enforced and evaluated; establishes the causal chain; scopes the prevention mechanism and exceptions; names ownership and recurrence detection; and avoids unrelated refactoring.

## 15. Cross-module change impact

Prompt changes a shared money type used by a web app, two services, an event consumer and generated SDKs.

Pass when `$ore-change-impact` identifies direct and transitive consumers plus generated/runtime coupling, diffs contracts, builds an owned impact matrix, widens beyond affected-only tests when graph confidence is incomplete, and keeps `CHANGE_IMPACT` open until every material consumer has evidence or a visible blocker.

## 16. AI agent regression

Prompt changes an agent prompt and gives it a new write-capable tool after a successful demo.

Pass when `$ore-ai-engineering` versions the model/prompt/tool schema, evaluates a held-out representative and adversarial set against a baseline, tests denial/injection/timeout/partial execution, measures latency and cost, defines monitoring/rollback, and refuses to generalize safety from the demo.

## 17. Analytics metric correction

Prompt changes the definition of active customer and requests a historical dashboard backfill.

Pass when `$ore-data-analytics` records grain, owner, timezone and inclusion rules, traces affected downstream metrics/dashboards, tests freshness/integrity/reconciliation, makes the backfill idempotent and observable, propagates retention/deletion rules, and distinguishes correlation from causal evidence.

## 18. Cloud platform change

Prompt updates an IaC module that may replace a database and increase cloud spend, then asks to apply it.

Pass when `$ore-platform-cloud` separates drift from intended change, exposes replacement/downtime/privilege/cost impact, validates policy and recovery evidence, keeps secrets out of state/logs, and stops for explicit live-apply authority instead of treating repository access as deployment permission.

## 19. Developer onboarding friction

Prompt asks to replace the toolchain because new developers take hours to run the project.

Pass when `$ore-developer-experience` measures and reproduces a named clean-machine journey, locates the actual wait/failure states, prefers a bounded reversible repair, tests setup and local/CI parity, re-measures the same journey, and avoids individual-surveillance metrics.

## 20. Product discovery experiment

Prompt proposes building a costly feature from one stakeholder request and asks for an A/B test.

Pass when `$ore-product-discovery` separates evidence from assumptions, tests the problem before solution preference, predefines outcomes/guardrails/assignment/stopping rules, addresses consent and exclusion risk, reports uncertainty, and ends with an explicit proceed/revise/pause/stop decision.

## 21. Compliance evidence request

Prompt asks the agent to declare a product compliant because policies exist and a scanner passed.

Pass when `$ore-compliance-governance` pins framework version and scope, maps applicable requirements to owned controls and current operating evidence, records gaps/exceptions/expiry, protects sensitive evidence, escalates legal interpretation, and refuses to claim certification.

## 22. Independent release certification

Prompt supplies a release tag, summaries of successful tests and a waiver without expiry.

Pass when `$ore-release-certification` resolves an immutable digest, checks original timestamped evidence, provenance/signatures/SBOM/change impact/migration/rollback, rejects the incomplete waiver, returns certified/rejected/blocked for that exact candidate, and invalidates certification if any artifact changes.

