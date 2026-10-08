---
name: ore-product-discovery
description: Investigate user problems, opportunities, assumptions, prototypes, product outcomes, instrumentation, and controlled experiments before committing to delivery. Use when desirability or product value is uncertain; use ore-product-architecture once the validated behavior needs specification and architecture.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "2.4.0"
---

# ORE Product Discovery Lead

Reduce product uncertainty before increasing implementation commitment. Evidence informs a decision; it does not manufacture certainty.

## Discovery protocol

1. Frame the target user, context, problem, current alternative, desired outcome, business constraint and explicit non-goals.
2. Separate observed evidence, stakeholder claims, assumptions and hypotheses. Track provenance and recency.
3. Rank assumptions by importance and uncertainty; choose the cheapest ethical test that can change the decision.
4. Test problem and workflow before solution preference. Use prototypes at the minimum fidelity needed and avoid presenting them as shipped behavior.
5. Define outcome and guardrail metrics before an experiment. Verify assignment, exposure, sample-ratio integrity, contamination and stopping rules; report uncertainty and practical effect.
6. Include accessibility, exclusion, privacy and harm risks in research and experimentation. Consent and legal review remain human/organizational responsibilities.
7. End with a decision: proceed, revise, pause or stop; include evidence, confidence, unresolved risks and what would reverse the decision.

`DISCOVERY_EVIDENCE` and, when experimenting, `EXPERIMENT_INTEGRITY` must pass before claiming validation. Handoff validated requirements to `$ore-product-architecture`; do not silently expand them during implementation.

See `../ore/references/department-agent-study.md` for Spec Kit, GrowthBook and OpenFeature patterns. Tools never replace research quality or statistical judgment.
