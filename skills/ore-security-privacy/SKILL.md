---
name: ore-security-privacy
description: Threat-model, audit, design, or harden application security, authorization, secrets, privacy, compliance controls, dependency and software-supply-chain risk. Use when security/privacy is requested or the change crosses trust, identity, payment, sensitive-data, upload, admin, or release boundaries; do not claim certification or complete security from a scoped review.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "2.2.0"
---

# ORE Security and Privacy Lead

Produce evidence-backed risk reduction. Severity combines exploitability, impact, exposure and confidence; framework category names are not findings.

## Route specialist passes

- **Threat modeling:** assets, actors, data flows, trust boundaries, abuse cases, threats and mitigations.
- **Identity/access:** authentication, session/token lifecycle, authorization at object/function/tenant boundaries and privileged workflows.
- **Application/API security:** validation, injection, file handling, SSRF, deserialization, browser controls, business abuse and rate limiting.
- **Data privacy:** purpose, minimization, consent/legal basis inputs, retention/deletion, export, residency and processor boundaries.
- **Supply chain:** provenance, dependencies, vulnerabilities, licenses, secrets, CI permissions, artifacts, SBOM and update policy.
- **Compliance evidence:** map requested controls to implementation and evidence; flag legal/auditor decisions instead of inventing them.

## Required workflow

1. Scope system, environment, data classification and attacker capability; distinguish verified findings from hypotheses.
2. Draw or describe trust boundaries before selecting controls.
3. Verify authorization server-side with negative cross-user/cross-tenant tests; authentication alone is not authorization.
4. Prevent secrets from entering prompts, logs, artifacts or source. Treat secret scanning output and production evidence as sensitive.
5. Pin/version security standards used. Use ASVS or similar as a control catalog, not a claim that every control applies.
6. Report finding, location, evidence, impact, likelihood, remediation, residual risk and retest. Do not publish exploit detail or contact third parties without authorization.

`SECURITY_PRIVACY` passes only when applicable high/critical findings are resolved or explicitly accepted by an authorized owner and retested. Compliance remains “control evidence reviewed,” never “certified.” External references and their share-alike/attribution limits are recorded in `../ore/references/legacy-agent-study.md`.

