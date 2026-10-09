# Flow Intelligence and Flow Watch

**One entry. Every module. Zero unnecessary re-entry.**

ORE's offline flow engine validates explicit business-flow documents and checks supplied execution evidence. Flow Watch diagnoses authorized telemetry snapshots. Neither engine writes `.ore/`, runs processes, contacts services, executes repairs, or discovers arbitrary applications automatically.

## Reproducible demonstrations

```sh
python skills/ore/scripts/ore_flow.py validate evals/fixtures/flows/factory.json
python skills/ore/scripts/ore_flow.py analyze evals/fixtures/flows/factory.json
python skills/ore/scripts/ore_flow.py analyze evals/fixtures/flows/marketplace.json
python skills/ore/scripts/ore_flow.py watch evals/fixtures/flows/factory.json --now 2026-01-01T01:00:00Z
python -m unittest discover -s evals -p "test_ore_flow.py" -v
```

The fixtures contain **synthetic model evidence**, not evidence from a beverage factory, marketplace application, production database, or payment provider. Their execution records are supplied test inputs. Automated acceptance tests mutate these inputs to reproduce faults and verify diagnostics. They do not execute a real business application or substitute for its integration/E2E tests. The base fixtures deliberately have unavailable telemetry; Watch reports `no_telemetry`, without statistics.

## Public interfaces

`validate_flow(document) -> list[str]` returns schema/reference errors. `analyze_flow(document) -> dict` returns validation results, relationship counts, findings, model continuity, and local gate recommendations. `watch_flow(document, now_iso=None) -> dict` returns connection status and evidence-backed alerts. All functions are deterministic for the supplied data and timestamp, except Watch's optional current clock. Input data is unchanged.

The CLI reads one UTF-8 JSON file. Exit status 2 means unreadable input; 1 means schema errors; 0 means analysis ran successfully. A successful analysis command can still report continuity findings: inspect `continuity_verified` and `findings` before accepting the result.

## Version 1 document contract

- `schema_version: 1`, a stable flow `id`, and arrays `entities`, `relationships`, `transitions`, `executions`.
- Entity: globally distinct `id`, domain `type`, `owner`, optional `fields`. Distinct entity identities remain distinct even within one operation.
- Field: `value`, `source` (`entity.field`), `version`, `owner`, `mode`: `canonical`, `reuse`, `snapshot`, or `transformed`. A historical snapshot needs `reason`. Reused values and versions must match their authorized source.
- Relationship: stable `id`, `source_type`, `target_type`, explicit entity `pairs`, `cardinality`, classification `status`, and `evidence`. Supported cardinalities: one-to-one, one-to-many, many-to-one, many-to-many. Classification: confirmed, inferred, unverified, contradictory, not_applicable. Confirmation is supplied by an evidence-producing adapter or reviewer; matching names never creates an edge.
- Transition: `id`, entity endpoints `source`/`target`, `event`, `owner`, string arrays `preconditions`/`permissions`, `reused_fields`, `transformations`, `state_change`, `side_effects`, `errors`, `retry`, `idempotency`, `reconciliation`, `cancellation`, `recovery`, `evidence`, and optional `required` (default true).
- Execution: distinct `id`, `transition`, `status`, timezone-aware `at`, stable `idempotency_key`, observed `preconditions`/`permissions`, `side_effect_count`, and `evidence`; optional `from_state`/`to_state` check event order against the transition's declared starting state.
- Optional `quantity_balances`: ordered, produced, rejected, packaged, shipped, and evidence. Integrity requires shipped <= packaged <= accepted production <= ordered. Partial progress is valid; overshipping or packaging rejected output is not.

Successful executions require the declared permissions, preconditions, and evidence. Duplicate deliveries must have no new side effects. Failed attempts can recover through a later successful execution with the same operation key; recovery is analyzed, never executed. Required transitions without observed success prevent continuity verification. Optional transitions represent explicitly scoped partial work, cancellations, rejected batches, refunds, or remaining shipments; adapters must not mark a required business obligation optional simply to pass.

These checks validate records supplied to the engine. A precondition label is an assertion from the adapter, not independent proof that a live database enforced it. Scope-wide temporal ordering, transactions, authorization enforcement, arithmetic payment reconciliation, and recovery semantics still require application-level tests. Contract descriptions of transforms/recovery do not execute arbitrary code.

## Watch telemetry

Set `telemetry.connection` to `connected` only when using an authorized source. Each observation supplies `entity`, `kind`, `evidence`, `last_transition`, timezone-aware `last_transition_at`, optional nonnegative `sla_seconds`, `terminal`, `owner`, `severity`, and proposed `recovery`.

Watch detects supplied stuck/unprocessed/duplicate/orphan/incompatible/reconciliation/integration/missing-transition observations and calculated SLA breaches. Alerts include process, records, last transition, elapsed time when available, evidence, severity, owner, recovery proposal, and a stable `repair_key`. Alerts are deduplicated per entity and diagnostic kind within one snapshot. No repair is scheduled or executed; a production repair service would need authorization and durable concurrency protection beyond this key.

A proposed `cause` is displayed only with `cause_evidence`; otherwise it is `unknown`. Evidence-backed correlation is not proof of causality. Unknown telemetry does not become an operational failure or a fabricated metric.

## Acceptance coverage and integration limits

Synthetic factory tests cover an existing customer, two products, separate PO/sales/production/batch/shipment identities, partial production and shipping, rejected quantity restrictions, corrected source versions, creation retries, failed logistics, and idempotent recovery. Marketplace tests cover separate order/payment/seller/shipment records, multi-vendor relations, refund permissions, cancellation-state/order mismatches, and settlement restrictions.

Adapters must collect real schema/API/trace/test evidence to create flow documents. Browser exploration, repository-wide discovery, external telemetry connectors, automatic code repair, and production replay are not implemented by this module. Integrate with existing `ore-business-lifecycle`, `ore-backend-data`, `ore-form-workflows`, and quality-engineering procedures rather than treating the model as independent certification.

`gates` are local model recommendations. `CHANGE_IMPACT` and `TESTS` remain pending because a model alone cannot establish them. Recommendations never close ORE's persisted quality gates; `ore_state.py` remains the state-writing authority, and real scope-specific evidence is required before task completion. Version 1 documents are optional and do not change legacy task behavior.
