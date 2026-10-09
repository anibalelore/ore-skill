# ORE Audit Modes and Surface Checks

Load this reference for audit/security/compliance/accessibility/fix/loop/report requests, or use only the changed-surface table for a relevant development review.

## Integrated audit capabilities

ORE SECURITY, ORE PRIVACY & COMPLIANCE, ORE ACCESSIBILITY & TRUST, ORE OBSERVABILITY, and ORE AUTOFIX & VALIDATION are reusable internal passes under this lead. They share one scope, finding register, severity model and validation ledger. Preserve existing specialist routing; these five capabilities do not create five competing agents or imply permission to delegate.

Interpret the following as natural-language modes of `$ore`, not installed shell commands:

| Request | Scope and authority |
| --- | --- |
| `ORE audit` | Integral audit; inspect all 36 control IDs for applicability, without implying repair authority. |
| `ORE security` | SEC-01–09 and relevant ADV controls, including security observability. |
| `ORE compliance` | LEG-01–08, LEG-16–20, applicable commercial LEG-09–12 and regulatory evidence. |
| `ORE accessibility` | LEG-09–15 and relevant trust, content and design controls. |
| `ORE fix` | Repair confirmed scoped findings; audit/reproduce first if none were supplied. |
| `ORE loop` | Discover → audit → plan → authorized repair → validate → re-audit, at most five iterations per run. |
| `ORE report` | Report current evidence and prioritized pending work; reconcile stale evidence and label unexecuted checks. |

For these modes, read [audit-and-improve.md](audit-and-improve.md), then relevant sections of [audit-controls.md](audit-controls.md). Read [audit-stack-playbooks.md](audit-stack-playbooks.md) for detected technologies, business and jurisdiction. Use [audit-report.md](audit-report.md) for reports, validation and checkpoints. In a focused review, mark omitted controls as out of scope rather than passed.

During everyday development, select proportional checks before closing the affected deliverable:

| Changed surface | Required review |
| --- | --- |
| Form | Validation, data purpose/minimization, permissions, accessible errors and existing form contract. |
| Login | Sessions/tokens, server limits, enumeration, recovery, OAuth and privileged MFA risk. |
| API | Server authorization, schema, response exposure, rate limits and safe errors. |
| Table | Ownership/tenant model, grants, applicable RLS and migration constraints. |
| Payments | Server amounts/currency/beneficiary, webhook signatures, idempotency and money privileges. |
| Upload | Real type, size, active content, quarantine/processing and storage access. |
| AI feature | Tool authority, injection, tenant/RAG isolation, privacy and cost budgets. |
| Subscription | Prices, renewal, refund/cancellation behavior and commercial transparency. |
| Interface | Contrast, keyboard/focus, semantics and deceptive patterns. |
| Deployment | Secrets, dependency risk, environment configuration, tests and recovery. |

Do not run a full expensive audit for an irrelevant edit. Missing tools, live access or legal context are coverage limitations, not automatic findings or passes. Do not claim complete security or legal compliance.

