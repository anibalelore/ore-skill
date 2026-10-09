# Explicit task rubric

Supply complexity, scope, dependencies, reasoning, risk, context, tools,
verification, uncertainty and cost as integer ratings 0–4, plus required_tools,
acceptance and gates. These are an operator assessment, not a learned classifier.

| Level | Work | Typical evidence |
| --- | --- | --- |
| L0 Mechanical | Search, extraction, formatting | Deterministic comparison |
| L1 Simple | Local text/style/component edit | Focused functional check |
| L2 Standard | CRUD, forms, endpoints, validation | Automated behavior tests |
| L3 Advanced | Migration, concurrency, enterprise integration | Integration, regression and independent review |
| L4 Critical | Security, authorization, finance, irreversible architecture | Risk-specific controls and independent verification |

The maximum of complexity, reasoning, risk and uncertainty sets the level.
Large scope/dependencies/context impose L3. Existing operational L0–L5 remains
a separate taxonomy; routing conservatively maps recorded operational risk to
an equal floor capped at L4. Existing task acceptance and required gates are unioned
into the profile and cannot be removed by a supplied routing profile.

Bounded L0 work inside an L4 task requires a separate explicit task contract;
the current evaluator conservatively retains the parent risk floor. Model capability
does not prove verification passed. Ratings need benchmark calibration.
