# Progress and Token Reporting Contract

Use this contract for every substantial ORE task. A task is substantial when it has multiple deliverables or phases, requires repository discovery plus implementation/audit, uses repair loops, or takes long enough that the user benefits from status updates.

## Evidence-based progress

At startup, create a private weighted plan whose deliverables total 100%. Choose weights from the actual scope; do not equate progress with elapsed time, number of tool calls, files opened, or lines changed.

Typical audit-and-improve weighting:

| Deliverable | Default weight |
| --- | ---: |
| Repository discovery and baseline | 15% |
| Evidence-backed audit and prioritization | 25% |
| Authorized repair/improvement batches | 35% |
| Validation and regression checks | 20% |
| Final report and remaining backlog | 5% |

Typical audit-only weighting:

| Deliverable | Default weight |
| --- | ---: |
| Repository discovery and baseline | 20% |
| Evidence-backed audit | 55% |
| Verification and prioritization | 20% |
| Final report | 5% |

Adjust weights before work when the task is clearly different. If scope changes materially, explain the reweighting; do not silently move the percentage backward or inflate completed work.

Count a deliverable as complete only when its observable exit condition is met. Partial credit inside the active deliverable must be tied to concrete completed sub-deliverables.

## Visible update cadence

For substantial work, publish progress:

1. after discovery establishes the baseline and weighted plan;
2. at every phase transition;
3. after each completed repair batch;
4. when verified progress increases by at least 10 percentage points;
5. before asking for information or approval that blocks continued work;
6. in the final completion or blocker report.

Use this compact format:

```text
ORE 40% · Audit complete · 7 verified findings prioritized; beginning repair batch 1.
```

Do not issue empty percentage updates. Every update must name the completed evidence and the next active phase or blocker.

Use 100% only when every in-scope deliverable and required gate is complete. If work stops with a blocker or deferred scope, report the actual weighted percentage and identify what remains.

## Token-efficiency ledger

Track only defensible efficiency events during the task, such as:

- reusing validated project memory instead of rereading known material;
- sending compact context packs instead of broadcasting the same corpus to multiple roles;
- rerunning only failed gates instead of the full validated suite;
- avoiding repeated file reads whose size is known;
- eliminating a planned specialist pass because existing evidence made it unnecessary.

Do not count ordinary brevity, hypothetical future work, cached computation you cannot observe, or a guessed “full repository” baseline.

For each event, record the baseline, actual path, measurement source, and saved tokens or estimated range.

## Calculation hierarchy

Use the strongest available method:

1. **Exact:** authoritative host token counters or deterministic tokenizer counts exist for both the baseline and actual comparable inputs. Report the difference as an integer.
2. **Estimated range:** concrete text sizes or token counts exist, but tokenization or baseline has limited uncertainty. For plain text without a tokenizer, estimate `characters ÷ 4` and report a range of ±25%, rounded to sensible precision. State the baseline being compared.
3. **No demonstrated savings:** no comparable baseline or measurable avoided context exists. Report `0 tokens demonstrated`; clarify that actual savings are unknown, not necessarily zero.

Never report a percentage reduction unless both baseline and actual token quantities are defensible. Never label a character-based estimate as exact.

## Mandatory final format

Every substantial final response must contain one of these forms:

```text
Progress: 100% · 5/5 deliverables complete · all required gates passed.
Token efficiency: 3,284 tokens saved (exact; host counters, 12,940 baseline vs 9,656 actual).
```

```text
Progress: 85% · implementation complete; production validation remains blocked.
Token efficiency: approximately 2,400–4,000 tokens saved (estimated from 12,800 characters of avoided repeated context, characters ÷ 4 ±25%).
```

```text
Progress: 100% · audit and requested repairs complete.
Token efficiency: 0 tokens demonstrated · this host exposed no comparable counters or measurable avoided-context baseline; actual savings are unknown.
```

The line is mandatory even when savings are zero or unavailable. Accuracy takes priority over presenting ORE as efficient.
