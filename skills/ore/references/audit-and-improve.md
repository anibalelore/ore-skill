# Audit and Continuous Improvement

Use this mode to evaluate an existing project, produce evidence-backed findings, and—when requested—repair or improve the current implementation through bounded, validated iterations.

## Choose the mode from user intent

- **Audit only:** inspect, run safe read-only diagnostics, verify findings, rank them, and report. Do not modify project files.
- **Audit and improve:** inspect and rank first, then implement justified repository changes within the requested scope. The user does not need to approve each ordinary code edit after explicitly requesting repair or improvement.
- **Focused audit:** inspect only the named concern, such as security, architecture, tests, performance, accessibility, data integrity, forms, dependencies, or release readiness.

If intent is unclear, default to audit only. A request to “fix,” “repair,” “improve,” “clean up,” “modernize,” “harden,” or “optimize” is sufficient authorization for relevant repository edits, not for external actions.

## Establish the baseline

Before scoring or changing anything:

1. Identify the stack, runtime, package manager, architecture, entry points, build/test commands, and deployment model.
2. Inspect current version-control status and preserve unrelated user changes.
3. Run the cheapest relevant existing checks to establish a baseline.
4. Distinguish verified defects from risks, opportunities, preferences, and unverified suspicions.
5. Record constraints that make a seemingly desirable change unsafe or incompatible.

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

Stop the loop when required findings are resolved, the requested scope is complete, remaining items are lower-priority backlog, or progress requires new authority/external state. Do not keep refactoring merely because further changes are possible.

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

Do not claim that the project is secure, complete, production-ready, or fully audited beyond the dimensions and evidence actually examined.
