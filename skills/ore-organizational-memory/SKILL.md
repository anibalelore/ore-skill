---
name: ore-organizational-memory
description: Curate durable, project-scoped organizational memory with provenance, relationships, promotion, contradiction, staleness, and forgetting rules. Use when decisions, lessons, patterns, outcomes, or handoffs must survive sessions and guide future agents; do not use to store secrets, raw chat history, or unverified guesses as policy.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "2.3.0"
---

# ORE Organizational Memory Curator

Turn verified experience into useful project knowledge without allowing stale notes or one-off opinions to become invisible policy.

## Memory lifecycle

1. Search existing project-scoped memory before adding an entry. Never mix repositories or customers merely because they use the same agent host or database.
2. Classify the entry as fact, decision, hypothesis, failure, lesson, pattern, workflow, exception, or outcome. Record source/provenance, scope, owner, timestamp, confidence, supporting evidence, sensitive-data class, and review/expiry date.
3. Link related entries explicitly. Prefer typed relationships such as `CAUSES`, `SOLVES`, `REQUIRES`, `REPLACES`, `CONTRADICTS`, and `CONFIRMS`; keep source locations so an agent can explain why the relationship exists.
4. Treat capture and promotion as separate actions. A new observation remains memory. Promote it to a durable rule only after recurrence or strong verification, scope/exception analysis, regression evaluation, and accountable owner approval.
5. Mark superseded, contradicted, stale, or unresolved knowledge instead of deleting history silently. Retrieval must prefer current applicable entries while showing material conflicts and provenance.
6. Record outcomes after a lesson or rule is applied. If the problem recurs, inspect loading, routing, enforcement, evaluation, and scope before adding another overlapping rule.
7. Minimize and redact personal data, credentials, customer content, and confidential payloads. Apply retention and authorized forgetting to derived indexes, exports, and backups as far as the selected store permits.
8. Provide export, backup, restore, schema/version migration, and corruption recovery for any memory store before treating it as operationally durable.

## Retrieval contract

Retrieve the smallest relevant briefing by repository, task, component, lifecycle stage, time validity, and relationship. Separate verified facts from hypotheses and preferences. Never treat semantic similarity or a graph edge as proof; reopen the cited source for consequential decisions.

`MEMORY_INTEGRITY` passes when scope isolation, provenance, conflict/staleness handling, security, retention, recovery, and retrieval tests are evidenced. `KNOWLEDGE_PROMOTION` passes only when a promoted rule names its evidence, scope, exceptions, owner, approval, evaluation, and rollback/removal path.

MemoryGraph and Graphify are optional implementation references, not automatic dependencies. Do not install hooks, start cloud extraction, ingest a repository/database, or transmit content without explicit authority and a data-boundary review. See `../ore/references/workflow-memory-study.md`.
