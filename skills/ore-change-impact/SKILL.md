---
name: ore-change-impact
description: Analyze and verify the blast radius of code, schema, API, event, dependency, configuration, or infrastructure changes across modules and consumers. Use before or after cross-boundary modifications and regressions; do not use as a substitute for the owning implementation specialist.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "2.2.0"
---

# ORE Change Impact Guardian

Prevent a locally correct change from silently breaking another module. Own the impact map and verification scope; the implementation lead still owns the change.

## Impact protocol

1. Establish the base/head diff, intended behavior and public surfaces. Include generated files, lockfiles, configuration, migrations and feature flags—not only source files.
2. Build the best available dependency graph and walk reverse dependencies. Record static imports plus runtime registration, reflection, generated code, shared storage, events, APIs, jobs and deployment coupling that the graph cannot see.
3. Produce an impact matrix with changed surface, direct and transitive consumers, compatibility risk, owner, required evidence and status.
4. Diff machine-readable contracts and representative payloads. Verify old/new and mixed-version behavior whenever deployments can overlap.
5. Select affected build, lint, unit, integration, contract and end-to-end checks. Treat selection as an optimization, not proof: run broader suites for incomplete graphs, global inputs, foundational libraries, migrations or high-risk boundaries.
6. Compare a verified baseline with the candidate. Investigate changed behavior; do not accept snapshot churn or regenerated output without explaining it.
7. Route failures to their owning specialist, update the matrix, then rerun the failed check and invalidated dependents.

`CHANGE_IMPACT` passes only when every material consumer is verified, explicitly deferred by an authorized owner, or recorded as an open blocker. `CONTRACT_COMPATIBILITY` and `TESTS` remain required when applicable. Never claim “no impact” from search results alone.

Use repository-native graph tools first. Nx, Bazel, Pact and CODEOWNERS are optional patterns described in `../ore/references/department-agent-study.md`; no tool is installed automatically.
