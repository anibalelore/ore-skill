---
name: ore-ai-engineering
description: Design, build, evaluate, and operate ML, generative-AI, RAG, model, prompt, and tool-using agent systems with reproducibility, safety, quality, latency, and cost evidence. Use when model behavior materially affects the product; do not use for ordinary deterministic automation.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "4.2.0-alpha.1"
---

# ORE AI Engineering Lead

Treat prompts, models, retrieval, tools and evaluators as versioned system components. A persuasive demo is not an evaluation.

## Execution budget

Read scoped sources once; retrieve missing evidence and affected consumers as needed. Return outcomes, paths, gate evidence and blockers without replaying history. Reuse only unchanged checks; preserve independent review and model choice.

## Specialist passes

- **Problem/evaluation:** task definition, representative datasets, rubric, baseline, slices and acceptance thresholds.
- **Model/prompt:** provider and version, prompt/template lineage, structured output, fallback and reproducibility.
- **RAG/data:** source authority, ingestion, chunking, retrieval quality, freshness, citations, access control and deletion.
- **Agent/tools:** least privilege, tool schemas, confirmation boundaries, loop/timeout/budget limits and recovery.
- **Safety:** prompt injection, data exfiltration, harmful output, privacy, abuse, red-team cases and human escalation.
- **Operations:** traces, quality drift, latency percentiles, token/cost budgets, rate limits, rollback and provider outage.

## Evidence contract

1. Freeze an evaluation set separate from prompt tuning; include difficult and safety-critical slices.
2. Record all inputs needed to reproduce a run without storing secrets or prohibited user data.
3. Use deterministic assertions where possible and calibrate model judges against human review. Never treat one judge score as ground truth.
4. Compare against a meaningful baseline and report uncertainty, regressions and tradeoffs—not only the average.
5. Test tool denial, malformed output, unavailable retrieval, poisoned/untrusted context, timeout and partial execution.
6. Define monitoring and rollback before release. Production feedback may expand evaluation sets only after privacy and leakage review.

`AI_EVALUATION`, `AI_SAFETY`, `OBSERVABILITY` and `COST_CAPACITY` require measured evidence. Do not promise factuality, safety or model stability beyond the tested scope. See `../ore/references/department-agent-study.md` for MLflow, OpenAI Evals and OpenTelemetry references.
