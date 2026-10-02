# External Study for Department Agents

Study date: 2026-10-02. These projects informed ORE 2.2 behavior. They are references, not dependencies; re-check version, maintenance, license and fit before adoption.

## Change impact and integration

| Source | License/status | Behavior adopted |
| --- | --- | --- |
| [nrwl/nx](https://github.com/nrwl/nx) | MIT; active | Derive affected projects from Git history plus a project graph; fail wider for global/dependency inputs. |
| [bazelbuild/bazel](https://github.com/bazelbuild/bazel) | Apache-2.0; active | Query direct/transitive and reverse dependencies; distinguish build graph evidence from runtime coupling. |
| [pact-foundation/pact-specification](https://github.com/pact-foundation/pact-specification) | MIT; active | Verify actual consumer/provider expectations rather than schemas alone. |
| [GitHub CODEOWNERS documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) | Documentation terms | Map changed surfaces to accountable reviewers; ownership does not replace tests. |

Applied: `$ore-change-impact` must produce a reverse-dependency impact matrix, inspect non-static coupling, select affected checks, widen when graph confidence is low and block unsupported “no impact” claims.

## AI engineering

| Source | License/status | Behavior adopted |
| --- | --- | --- |
| [mlflow/mlflow](https://github.com/mlflow/mlflow) | Apache-2.0; active | Versioned runs, evaluation, tracing, prompt/model lineage, monitoring and cost visibility. |
| [openai/evals](https://github.com/openai/evals) | MIT; active | Reproducible task-specific evaluations and comparison of candidate behavior. |
| [open-telemetry/semantic-conventions](https://github.com/open-telemetry/semantic-conventions) | Apache-2.0; active | Stable telemetry semantics, including evolving generative-AI conventions; pin versions. |

Applied: evaluate representative and adversarial slices against a baseline; version prompts/models/tools; constrain agent permissions and budgets; calibrate model judges with humans; monitor quality, latency and cost.

## Data and analytics

| Source | License/status | Behavior adopted |
| --- | --- | --- |
| [dbt-labs/dbt](https://github.com/dbt-labs/dbt) | Apache-2.0 core; active | Versioned analytical transformations, model dependency graphs, tests and documentation artifacts. |
| [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage) | Apache-2.0; active | Standard run/job/dataset lineage across pipeline components. |
| [great-expectations/great_expectations](https://github.com/great-expectations/great_expectations) | Apache-2.0; active | Explicit, executable expectations for data quality; tool use remains optional. |

Applied: metric contracts identify grain/owner/semantics; lineage reaches consumers; quality includes freshness and distributions; backfills are idempotent and privacy obligations propagate to derived data.

## Platform and cloud

| Source | License/status | Behavior adopted |
| --- | --- | --- |
| [opentofu/opentofu](https://github.com/opentofu/opentofu) | MPL-2.0; active | Declarative plans, resource graph, versioned state-aware infrastructure changes. Do not copy MPL source. |
| [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) | Apache-2.0; active | Declarative desired state, health/readiness and controller/reconciliation thinking; Kubernetes is not mandatory. |
| [backstage/backstage](https://github.com/backstage/backstage) | Apache-2.0; active | Software catalog, templates and docs-as-code for guarded self-service platforms. |
| [open-policy-agent/opa](https://github.com/open-policy-agent/opa) | Apache-2.0; active | Policy decisions as testable code/data separated from enforcement. |

Applied: separate plan from authorized apply; expose drift and replacements; protect state/secrets; require capacity/cost/DR evidence; provide paved roads without forcing a platform rewrite.

## Developer experience

| Source | License/status | Behavior adopted |
| --- | --- | --- |
| Backstage above | Apache-2.0 | Discoverable catalog, templates and documentation connected to owned software. |
| [devcontainers/spec](https://github.com/devcontainers/spec) | CC BY 4.0 specification; related CLI MIT | Reproducible, tool-neutral development-environment metadata reusable in CI. Attribute adapted spec material. |
| Nx above | MIT | Incremental/affected feedback based on real dependency graphs. |

Applied: start from a measured developer journey, reproduce from clean state, improve diagnostics/self-service, align local and CI behavior and re-measure outcomes without surveillance or vanity metrics.

## Product discovery and experimentation

| Source | License/status | Behavior adopted |
| --- | --- | --- |
| [github/spec-kit](https://github.com/github/spec-kit) | MIT; active | Durable separation of specification, clarification, planning and implementation. |
| [growthbook/growthbook](https://github.com/growthbook/growthbook) | Mixed MIT/open-core; active | Guardrailed feature flags, experiment definitions, metric contracts and sample-ratio checks. Review directories before reuse. |
| [open-feature/spec](https://github.com/open-feature/spec) | Apache-2.0; active | Vendor-neutral evaluation context and hooks; flags require lifecycle and cleanup. |

Applied: rank assumptions, use the cheapest ethical test, predefine outcomes/guardrails/stopping rules, report uncertainty and end with an explicit proceed/revise/pause/stop decision.

## Compliance and governance

| Source | License/status | Behavior adopted |
| --- | --- | --- |
| [usnistgov/OSCAL](https://github.com/usnistgov/OSCAL) | NIST terms/publication notices; active | Versioned machine-readable catalogs, profiles, implementations and assessment artifacts. Verify notices per artifact. |
| [oscal-compass/compliance-trestle](https://github.com/oscal-compass/compliance-trestle) | Apache-2.0; active | Compliance-as-code workflows, schema validation, Git review and traceable artifact governance. |
| [OWASP/ASVS](https://github.com/OWASP/ASVS) | CC BY-SA 4.0; active | Versioned verification controls as reference; adapted text carries attribution/share-alike obligations. |

Applied: pin framework versions and scope, map requirements to owned controls and current evidence, distinguish design from operation, expire exceptions and never invent legal interpretation or certification.

## Release certification

| Source | License/status | Behavior adopted |
| --- | --- | --- |
| [slsa-framework/slsa](https://github.com/slsa-framework/slsa) | Community Specification License 1.0 plus legacy Apache-2.0 portions | Source/build provenance and increasing supply-chain guarantees; reference the exact licensed version. |
| [in-toto/in-toto](https://github.com/in-toto/in-toto) | Apache-2.0; active | Signed attestations that link supply-chain steps and artifacts. |
| [sigstore/cosign](https://github.com/sigstore/cosign) | Apache-2.0; active | Verify artifact signatures, claims and transparency-log material against trusted identity/policy. |
| [argoproj/argo-rollouts](https://github.com/argoproj/argo-rollouts) | Apache-2.0; active | Evidence-based progressive promotion and automated abort/rollback patterns. |

Applied: certify an immutable digest, verify original evidence and provenance, bind waivers to owners/expiry, require change-impact and rollback evidence, and invalidate certification after any candidate modification.

## Shared exclusions

- No repository is cloned, installed, executed or vendored by these skills.
- Prefer principles and links over copied source or documentation. Preserve attribution, notice, share-alike, file-level copyleft and trademark obligations when reuse goes beyond a link or general practice.
- Tool popularity is not proof of project fit. Use repository-native capabilities first and document why a new dependency is necessary.
- A specialist gate records bounded evidence; it never expands permissions or grants production, legal, audit or release authority.
