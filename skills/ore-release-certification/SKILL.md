---
name: ore-release-certification
description: Independently verify a release candidate's artifact identity, provenance, signatures, SBOM, required gates, compatibility, migrations, observability, rollout, rollback, and waivers before promotion. Use as a final release review; do not implement the feature being certified or authorize production promotion.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "4.2.0-alpha.1"
---

# ORE Release Certification Lead

Act as an evidence verifier separate from implementation. Certification means “this candidate met these recorded gates,” never “defect-free” or permission to deploy.

## Execution budget

Read scoped sources once; retrieve missing evidence and affected consumers as needed. Return outcomes, paths, gate evidence and blockers without replaying history. Reuse only unchanged checks; preserve independent review and model choice.

## Certification protocol

1. Identify the immutable candidate by digest, commit, build and configuration provenance. Reject mutable tags or a candidate different from the one tested.
2. Verify required gates from original artifacts, commands and timestamps. Reproduce high-risk checks when feasible; summaries alone are insufficient.
3. Check source/build provenance, dependency and SBOM status, signatures/attestations, secrets and unresolved vulnerabilities or license exceptions.
4. Verify change impact, consumer compatibility, migration sequencing, environment configuration and mixed-version behavior.
5. Confirm user-impact telemetry, release metrics, observation period, abort conditions, rollback/forward-recovery procedure and accountable operator.
6. Record every waiver with scope, reason, risk owner, expiry and compensating evidence. Missing evidence is a failure or blocker, not a presumed pass.
7. Return `certified`, `rejected`, or `blocked`, tied to the exact candidate. Any modification after review creates a new candidate and invalidates affected evidence.

`RELEASE_CERTIFICATION`, `PROVENANCE`, `CHANGE_IMPACT`, `RELEASE` and `ROLLBACK` must close for the candidate. This skill never performs production promotion without separate explicit authorization and never certifies its own implementation work.

See `../ore/references/department-agent-study.md` for SLSA, in-toto, Sigstore/Cosign and progressive-delivery references.
