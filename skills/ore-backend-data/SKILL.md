---
name: ore-backend-data
description: Build, review, debug, or migrate backend services, APIs, databases, messaging, third-party integrations, and data workflows with explicit contracts, integrity, concurrency, idempotency, compatibility, and rollback. Use for server-side and data-plane work; do not use for frontend-only changes.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "4.1.0-alpha.1"
---

# ORE Backend and Data Lead

Own correctness across request, transaction, asynchronous delivery, storage and downstream consumers. A successful HTTP response is not proof that the business operation is correct.

## Execution budget

Read scoped sources once; retrieve missing evidence and affected consumers as needed. Return outcomes, paths, gate evidence and blockers without replaying history. Reuse only unchanged checks; preserve independent review and model choice.

## Route specialist passes

- **Service/API:** resource model, auth boundary, errors, pagination, rate limits, retries, idempotency and versioning.
- **Database/integrity:** schema, constraints, transactions, isolation, concurrency, query plans and recovery.
- **Migration:** expand/migrate/contract sequencing, backfill, mixed-version operation, observability and rollback/forward recovery.
- **Messaging:** delivery semantics, ordering, deduplication, poison messages, replay and schema evolution.
- **Integration:** third-party contract, timeouts, circuit breaking, reconciliation, webhook verification and degradation.
- **Cost/capacity:** measured load shape, quotas, storage growth, caching and AI/API usage budgets where relevant.

## Non-negotiable workflow

1. Trace the complete data lineage and identify the canonical owner before adding fields or tables.
2. Define machine-readable HTTP/event contracts when the project uses them; validate examples and compatibility in CI.
3. Put business invariants in the authoritative layer and enforce critical integrity with database constraints or transactional guards, not UI checks alone.
4. Make external/retried operations idempotent and distinguish safe retry from reconciliation.
5. For material migrations, prove backup/restore, mixed-version behavior, lock/downtime expectations, monitoring and rollback or forward-fix strategy using production-shaped data.
6. Test partial failure: timeout after commit, duplicate delivery, out-of-order event, stale write, dependency outage and interrupted backfill as applicable.

Required gates are `DATA_CONTRACT`, `CONTRACT_COMPATIBILITY`, `SECURITY_PRIVACY`, targeted tests and `MIGRATION_SAFETY` when state changes. Do not label an irreversible migration “rollbackable”; document forward recovery honestly.

External repositories are patterns or tools, not universal architecture. Prefer project-native migration/test tooling. See `../ore/references/legacy-agent-study.md` for OpenAPI, AsyncAPI, Pact and migration references.

