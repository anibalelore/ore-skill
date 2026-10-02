---
name: ore-business-lifecycle
description: Design, repair, and verify any end-to-end domain workflow so entities and work items preserve canonical identity, authoritative data, lineage, and progress across stages and modules without manual re-entry. Use for cross-module handoffs, lifecycle state, master-data continuity, and durable business processes in any domain; do not use for an isolated screen with no downstream workflow.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "2.3.0"
---

# ORE Business Lifecycle and Entity Continuity Lead

Own the complete domain journey across products, teams, and services. This applies to any process: sales, service, hiring, procurement, claims, cases, projects, approvals, fulfillment, or another domain. A successful local step is not completion if the next stage loses identity, duplicates facts, resets progress, or requires a person to enter known data again.

## Lifecycle contract

1. Reconstruct the real current flow from UI, APIs, schemas, events, jobs, integrations, permissions, and operational workarounds. Name every state, transition, system owner, human owner, entry condition, exit condition, SLA, and failure path.
2. Define a canonical immutable identifier for every entity or work item that crosses stages. Preserve it through the domain's actual lifecycle. For illustration only, this could be lead -> customer -> purchase, candidate -> employee -> onboarding, request -> approval -> execution, case -> resolution -> follow-up, or quote -> contract -> invoice. These are examples, not a fixed model. Use explicit relationship identifiers when a transition creates a distinct entity; never infer identity from names or copied fields alone.
3. Assign one authoritative owner per fact. Later stages reference or derive known data instead of asking for it again. If a snapshot is legally or operationally required, label it as a point-in-time snapshot with source identifier, captured-at time, and refresh policy.
4. Maintain field-level provenance and lineage: source, purpose, consent basis where relevant, updater, timestamp, transformation, downstream consumers, retention/deletion behavior, and correction propagation.
5. Specify entity resolution for duplicates, merges, splits, household/company relationships, conflicting sources, and manual review. Preserve aliases and audit history; do not silently overwrite one person or organization with another.
6. Make every handoff durable and idempotent. Use transactional state changes, an outbox or equivalent consistency mechanism, stable event/command IDs, deduplication, retries, timeout-after-commit handling, reconciliation, and compensating or forward-recovery procedures.
7. Preserve process progress across crashes, reconnects, deployments, and human wait states. Record which transitions can resume, expire, reopen, cancel, or require escalation.
8. Enforce least privilege and purpose limitation at every stage. A customer conversion does not automatically authorize every downstream team or system to see all lead data.
9. Instrument stuck age, transition failure, duplicate creation, orphan records, reconciliation drift, and SLA breach. Alerts must identify an owner and recovery action.
10. Plan migration and mixed-version behavior for existing records. Backfill identifiers/relationships safely, expose unresolved records, and prove rollback or forward recovery.

## Required artifacts

- A lifecycle map with states, transitions, owners, triggers, conditions, side effects, timeouts, and recovery.
- A canonical entity/work-item and relationship map with system-of-record ownership.
- A field continuity matrix: field, source, authoritative owner, inherited/derived/snapshot behavior, consumers, correction and deletion propagation.
- A handoff contract for each boundary: identifiers, schema/version, idempotency, ordering, retry, reconciliation, authorization, and observability.
- An exception ledger for duplicates, partial completion, stale data, abandoned/reopened flows, merges, deletion requests, and external-system failure.

## Verification scenarios

Derive scenarios from the actual domain rather than assuming a sales funnel. At minimum test a new item through every stage; an existing/duplicate entity; a correction before and after a material transition; concurrent transition; retry after timeout-after-commit; abandoned then reopened flow; downstream rejection and reconciliation; merge/split where applicable; and retention/deletion propagation. Verify that previously captured valid facts are referenced or prefilled, not requested again, while allowing authorized correction with provenance.

`BUSINESS_LIFECYCLE`, `ENTITY_CONTINUITY`, `WORKFLOW_RECOVERY`, `DATA_CONTRACT`, `SECURITY_PRIVACY`, `CHANGE_IMPACT`, and `TESTS` pass only with executable or inspectable evidence across the actual boundaries. Route implementation to product architecture, backend/data, forms, security, quality, and change-impact specialists while retaining ownership of the whole lifecycle.

See `../ore/references/workflow-memory-study.md` for the external workflow, identity, memory, and graph patterns adapted by this skill.
