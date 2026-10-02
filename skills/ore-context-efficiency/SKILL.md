---
name: ore-context-efficiency
description: Reduce agent context and token cost while preserving task fidelity, evidence, safety, and recoverability. Use for large repositories, long-running workflows, tool-heavy sessions, or repeated handoffs; do not use to drop required context, weaken verification, or claim savings without comparable measurements.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "2.3.0"
---

# ORE Context Efficiency Lead

Make the working set smaller and more relevant without making the answer less correct.

## Optimization protocol

1. Establish a baseline from host-provided token counters or a documented reproducible estimator. Record model, task boundary, tool payloads, cache assumptions, and quality/gate results so comparisons are meaningful.
2. Build the minimum sufficient context pack: objective/non-goals, owned deliverable, relevant paths/symbols, active decisions, constraints, evidence, acceptance criteria, and return contract.
3. Load only skills, references, tools, files, and history required for the current bounded task. Search or index first, then open exact regions. Filter verbose command output and retain the command, decisive lines, exit status, and artifact path.
4. Persist stable decisions and evidence in project state; hand off concise links and identifiers instead of replaying full conversations. Keep source artifacts accessible when summaries could omit a consequential detail.
5. Isolate independent high-volume work only when delegation is authorized and integration ownership is clear. Do not fragment tightly coupled reasoning merely to reduce prompt size.
6. Re-measure against the same task and gates. Reject an optimization that increases errors, rework, latency, missed consumers, security risk, or loss of reproducibility.
7. Prefer reversible changes and remove context machinery whose maintenance cost exceeds measured benefit.

## Reporting rules

Report exact savings only from authoritative comparable counters. Report an estimated range only with the method, assumptions, and uncertainty. Otherwise write `Token efficiency: 0 tokens demonstrated`. Fixed universal context thresholds and unsupported percentage claims are not evidence.

`CONTEXT_EFFICIENCY` passes when the reduced context still closes the same required gates and the comparison is reproducible. `TOKEN_ACCOUNTING` passes when baseline/candidate boundaries, measurement source, assumptions, and result are explicit. See `../ore/references/workflow-memory-study.md` for adopted and rejected external advice.
