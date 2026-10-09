---
name: ore-ftc-safeguards
description: Assess FTC 16 CFR Part 314 scope and engineer evidence-backed safeguards and incident notification readiness for covered financial institutions and their service-provider boundaries. Payment processing alone does not establish applicability.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "4.2.0-alpha.1"
---

# ORE FTC Safeguards

Read the [regulatory engineering contract](../ore/references/regulatory-engineering.md) for sources, evidence, adapters and gates.

Assess entity activity, jurisdiction, financial-institution definition, protected customer information and third parties. Distinguish the regulated institution from a technology provider. Payments alone are insufficient. Document applicable, excluded and unresolved requirements with citations and an owner. §314.6 limits specific requirements for institutions maintaining information on fewer than 5,000 consumers; it is not a blanket exemption or an exemption from §314.4(j).

Reuse security/privacy implementations for MFA, least privilege, tenant boundaries, encryption, key/secret management, inventories, secure development, monitoring, vulnerabilities, tests, change management, retention/disposal, integrations and unauthorized-access detection. Verify effective configurations and executed behavior. Document permitted MFA/encryption alternatives with Qualified Individual review and the exact regulatory basis. Disposal exceptions need a documented basis; retention is not an arbitrary global timeout.

`ore-safeguards-monitor` reads authorized, hash-bound configuration/test/scanner artifacts and reports missing or failed controls with severity and owner. It does not scan production or infer IdP, encryption or vendor settings from unconnected systems. Keep evidence of written risk assessment, Qualified Individual designation, training, provider contracts/oversight, response plan, management reports and exceptions separate from automated checks. Never invent missing documents or treat automation as the complete organizational security program.

For potential incidents use `ore_regulatory.incident_readiness`. Assess unauthorized acquisition and the unauthorized-access presumption; assess encryption and key compromise, consumers affected and the earliest discovery known to a non-offending employee/officer/agent. Escalate unknown counts promptly. The 500-consumer threshold and 30-day maximum do not remove the duty to act as soon as possible. Preserve timeline/evidence for authorized review. Law-enforcement public-disclosure delay is not permission to delay reporting. Never submit a legal notification automatically.

Require the eleven FTC scenarios in the contract with synthetic data, isolated tenants and controlled failure/recovery. At each Customer Information → Authorized Access → Processing → Retention → Secure Disposal transition, enforce the shared access/protection precondition; do not widen privileges or disclose unnecessary fields.

Route scope/documents to compliance governance, technical controls to security/privacy, tests to quality and process enforcement to business lifecycle/flow intelligence. Feed verified recurring failures into the existing never-again mechanism. State verified technical outcomes and limits; never claim FTC certification.

Use [the pending contract example](references/contract.example.json) as a starting point; replace pending scope and supply actual authorized evidence. It deliberately passes no gates.
