# Durable Workspace State

Use repository-backed state so another ORE-enabled conversation or window working in the same workspace can resume without the user reconstructing the task.

## Storage contract

Store state under `.ore/` in the target repository:

```text
.ore/
├── active.json
├── tasks/<task-id>.json
├── handoffs/<task-id>.md
├── forms/<form-id>.json
└── lessons.md
```

Do not put credentials, tokens, private keys, raw production data, private logs, or unnecessary personal information in these files. If `.ore/` should not be committed, add it to the project's ignore mechanism only when that does not conflict with the user's desired shared persistence.

## Task record

The task JSON must preserve:

- stable task id, title, objective, status, risk, created/updated timestamps;
- weighted deliverables and their status/evidence;
- selected leads/subagents and owned outputs;
- required gates and their status/evidence;
- decisions and user corrections with rationale;
- blockers, remaining risks, exact next action, and progress percentage.

Repository evidence overrides stale state. When code and memory disagree, repair the state and record the reconciliation.

## Required lifecycle

Use `scripts/ore_state.py` relative to this skill directory:

```text
python <ore-skill>/scripts/ore_state.py resume --repo <workspace>
python <ore-skill>/scripts/ore_state.py start --repo <workspace> --title "..." --objective "..." --kind general --acceptance "observable criterion" --deliverable "Baseline:15" --deliverable "Implementation:45" --deliverable "Validation:30" --deliverable "Handoff:10"
python <ore-skill>/scripts/ore_state.py update --repo <workspace> --task-id <task-id> --expect-revision <revision> --deliverable "Baseline=done" --evidence "Baseline: stack and failing check recorded"
python <ore-skill>/scripts/ore_state.py checkpoint --repo <workspace> --task-id <task-id> --expect-revision <revision> --next "Run targeted regression test"
python <ore-skill>/scripts/ore_state.py complete --repo <workspace> --task-id <task-id> --expect-revision <revision>
```

The helper computes progress from weights. A revision is mandatory for every write; a mismatch means another window changed the task and state must be resumed and reconciled. Use `list` and `resume --task-id` for multiple tasks. The helper serializes writers, validates safe task ids, rejects unknown deliverables, weights not totaling 100, stale revisions, and completion with open gates or blockers.

## Cross-window guarantee and limit

The guarantee applies when windows share the same workspace and can load this skill. A skill cannot synchronize arbitrary unrelated workspaces or clients with no shared storage. State that limit honestly; never imply invisible global memory.

At every yield, write a handoff with: current objective, verified completed work, active files, last validation, blockers, unresolved decisions, and one exact next action.

