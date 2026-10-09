# Reproducible evaluation

Freeze fixture/artifact, environment, task profile, acceptance and gates. Compare
fixed-model, adaptive, and adaptive-with-escalation strategies using the same tasks:
code search, documentation, frontend, backend, debugging, refactoring, architecture,
security, business flows and change verification.

For each execution record strategy, model/provider/effort, immutable artifact,
dataset version, seed where supported, tool permissions, acceptance/gates, pass/fail,
total tokens/cost/time including delegation/validation/retries/recovery, retry count,
defects, regressions, permission violations and selection errors. Record counter
sources and unavailable fields; protect sensitive input data. Compare repeated runs
and uncertainty; independent review remains required for critical decisions.

The offline evaluator and evals/test_ore_models.py are synthetic contract tests,
not inference benchmarks. No model success probabilities or measured savings are
shipped. Real provider evaluation requires an authorized account, model access,
budget and isolated fixtures. Keep synthetic and provider results separate.

Existing ore-learning-lab comparisons keep their same-model contract. Do not use
that function to claim cross-model savings. Cross-model benchmark reporting is
manual in this alpha, pending real execution adapters and verified counters.

Run `python evals/model_routing_benchmark.py` from the repository root for 30
deterministic synthetic policy comparisons (ten categories × three strategies).
Its JSON marks measured tokens/cost, task success and savings as null. This tests
policy contract preservation only; it never executes model inference.
