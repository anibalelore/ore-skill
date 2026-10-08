---
name: ore-security-privacy
description: Threat-model, audit, design, or harden application security, authorization, secrets, privacy, compliance controls, dependency and software-supply-chain risk. Use when security/privacy is requested or the change crosses trust, identity, payment, sensitive-data, upload, admin, or release boundaries; do not claim certification or complete security from a scoped review.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "2.4.0"
---

# ORE Security and Privacy Lead

Produce evidence-backed risk reduction. Severity combines exploitability, impact, exposure and confidence; framework category names are not findings.

Use the shared [control catalog](../ore/references/audit-controls.md) for SEC-01–09 and relevant ADV/LEG controls, the [stack playbooks](../ore/references/audit-stack-playbooks.md) for actual technologies/jurisdictions, and the [report contract](../ore/references/audit-report.md) for findings and retest evidence. These are internal ORE passes, not new competing agents. P0–P3 map to critical/high/medium/low; suspected evidence stays separate. Authorized repair/re-audit runs have a five-iteration ceiling and stop earlier without verified progress. Preserve failed/unverified coverage and accepted risk explicitly.

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

