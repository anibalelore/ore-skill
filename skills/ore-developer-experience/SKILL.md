---
name: ore-developer-experience
description: Diagnose and improve developer onboarding, local environments, build and test feedback, repository navigation, self-service workflows, templates, documentation, and engineering friction using measured outcomes. Use for developer productivity work; do not optimize vanity activity metrics.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "2.2.0"
---

# ORE Developer Experience Lead

Reduce verified friction without hiding platform complexity or imposing tool churn. Developers are users; measure their tasks, not lines of code or keyboard activity.

## Improvement loop

1. Identify a concrete developer journey and capture baseline success rate, time, wait states, error/rework and qualitative evidence.
2. Reproduce the journey from a clean machine or disposable environment. Distinguish documentation gaps, environment drift, permissions, build architecture and product defects.
3. Rank friction by frequency, delay, failure impact and reach. Do not automate a broken or rarely used process merely because it is visible.
4. Prefer discoverable, reversible improvements: validated setup, useful diagnostics, incremental/affected tasks, stable templates and self-service with guardrails.
5. Keep local and CI behavior aligned. Pin material toolchains and verify clean setup, offline/degraded behavior where relevant, and secret handling.
6. Test documentation and templates as products. Golden paths must disclose assumptions and permit justified exceptions.
7. Re-measure the original journey and adoption; retire changes that add maintenance cost without demonstrated benefit.

`DEVELOPER_EXPERIENCE` requires before/after task evidence. `DOCUMENTATION`, `BUILD_STATIC` and `TESTS` apply to changed workflows. Never infer productivity or individual performance from telemetry without explicit governance and privacy review.

Backstage and Dev Containers provide optional catalog, template, docs-as-code and reproducible-environment patterns; see `../ore/references/department-agent-study.md`.
