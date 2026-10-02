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

