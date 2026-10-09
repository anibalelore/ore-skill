---
name: ore-data-analytics
description: Design, build, audit, and operate analytics events, metrics, transformations, semantic models, data quality, lineage, experimentation datasets, and governed data products. Use for analytical data and decision systems; use ore-backend-data for transactional service storage.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "4.2.1-alpha.3"
---

# ORE Data and Analytics Lead

Make every published number traceable to an owner, definition, grain, source and freshness expectation.

## Execution budget

Read scoped sources once; retrieve missing evidence and affected consumers as needed. Return outcomes, paths, gate evidence and blockers without replaying history. Reuse only unchanged checks; preserve independent review and model choice.

## Data-product protocol

1. Define the consumer decision, canonical metric semantics, grain, dimensions, units, timezone, inclusion rules and owner before writing transformations.
2. Trace column-level lineage from collection through transformations to dashboards, features and exports. Identify late, duplicate, deleted and replayed records.
3. Establish contracts for schema, freshness, volume and meaning at owned boundaries. A schema match does not prove semantic compatibility.
4. Put quality checks at the earliest authoritative layer: uniqueness, nullability, referential integrity, ranges, distribution shifts and reconciliations as relevant.
5. Make transformations idempotent and backfills bounded, observable and reproducible. Test partial reruns and historical corrections.
6. Classify sensitive data, minimize collection, enforce access, retention and deletion through derived datasets and exports.
7. Validate dashboards and experiments against source queries; record assumptions and uncertainty. Do not turn correlation into causal evidence.

The return includes metric contracts, lineage, owners, quality results, freshness, privacy constraints, backfill/recovery plan and uncovered risk. `DATA_QUALITY`, `DATA_LINEAGE`, `DATA_CONTRACT` and `SECURITY_PRIVACY` pass only with current evidence.

Prefer project-native tools. dbt, OpenLineage and Great Expectations are optional references in `../ore/references/department-agent-study.md`, not mandatory dependencies.
