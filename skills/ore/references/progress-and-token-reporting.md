# Automatic Progress and Token Reporting

Progress is a user-visible invariant, not an optional courtesy.

## When required

- For every explicit invocation of ORE, publish progress without waiting for the user to request it.
- For implicit ORE activation, do so for any task with multiple deliverables/phases, delegation, repair loops, or meaningful validation.
- A tiny isolated task may use one start and one completion update, but must not silently omit progress when ORE was explicitly requested.

## Deterministic calculation

Create weighted deliverables totaling 100 in the durable task record. The state helper calculates:

```text
progress = sum(deliverable weight × verified completion / 100)
```

Completion is evidence-based. Time elapsed, effort, tool calls, lines changed, confident language, and specialist self-reports are not completion evidence.

Default plans may be adapted before execution:

| Work type | Baseline | Analysis/design | Implementation | Validation | Handoff |
| --- | ---: | ---: | ---: | ---: | ---: |
| Build/repair | 10 | 15 | 45 | 25 | 5 |
| Audit and improve | 10 | 30 | 30 | 25 | 5 |
| Audit only | 15 | 55 | 0 | 25 | 5 |

If scope changes materially, update weights transparently and record why. Never reduce the displayed percentage merely to hide rework; record invalidated gates/deliverables and explain the recalculation.

## Visible cadence

Publish `ORE <n>% · <phase> · <evidence and next action>`:

1. after the repository baseline and weighted plan exist, or immediately after resuming persisted state;
2. at every phase transition;
3. after a verified increase of at least 10 percentage points;
4. after each completed repair batch;
5. before yielding, asking a blocking question, or awaiting authorization;
6. in the final completion or blocker report.

Write the durable state before publishing the matching percentage. Never show 100% while a deliverable, required gate, blocker, handoff, or requested artifact remains open.

Combine simultaneous cadence triggers into one update. Report only new evidence and the next action; do not repeat the entire plan, specialist history, ledger or token explanation at every tool call. Specialist reports feed the lead's update rather than duplicating overall progress. Preserve the host's required communication cadence and the user's requested detail.

## Token-efficiency reporting

Track savings only when a comparable baseline exists:

- exact from authoritative counters for both paths;
- estimated range from measured avoided text using characters ÷ 4, ±25%;
- otherwise `0 tokens demonstrated` and state that actual savings are unknown.

Never fabricate precision or count hypothetical savings.

Smaller instruction files demonstrate reduced potential context, not actual billed-token savings or equivalent model performance. Record file identities and the load scenario when comparing source sizes. Compare end-to-end host counters only with the same task, chosen model/settings, tools, acceptance evidence, required independent reviews and gates; include retries, subagents, tool payloads and available cache accounting. Without such a run, report actual savings and behavioral equivalence as unmeasured.

## Final lines

```text
Progress: 100% · 5/5 deliverables complete · all required gates passed.
Token efficiency: 0 tokens demonstrated · no comparable counters or measurable avoided-context baseline were available.
```

If blocked, use the actual computed percentage and name the remaining deliverables/gates.
