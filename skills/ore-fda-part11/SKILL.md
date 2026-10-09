---
name: ore-fda-part11
description: Engineer and verify electronic records and electronic signatures for systems with assessed FDA 21 CFR Part 11 applicability. Use for regulated record or signature workflows, not ordinary approvals without predicate-rule analysis.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "4.2.1-alpha.1"
---

# ORE FDA Part 11

Read the [regulatory engineering contract](../ore/references/regulatory-engineering.md) for source verification, evidence format, runtime interface and gates.

Before mandatory controls, identify the regulated activity, predicate rules, electronic record inventory and each record's applicability. Assess all §11.1 exclusions, especially §11.1(i): Part 117 records alone are excluded, while independently required records may remain subject. Food factory records are not automatically in scope. Read current FDA Scope and Application guidance; enforcement discretion does not remove predicate-rule obligations. Record unknowns as pending for the regulatory owner.

For applicable records use §11.10 closed-system controls; assess §11.30 additional protections for open systems. Plan risk-based validation, secure time-stamped audit trails preserving previous values, authorized access, sequencing, authority/device checks, record versioning, retention/retrieval, accurate readable and electronic copies, and documentation change control. Assess segregation of duties where the workflow requires it.

Implement signatures with verified individual identity, uniqueness and no reassignment (§11.100); signer name, timestamp and meaning (§11.50); record/version binding (§11.70). Non-biometric signing requires the §11.200 component and controlled-session rules; biometric signing requires genuine-owner-only design. Apply §11.300 credential lifecycle and unauthorized-use controls. Common MFA, a checkbox, signature image or approval boolean alone establishes none of this.

Use the shared `ore_regulatory.sign`, `verify_signature`, `supersede` and `transition` patterns. Supply server-side identity and authentication evidence, never user assertions. Do not store passwords, tokens or secrets in signatures. Commit record, signature, request-id uniqueness and audit event atomically; authorize supersession explicitly, preserve prior approvals and require a new signature for changed content/version. Revalidate before every release/shipping transition.

`ore-signature-guard` inspects supplied contracts and signed records, checks binding and permissions through executed scenario evidence, reports technical gaps and supplies gate outcomes to the existing state writer. It neither authenticates users nor installs a production signing service.

Require the eleven FDA scenarios in the contract, including failed save/retry/export and cross-module continuity. Use synthetic data and isolated storage. Route technical repairs to quality/security; applicability and organizational identity verification, training, signature policies and §11.100(c) certification evidence to compliance governance. Missing documents remain missing.

Describe verified technical controls and limitations. Do not claim FDA certification or final organizational compliance.

Use [the pending contract example](references/contract.example.json) as a starting point; replace pending scope and supply actual authorized evidence. It deliberately passes no gates.
