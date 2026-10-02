# Quality Gates

Choose gates from scope and risk before implementation. A required gate is `pending`, `passed`, `failed`, or `blocked`; “not applicable” requires a reason.

- `SPEC_FIDELITY`: requested behavior and non-goals match observable acceptance criteria.
- `BUILD_STATIC`: build, formatter, lint, typecheck, and generated-code consistency as applicable.
- `TESTS`: targeted regression tests first, then the appropriate broader suite.
- `SECURITY_PRIVACY`: authorization, secrets, dependency exposure, secure storage, tracking consent, and data minimization.
- `DATA_CONTRACT`: migrations, transactions, idempotency, offline/conflict behavior, API compatibility, and rollback.
- `FORM_INTELLIGENCE`: required for material forms; use `form-intelligence.md`.
- `ACCESSIBILITY`: assistive technology, semantics, focus, contrast, text scaling, reduced motion, and errors.
- `PERFORMANCE`: measured budgets for startup/render/network/bundle/media; avoid “feels fast” as evidence.
- `DISCOVERY`: crawlability, metadata, canonicalization, structured data validity, answerability, and measurement when search visibility is in scope.
- `RELEASE`: signing/configuration, store/deployment checks, observability, rollout, and rollback.
- `HANDOFF`: durable state matches repository evidence and names the exact next action.
- `ARCHITECTURE_FIT`: current-state evidence, boundaries, drivers, tradeoffs, fitness evidence and migration path.
- `CONTRACT_COMPATIBILITY`: affected consumers and version/schema behavior have executable compatibility evidence.
- `MIGRATION_SAFETY`: backup/restore, mixed-version operation, backfill, observability and rollback/forward recovery are proven.
- `LOCALIZATION`: locale, formatting, plural, expansion, bidi, timezone and fallback behavior are verified as relevant.
- `RESILIENCE`: steady-state invariants survive controlled failures and cleanup restores the environment.
- `DEPENDENCY_HEALTH`: necessity, source, version, vulnerability/license exposure, compatibility and rollback are reviewed.
- `OBSERVABILITY`: telemetry answers user-impact questions with stable semantics and bounded sensitive/cardinality risk.
- `ROLLBACK`: release reversal or safe forward recovery has a tested trigger, procedure and owner.
- `CODE_HEALTH`: the scoped maintainability risk is reduced without unverified behavior change or unrelated refactoring.
- `DOCUMENTATION`: current users can execute the documented task; commands, links and examples are verified or limitations disclosed.
- `LEARNING_CAPTURE`: a verified failure has root cause, scoped prevention, owner and recurrence check.

Passing evidence is a command result, test report, rendered inspection, reproducible observation, schema validator, device/browser run, or authoritative artifact. Source review alone does not substitute for runnable checks when available.

When a check cannot run, record the exact command or environment that is missing, what remains unverified, and the safest next validation step. A blocker does not become a pass.

