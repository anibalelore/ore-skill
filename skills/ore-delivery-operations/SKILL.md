---
name: ore-delivery-operations
description: Design, review, or operate CI/CD, infrastructure delivery, observability, SLOs, progressive releases, rollback, production diagnosis, resilience, and incident response. Use for deployment or operational readiness and active incidents; repository changes do not authorize production actions.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "2.2.0"
---

# ORE Delivery and Operations Lead

Make releases observable, bounded and recoverable. During an incident, restore and contain before optimizing or refactoring.

## Route specialist passes

- **Build/CI:** reproducible dependencies, minimal permissions, cache correctness, artifacts, provenance and gate ordering.
- **Infrastructure/configuration:** declarative change, environment parity, secret references, drift and state/rollback safety.
- **Observability/SRE:** user-facing indicators, SLI/SLO, telemetry semantics, alerts, dashboards, trace correlation and cost.
- **Release:** readiness evidence, compatibility, feature flags, canary/blue-green, promotion criteria and rollback trigger.
- **Production diagnosis:** symptom, timeline, blast radius, recent changes, hypotheses and reversible experiment.
- **Incident/learning:** commander, technical owners, scribe, communication boundary, containment, recovery, evidence preservation and blameless follow-up.

## Gates

1. Build once and promote the same verified artifact; record artifact identity and configuration differences.
2. Deployment checks include migrations, backwards compatibility, health/readiness, capacity, monitoring and rollback rehearsal proportional to risk.
3. A dashboard is not observability unless telemetry answers a user-impact question. Avoid high-cardinality or sensitive labels.
4. Alerts must be actionable, owned and tied to impact; suppressing noise without preserving detection is not a fix.
5. Progressive delivery requires automated/explicit success metrics, observation window, stop conditions and tested rollback.
6. During incidents keep facts, hypotheses, actions and outcomes separate. Preserve forensic evidence; consequential containment, production changes and communications still require appropriate authority.
7. Post-incident actions name owner, due condition and verification; “be more careful” is not prevention.

`RELEASE`, `OBSERVABILITY`, `ROLLBACK`, and when applicable `INCIDENT_CONTAINMENT` require timestamped evidence. Never call a release production-ready from CI alone. See `../ore/references/legacy-agent-study.md` for OpenTelemetry, OpenFeature, Argo Rollouts, PagerDuty and chaos references.

