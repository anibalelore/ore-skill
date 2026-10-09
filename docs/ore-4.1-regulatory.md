# ORE 4.1 regulatory extension

Version: 4.1.0-alpha.1. Review date: 2026-10-09.

Adds two skills and two optional mods to the ORE 4.0 architecture. All 26 prior
skills, six original mods and 19 prior adapters remain; inventory is 28 skills and
27 mods. Existing 4.0 roadmap/acceptance requirements remain active.

## Implemented

- FDA and FTC applicability-first skills, official-source baseline and procedural
  evidence requirements, routed through the existing specialists.
- Shared pure signature engine: authorized individual, scoped authentication,
  controlled-session component rules, exact record/version binding, idempotent
  retry and authorized supersession preserving prior history.
- FDA/FTC flow preconditions integrated into flow analysis.
- Offline Signature Guard and Safeguards Monitor using the audited SDK and
  vendored shared runtime, with owned technical findings.
- Six specialized gates in the existing writer. Gate closure reevaluates contracts;
  completion rechecks evidence hashes. Technical checks require structured executed
  observations, not a string claiming success.
- Incident candidate evaluation, discovery deadline, timeline/evidence and explicit
  authorized review. No notification transport or automatic legal filing.

See [the integration contract](../skills/ore/references/regulatory-engineering.md)
for source links, fields, scenario identifiers, command examples and boundaries.

## Remaining application acceptance

The package evaluates supplied artifacts; it does not provide a production
identity provider, regulated database, scanner or application authorization layer.
Applications must implement and validate atomic record/signature/audit storage,
tamper resistance, trusted identity/session attestations, credential lifecycle,
retention/retrieval and export behavior. Enforce flow preconditions at each actual
transition and supply comprehensive executed scenario evidence.

Security/organizational artifacts require provenance and coverage review by their
owners. A matching hash does not authenticate a report's author or establish legal
adequacy. Missing IdP/scanner/vendor/document evidence is an explicit gap. Final
compliance determination belongs to the organization and regulatory personnel.
No FDA or FTC certification is asserted.

## Validation

Run `python scripts/validate_package.py` and
`python -m unittest discover -s evals -p 'test_*.py'`.
Regulatory synthetic tests cover signature failures/retry/export, access/tenant
preconditions, incident thresholds, every required evidence entry, gate claim
rejection and tampered evidence at completion. These are package contract tests;
they are not executions against a customer's real application.

Native host validation requires the supported Claude runtime and TypeScript
compiler. Any unavailable or incompatible host must be reported as a blocked
check rather than a passed runtime launch. Stable release requires all original
4.0 checks plus application-specific regulatory acceptance.

Validation recorded 2026-10-09:

- Package inventory/version/reference checks: passed (28 skills, 27 mods).
- Initial full suite: 100 tests, 99 passed, one skipped before Playwright installation.
- Both new skills: bundled skill validator passed using isolated PyYAML dependency.
- Both new mods: Claude manifest validation and TypeScript no-emit checks passed.
- Native SDK handlers: deterministic Node host tests passed, including unavailable
  runtime and missing-state handling; these do not replace a real host launch.
- Real host launch: blocked by installed Claude Code 2.1.267 being below the
  repository's required 2.1.287+. No supported-host launch is claimed.
- Pending example contracts: verified to block every regulatory gate.
- Application-specific production adapters and organizational evidence: pending;
  no customer system was supplied or tested and no notification was sent.

Dependency update, 2026-10-09: installed Playwright 1.63.0 and matching Chromium,
declared pinned Python requirements in the repository, core skill and standalone
Python runtime mods, and made browser acceptance mandatory. Latest full validation:
100 tests passed with no skips, including real local Chromium exploration and
masked screenshot export. Package validation and whitespace checks also passed.
