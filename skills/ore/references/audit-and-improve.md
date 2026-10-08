# Audit and Continuous Improvement

Use this mode to evaluate an existing project, produce evidence-backed findings, and—when requested—repair or improve the current implementation through bounded, validated iterations.

For security, privacy, accessibility/trust and observability, use the single catalog in [audit-controls.md](audit-controls.md), relevant [stack playbooks](audit-stack-playbooks.md), and [report contract](audit-report.md). Existing general correctness and architecture reviews remain available.

## Choose the mode from user intent

- **Audit only:** inspect, run safe read-only diagnostics, verify findings, rank them, and report. Do not modify project files.
- **Audit and improve:** inspect and rank first, then implement justified repository changes within the requested scope. The user does not need to approve each ordinary code edit after explicitly requesting repair or improvement.
- **Focused audit:** inspect only the named concern, such as security, architecture, tests, performance, accessibility, data integrity, forms, dependencies, or release readiness.

If intent is unclear, default to audit only. A request to “fix,” “repair,” “improve,” “clean up,” “modernize,” “harden,” or “optimize” is sufficient authorization for relevant repository edits, not for external actions.

An explicit no-write or strictly read-only audit also forbids creating `.ore/` in the target repository. Keep task state in conversation or another already-authorized store and state that repository-backed cross-window resume is unavailable for that run.

## Establish the baseline

Before scoring or changing anything:

1. Initialize the weighted progress plan and token-efficiency ledger from `progress-and-token-reporting.md`.
2. Identify the stack, runtime, package manager, architecture, entry points, build/test commands, and deployment model.
3. Inspect current version-control status and preserve unrelated user changes.
4. Run the cheapest relevant existing checks to establish a baseline.
5. Distinguish verified defects from risks, opportunities, preferences, and unverified suspicions.
6. Record constraints that make a seemingly desirable change unsafe or incompatible.
7. Publish the first evidence-based ORE progress update.

Do not mistake personal style preferences for audit findings. Do not recommend large rewrites when a smaller project-native repair addresses the evidence.

## Audit dimensions

Select only dimensions relevant to the project and request:

- correctness, error handling, and edge cases;
- security, authorization, secrets, dependency exposure, and unsafe defaults;
- architecture, coupling, duplication, boundaries, and domain-flow coherence;
- data integrity, migrations, transactions, idempotency, and recovery;
- tests, coverage of critical behavior, flaky checks, and missing regression protection;
- performance, resource use, caching, concurrency, and scalability bottlenecks;
- reliability, observability, resilience, and operational failure modes;
- accessibility, localization, usability, and form intelligence;
- API compatibility, integration contracts, and versioning;
- build, CI/CD, deployment, rollback, configuration, and release readiness;
- maintainability, dead code, complexity, documentation, and dependency health.

## Finding standard

Each reported finding must include:

- concise title and affected location;
- category and severity;
- direct evidence or reproducible observation;
- concrete impact;
- recommended repair or improvement;
- confidence level when evidence is incomplete;
- validation required after repair.

Also record stable finding ID, linked control IDs, exploit preconditions, side effects, owner and validation status. Keep `suspected` separate from `confirmed`; source evidence must establish the relevant reachability and missing control before confirmation. If a safe runtime reproduction is unavailable, state that limitation. Severity is independent of confidence and finding lifecycle.

Use the existing names with stable priority aliases: **P0 / Critical** for active information exposure, severe unauthorized access or immediate significant harm; **P1 / High** for an important exploitable vulnerability or an absent essential control with material impact; **P2 / Medium** for a relevant weakness requiring scheduled repair; **P3 / Low** for bounded preventive/documentation/hardening work. Informational observations remain non-vulnerability notes and do not inflate P3 counts. L0–L5 describe operation risk, not finding severity.

Use severity based on impact and likelihood:

- **Critical:** active compromise, destructive data risk, or release-blocking catastrophic failure.
- **High:** likely material security, correctness, data, or availability impact.
- **Medium:** meaningful defect, maintainability risk, or user harm with limited blast radius.
- **Low:** bounded improvement with modest impact.
- **Informational:** useful observation without a required change.

Do not inflate severity to make the report appear valuable. Consolidate findings with the same root cause.

## Prioritize the improvement plan

Rank work using severity, user impact, confidence, effort, reversibility, dependencies, and the amount of risk reduced. Prefer this order unless project evidence justifies another:

1. Stop active security, data-loss, or production correctness risks.
2. Restore broken builds, tests, or critical user workflows.
3. Add regression protection around verified failures.
4. Repair architectural or data-flow defects that cause recurring problems.
5. Improve reliability, accessibility, performance, and maintainability.
6. Leave cosmetic or speculative changes for last.

Create a bounded first batch. Avoid combining unrelated high-risk changes into one iteration.

## Repair and improvement loop

When repository changes are authorized:

1. Select the highest-value coherent batch whose dependencies are understood.
2. Capture the pre-change failure or baseline when possible.
3. Make the smallest project-native change that addresses the root cause.
4. Add or update tests when the behavior can regress.
5. Run targeted validation, then broader checks proportional to the blast radius.
6. Reassess affected findings and any newly exposed risk.
7. Continue with the next justified batch while within scope and while meaningful verified progress remains.

Run no more than five automatic discover/audit/plan/repair/validate/re-audit iterations per execution; a smaller authorized limit takes precedence. Count unsuccessful batches too. Stop earlier when no verified progress is made, authority/access is missing for the next action, or the requested scope is complete. Do not reset the counter through delegation, compaction or retries. A later explicit continuation starts a new run from the checkpoint.

After each batch run affected regression, authentication/permission and configuration checks; compare behavior to the baseline and re-audit the affected controls. A code edit alone never resolves a finding. Mark an applied but untested change `fixed_unvalidated`; mark `resolved` only with passing retest and affected regression evidence for the current state. Never weaken a security check to make tests pass. Use versioned database migrations and preserve compatible workflows; do not blindly update major dependencies or introduce paid services.

The target is zero confirmed, unresolved P0/P1 findings that can be repaired within the authorized scope. Lower-priority backlog does not justify stopping while an authorized, correctable P0/P1 remains. Accepted risks remain visible findings with owner, rationale, scope and expiry; acceptance is not a repair or a claim of zero findings. When stopping, preserve iteration number, repository revision, changes, gate results, pending priorities and exact next action in the existing durable state plus report ledger. For a strict no-write audit, retain this checkpoint in conversation or an authorized external store.

## External boundaries

Audit-and-improve authorization applies to repository changes only. Obtain approval when required before production deployment, destructive data operations, deleting remote resources, rotating or exposing credentials, publishing releases, sending communications, changing live third-party configuration, or incurring material costs.

## Completion report

Report:

- baseline and audit scope;
- verified findings grouped by severity;
- repairs/improvements made, if authorized;
- validation evidence and remaining uncertainty;
- unresolved findings and prioritized next actions;
- any external action awaiting approval.
- weighted progress and gate completion;
- token efficiency using the exact, estimated-range, or `0 tokens demonstrated` format.

Do not claim that the project is secure, complete, production-ready, or fully audited beyond the dimensions and evidence actually examined.
