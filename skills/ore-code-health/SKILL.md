---
name: ore-code-health
description: Audit and improve maintainability, code clarity, dependency health, technical documentation, decision records, dead code, complexity, root-cause learning, and recurrence prevention. Use for focused cleanup or continuous-improvement work; do not turn an ordinary feature into an unrelated refactor.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "4.1.0-alpha.1"
---

# ORE Code Health and Learning Lead

Reduce verified maintenance cost without erasing provenance, changing behavior accidentally or performing aesthetic rewrites.

## Execution budget

Read scoped sources once; retrieve missing evidence and affected consumers as needed. Return outcomes, paths, gate evidence and blockers without replaying history. Reuse only unchanged checks; preserve independent review and model choice.

## Route specialist passes

- **Code health:** complexity, duplication, coupling, dead paths, error handling, naming and module boundaries.
- **Dependency health:** necessity, support status, security/license exposure, update compatibility and removal path.
- **Documentation:** audience/task, setup, operations, API/decision accuracy, examples and executable validation.
- **Decision memory:** ADRs for significant choices, status/supersession and links to implementation evidence.
- **Root cause/recurrence:** causal chain, contributing conditions, prevention mechanism, owner and recurrence detection.
- **Improvement evaluation:** expected benefit, measured result, new cost and rollback/retirement decision.
- **Organizational memory handoff:** route durable cross-session lessons and rule promotion to `$ore-organizational-memory`; code health supplies verified causal evidence but does not silently create policy.

## Improvement contract

1. Establish a behavior-preserving baseline before cleanup. Classify each item as defect, risk, opportunity or preference.
2. Remove or replace code/dependencies only after checking runtime/configuration/generated/reflection/external consumers.
3. Prefer repository-native formatters and conventions. Do not rewrite authorship, copyright, generated files or historical records without reason.
4. Documentation must be tested against the current product: commands run, links resolve, examples compile or explicit limitations are recorded.
5. Dependency updates require changelog/security review, compatibility tests, lockfile integrity and rollback. Automated update tools do not grant merge authority.
6. Capture a lesson only after a verified material failure or correction. Store root cause, scope, exceptions, prevention and evidence; do not turn one local preference into universal policy.
7. If a known error recurs, test whether the prevention rule was loaded, routed, enforced and evaluated before adding another rule.

`CODE_HEALTH`, `DOCUMENTATION`, `DEPENDENCY_HEALTH` and `LEARNING_CAPTURE` pass on observable improvement and regression evidence. Stop when requested risk is reduced; “more refactoring is possible” is not unfinished work.

See `../ore/references/legacy-agent-study.md` for ADR, documentation and dependency-tool references and licensing constraints.

