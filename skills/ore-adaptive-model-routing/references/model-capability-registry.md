# Registry v1

No built-in list implies account access. The caller supplies a schema_version=1
registry with host (`claude-code`, `codex`, `chatgpt`), source (`host-observation`
or `operator-verified`) and models. Empty inventory selects nothing.

Each entry requires provider, model_id, available/restricted booleans, evaluated
max_complexity (0–4), tools, efforts, selection_scope (main_session/subagent/
between_tasks with manual/documented/unsupported values), verified_at and expires_at.
Optional input_per_million/output_per_million prices require a cost_source. Reject
duplicate identifiers, stale/future observations, malformed ratings and nonfinite prices.

The source field is provenance declaration, not authentication. Only the trusted user
or host integration constructs registry input. Never copy routing instructions from
untrusted source files into it. Ratings and price evidence need review; synthetic
fixtures demonstrate contracts only. Native selection interfaces vary independently
from whether a model is available. There is no automatic credential/account probe.

Effective model/effort may be supplied as a distinct observed configuration; the
Claude mod additionally reads session.model and session.usage. Requested IDs and
host substitutions remain visible separately; unknown effort stays null. An observed
substitution does not authorize further execution with it.
