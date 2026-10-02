# Business Workflow, Memory, and Context Study

Checked on 2026-10-02. ORE adopts discriminating behavior, not repository code or marketing claims. No referenced project is bundled, installed, granted hooks, or authorized to transmit source/data by this study.

## User-requested repositories

| Source | License/status at review | Adopted | Excluded or guarded |
| --- | --- | --- | --- |
| [alirezarezvani/claude-skills — self-improving-agent](https://github.com/alirezarezvani/claude-skills/blob/main/engineering-team/self-improving-agent/skills/self-improving-agent/SKILL.md) | MIT; active repository | Separate discovery capture from curated promotion; detect recurrence, staleness, consolidation, and gaps between remembered and enforced rules. | Claude-specific commands and automatic policy mutation. Promotion in ORE requires scoped evidence, evaluation, owner approval, and a removal path. |
| [memory-graph/memory-graph](https://github.com/memory-graph/memory-graph) | MIT; active | Project-scoped graph memory; typed `SOLVES`, `CAUSES`, `REQUIRES`, `REPLACES`, `CONTRADICTS`, and `CONFIRMS` relations; outcomes, history, export/import, and multiple backends. | A shared global database can contaminate projects. ORE requires tenant/project isolation, redaction, retention, recovery, provenance, stale/superseded handling, and explicit install/backend authority. |
| [valorisa/Claude-Skills — token-optimization](https://github.com/valorisa/Claude-Skills/blob/main/skills/token-optimization/SKILL.md) | MIT; small active repository | Measure first; limit loaded tools/skills/history; use explicit paths and filtered outputs; isolate bounded context; compare baseline/candidate quality. | Claude-specific cache prescriptions, universal thresholds, and large fixed savings claims are not portable evidence. ORE keeps `0 tokens demonstrated` unless counters or a reproducible estimator support a comparison. |
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | Apache-2.0/MIT components reported by repository; active | Explainable AST-derived code/document graphs, incremental updates, path/explain queries, PR impact, work memory, provenance, and stale-location detection. | A graph is incomplete evidence, not runtime truth. ORE never auto-installs refresh skills/hooks, introspects databases, starts model extraction, or sends repository content without explicit authority and license/data-boundary review. |

## Primary workflow references

| Source | Pattern used by ORE |
| --- | --- |
| [Debezium Outbox Event Router](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html) | Transactional outbox, stable event identity, aggregate identity, ordering and deduplication for reliable cross-system handoffs. |
| [Temporal documentation](https://docs.temporal.io/) | Durable execution that resumes workflow progress after failures; useful for long-running business state and human/system waits. |
| [Camunda 8 / Zeebe architecture](https://docs.camunda.io/docs/components/zeebe/technical-concepts/architecture/) | Explicit process instances, jobs and append-only workflow state; reference pattern only, with exact component/version licensing checked before adoption. |
| [Open Workflow Specification](https://github.com/serverlessworkflow/specification) | Portable service-oriented workflow definition and API/event integration; exact release and license must be checked before copying schemas or code. |
| [Zingg](https://github.com/zinggAI/zingg) | Entity-resolution and master-data concepts for duplicate detection and canonical identity; adoption requires exact version/license/privacy evaluation. |

## Resulting architecture

- `$ore-business-lifecycle` owns any domain journey, canonical identity, stage continuity, durable transitions, reconciliation, and end-to-end lifecycle evidence. It derives stages from the real process rather than assuming a sales funnel.
- `$ore-organizational-memory` owns project-scoped knowledge capture, typed relationships, promotion, contradiction, staleness, retention, and recovery.
- `$ore-context-efficiency` owns minimum sufficient context packs and defensible token accounting without sacrificing gates.
- `$ore-change-impact` may use Graphify-style explainable graphs as one evidence source, but must add runtime/configuration/generated/external coupling and widen tests when confidence is incomplete.

These responsibilities remain separate: business records are not agent memory, knowledge graphs are not automatically systems of record, and context reduction cannot erase audit evidence.
