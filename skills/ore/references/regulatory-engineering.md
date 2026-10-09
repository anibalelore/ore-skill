# ORE 4.1 regulatory engineering contract

## Source baseline

Reviewed 2026-10-09; both eCFR titles displayed current through 2026-10-07.
The title dates are not assertions that these parts changed on that date.
Before each real implementation refresh the official sources, record the retrieval
date, point-in-time version and affected sections; pending review cannot pass a gate.

- [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [FDA Scope and Application guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application)
- [16 CFR Part 314](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-314)
- [FTC business guidance](https://www.ftc.gov/business-guidance/resources/ftc-safeguards-rule-what-your-business-needs-know)

Use regulation as authority and guidance as interpretation/enforcement policy;
do not substitute commercial articles. eCFR is authoritative but unofficial.

## Shared architecture and responsibilities

Keep all existing skills and six original mods. Governance owns scope, citations,
documentary review, exceptions and final determination; security/privacy owns
shared security controls; quality owns scenario execution; business lifecycle
and flow intelligence own transition enforcement. Never-again accepts only
confirmed recurring failures through its existing rule API; no automatic new
restriction or privilege grant. Both new mods use the existing SDK and state writer.

The mods are offline artifact evaluators. They do not access production, run
scanners, authenticate users, create organizational documents or send notifications.
Supply only authorized scanner/configuration extracts and synthetic test results.
Artifacts are not trusted solely because they have a matching hash: hashes prove
content stability, while provenance, coverage and legal adequacy require owner review.

## Input interface

One JSON contract per domain with `schema_version: 1`, `domain: fda|ftc`, `risk`,
`source: {url, version, checked_at}` and `scope` containing `status:
applicable|not_applicable|pending`, `owner`, `rationale`, `citations`, `evidence`.
`checked_at` and all evidence dates include timezone.

FDA scope fields: `activity`, `predicate_rules`, `electronic_records`, `exclusions`,
`fda_enforcement_policy`. FTC scope fields: `activity`, `jurisdiction`,
`financial_institution_analysis`, `entity_role`, `protected_data`, `providers`,
`314_6_analysis`. Values must explain the actual scope; a reviewer verifies facts.
Part 117 exclusions do not erase independent record obligations. §314.6 applies
only to §314.4(b)(1), (d)(2), (h), (i); all other obligations need their own analysis.

`controls`, `tests`, `documents` are maps keyed by the identifiers below. Each
entry has `result: passed|failed|pending|not_applicable`, `owner`, `severity` and
`evidence` descriptors. Each descriptor is `{path, sha256, owner, validation,
limitations, at}`: path is a repository-relative existing file; sha256 binds its
exact bytes; validation describes an executed check, not a future plan.
`not_applicable` requires evidence plus `exception: {owner, citation, rationale}`.
An organizational waiver without regulatory basis cannot remove a legal obligation.
Use existing control evidence by reference rather than recreating shared checks.

Technical control and test artifacts must be JSON with `schema_version: 1` and
`checks: {identifier: {result: "passed", validation, subject, owner, at}}`.
The evaluator reads the hash-bound artifact and matches the exact check identifier;
free-form text or a failed observation cannot pass a technical gate. An authorized
adapter converts scanner/test results to this format, preserving raw reports as
additional evidence. This checks recorded executions, not report authenticity.

FDA controls: audit_trail, history, access, segregation, versioning, retention,
retrieval, readable_copy, electronic_copy, integrity, documentation, validation.
FDA documents: identity_verification, training, signature_policy, agency_certification.
FDA tests: legitimate, unauthorized, disabled, reuse, altered, versions, incomplete,
save_failure, retry, export, module_continuity. `signed_records` contains
`{record, signature}` pairs produced by the signature pattern/trusted host adapter.

FTC controls: mfa, least_privilege, encryption_rest, encryption_transit, secrets,
inventory, secure_development, monitoring, vulnerabilities, security_tests,
change_management, disposal, providers, unauthorized_detection, incident_response.
FTC documents: risk_assessment, qualified_individual, training, provider_contracts,
provider_oversight, incident_plan, management_report, exceptions.
FTC tests: authorized, unauthorized, tenant_isolation, mfa, secrets, encryption,
events, disposal, incident, integration_failure, recovery.

Optional FTC `incident`: consumers (integer or null), discovered_at, encrypted,
key_compromised, unauthorized_access, unauthorized_acquisition,
reliable_no_acquisition_evidence (artifact reference), timeline, evidence, owner.
The engine returns a potential event/unknown alert and conservative deadline;
it does not make a final notification decision. Preserve earliest discovery.

## Execution and gates

Start/resume an ORE task through the current state CLI and add relevant gates with
`update --add-gate NAME`. To evaluate, use the existing runtime command:

```text
python skills/ore/scripts/ore_state.py runtime --repo . --task-id TASK --expect-revision REV --mod ore-signature-guard --payload '{"contract":"evidence/fda.json"}'
```

For FTC use `ore-safeguards-monitor` and its contract. Native plugin commands use
the same payload through `/ore-signature-guard` or `/ore-safeguards-monitor`.
Evaluation is read-only. Persist an outcome with the existing writer:

```text
python skills/ore/scripts/ore_state.py update --repo . --task-id TASK --expect-revision REV --gate FDA_SIGNATURE_INTEGRITY=passed --evidence FDA_SIGNATURE_INTEGRITY:evidence/fda.json
```

Six specialized controls: FDA_PART11_APPLICABILITY, FDA_SIGNATURE_INTEGRITY,
FDA_RECORD_CONTROLS, FTC_SAFEGUARDS_APPLICABILITY, FTC_SECURITY_CONTROLS,
REGULATORY_EVIDENCE. Reports contain source/version, applicability, risk, required
evidence, executed validator, result (`status`), limitations, owner and exception.
Missing applicable requirements fail; unknown applicability blocks. Add all
domain gates, not only applicability. REGULATORY_EVIDENCE requires every applicable
technical/test/document check in each supplied domain. Supply both contracts when
both domains apply. Completion rechecks all saved dependency hashes. No free-form
claim can close these gates. Hash changes require reevaluation and a new gate update.

## Signature and flow adapter contract

`sign(record, identity, authentication, ledger, request_id, now)` returns a candidate
ledger and signature. Record has id, version, content, meaning. Identity adapter
supplies id, name, verified, enabled, allowed_records. Authentication adapter
supplies subject, at, expires_at, evidence_ref, mode, owner_only and for non-biometric
signatures components, two_person_admin, continuous_session, first_signing,
session_id and session_initial_signature. Components are identifiers, never secrets.
Sessions must be independently established by the trusted host; a request cannot
self-assert continuous access. Revoked users cannot retry. A repeated request
returns the same signature only for the same signer and exact record.

The host must enforce request/signature uniqueness and atomic record/signature/audit
commit, protect the ledger against replacement/deletion, maintain clock integrity,
implement credential/device policies and test failure recovery. SHA256 alone cannot
prevent an attacker replacing a record and its digest. Validate tamper-resistant
storage and trusted authentication separately; this library is not a signing service.
Supersession preserves old approval and requires an existing replacement, authorized
actor and reason. Revocation policies require host-specific authorized procedures.

`transition('fda', before, after, signature)` requires unchanged signed record/version;
flow metadata travels outside that immutable object. `transition('ftc', before,
after)` checks tenant equality, no widened privileges/data fields and protected,
authorized destination. It is a host precondition, not an interceptor.
Flow documents may include `regulatory_transitions: [{domain, before, after,
signature}]`; flow analysis blocks continuity on a failed precondition. Adapters
must supply every applicable transition, including Production → Quality Review →
Electronic Signature → Batch Release → Shipping and customer-information disposal.

## Validation boundary

`evals/test_ore_regulatory.py` tests reusable contracts on synthetic fixtures.
Real applicability, organizational procedures, storage guarantees, IdP settings,
deletion behavior and integration coverage need application-specific executions.
Do not present package tests as a passed customer gate or FDA/FTC certification.
