# ORE control catalog

One catalog serves the five internal capabilities. Read only the sections needed for a focused task; an integral audit considers all 29 original controls and seven advanced controls. For every selected ID record applicability, inspected components/environment, evidence, outcome, finding IDs and missing coverage. Outcomes: `passed`, `failed`, `not_applicable`, `not_evaluated`, `out_of_scope`. A failed control can contain suspected or confirmed findings; lack of evidence is not a pass. Non-applicability needs a reason. Record versions of standards and authoritative legal sources at execution time.

## ORE SECURITY — nine original controls

### SEC-01 — Row Level Security and database authorization
Inventory exposed schemas, tables, views, RPC functions, grants, roles, RLS enablement and SELECT/INSERT/UPDATE/DELETE policies, plus Supabase Storage policies. Reconstruct user, organization, company, branch, membership, shared and administrator relationships before defining access; never assume every row is individually owned. Inspect USING/WITH CHECK, policy composition, changes to ownership/tenant/role columns, views' execution context, SECURITY DEFINER function grants/search_path and privileged roles/service_role. RLS is not proof of isolation when a reachable privileged path bypasses it. Keep privileged credentials server-side and narrowly scoped. Validate horizontal IDOR/BOLA and vertical access using anonymous, owner, colleague, unauthorized colleague, tenant A/B and scoped administrators. Exercise reads, mutations, RPC and files through actual application roles, not only a database owner. Expect allowed sharing to continue and denied reads/writes to expose/alter no foreign data. Use versioned migrations and disposable fixtures with rollback/cleanup.

### SEC-02 — CORS
Inventory every API/server and environment, permitted origins, methods, headers, credentials and preflight handling. Use an explicit environment-specific allowlist where browser cross-origin access is needed; avoid arbitrary origin reflection or permissive credential combinations. Test permitted and denied origins, OPTIONS and credential behavior; separate local development from production. CORS governs browsers and is neither authentication nor protection from non-browser requests. Independently test endpoint token and authorization enforcement.

### SEC-03 — Brute-force resistance
Inspect password login, registration, password recovery, OTP, administration and applicable API authentication. Prefer existing provider limits; verify server-side enforcement across replicas and account/IP signals as appropriate, progressive delays, bounded recovery and enumeration-safe replies. Avoid arbitrary permanent lockouts or account-targeted denial of service. In a test environment use bounded attempts and check throttling, expiry, legitimate recovery and indistinguishable account-existence behavior without flooding real endpoints.

### SEC-04 — Tokens and sessions
Review access/refresh expiry, rotation, reuse detection, revocation, logout, password recovery, persistence, administrator sessions, backend identity validation and cookies' Secure/HttpOnly/SameSite settings as appropriate to the architecture. Do not prescribe a universal token-storage rewrite; remove demonstrated unsafe exposure and document browser/mobile trust boundaries. Test stale/revoked tokens, refresh replay, logout and account recovery according to the provider's documented guarantees. Where the risk warrants it, provide visible active sessions and termination of other sessions; explain any bounded access-token revocation delay.

### SEC-05 — Bots and resource abuse
Inspect public forms/endpoints for credential stuffing, abusive signup, spam, excessive scraping, promotion fraud, API saturation and AI resource abuse. Reuse proportionate server rate limits, quotas, WAF and anomaly controls; introduce Turnstile/CAPTCHA only when justified, with accessible alternatives and server verification. Check token replay/expiry where challenges apply. Test quota isolation and legitimate-user behavior; measure false positives, workload and AI spend limits. New paid providers require authorization.

### SEC-06 — Authentication and authorization
Trace login/signup, Google/Microsoft or other OAuth, reset, invitations, private endpoints, admin roles and frontend-triggered operations to authoritative server decisions. Check signed token issuer/audience/expiry, OAuth state/PKCE/redirects as applicable, role assignment, invitation scope and single-use recovery. UI hiding is not authorization. Test missing, invalid and insufficient credentials, role escalation, invitations and sensitive transitions. Consider MFA/step-up for privileged and sensitive operations according to risk, and verify recovery cannot bypass it.

### SEC-07 — Malicious uploads
Inventory upload, download and processing paths for documents, images and video. Enforce server size limits, allowlisted formats, real type/magic bytes, safe storage names, traversal prevention, isolated parsing and access controls. Analyze SVG/HTML/active content, archives and decompression/resource limits. Use scanning and quarantine where warranted; define unavailable-scanner behavior so unsafe files do not become public during outages. Prevent execution, use suitable download headers and expiring signed URLs. Do not trust extensions or browser MIME alone. Test mismatched/truncated files, traversal, oversize, parser failure, active content and unauthorized access with benign fixtures; do not execute malware.

### SEC-08 — Sensitive-data exposure
Review client bundles, API serialization/errors, backend, logs, storage, configuration and tracked source/history as authorized. Identify unnecessary credentials/passwords/tokens/private keys, PII, identity documents, financial details, addresses/phones and foreign-tenant records. Use response allowlists, safe errors, secret management, least privilege and log redaction. Reports contain redacted type/location and exposure conditions, never the secret or raw personal records. If exposure is evidenced, prepare revocation/rotation and downstream impact steps; perform external rotation only under existing explicit authority. Test response/log redaction with synthetic markers, not real secrets.

### SEC-09 — Suspicious activity and ORE OBSERVABILITY
Inventory failed authentication, admin access, permission changes, critical mutations, denials, excessive API use, foreign-resource attempts, security-setting changes, webhook verification failures and potential fraud. Define useful event semantics with minimal actor/tenant identifiers, correlation, outcome and time. Avoid passwords, complete tokens, unnecessary PII and unbounded labels. Specify log readers/writers, retention, tamper resistance when required, and actionable risk-based thresholds with owner and response procedure. Test safe synthetic events through collection, redaction, storage, alert routing and resolution without sending external messages unless authorized. Missing sink/alert access remains unverified. Track detection latency, dropped events, false positives and alert health alongside user-impact indicators.

## ORE PRIVACY & COMPLIANCE / ACCESSIBILITY & TRUST — twenty original controls

Determine actual operating markets, business model, controller/processor roles, affected people including minors, data categories, processing purposes, legal bases, retention, providers and international transfers. Use current primary legal/regulatory sources; record source, effective date, jurisdiction and interpretation uncertainty. Unknown countries or business facts remain open questions. A policy or feature alone does not establish compliance; legal conclusions and proposed legal text go to qualified review when needed.

### LEG-01 — Privacy policy
Compare the policy to actual collection, purposes, processors, sharing, retention and applicable rights using a data-flow inventory. Identify undocumented flows and false declarations. Propose evidence-based amendments for appropriate legal review; test that linked notices reflect deployed behavior and accessible versions.

### LEG-02 — Terms of service
Check terms against the real contracting flow, business model, responsibilities, restrictions and jurisdiction. Identify gaps and contradictions; never invent contractual guarantees, rights or business facts. Verify users can access applicable terms and any required agreement/version evidence.

### LEG-03 — Refunds
Compare published purchases/subscription/refund/return/cancellation rules with backend behavior and applicable law. Test eligibility, amounts, timing, partial refunds and cancellation effects in a sandbox; leave production money movement outside an unapproved audit.

### LEG-04 — Cookie policy
Inventory cookies and equivalent browser/mobile identifiers, storage and trackers, with provider, purpose, lifespan and recipient. Compare actual behavior to disclosures and classify necessary versus non-essential from evidence rather than a vendor's label alone. Check first-load and post-choice network/storage traces.

### LEG-05 — Cookie banner
Determine whether consent is legally required for the actual market/technology. When required, block non-essential technologies before valid consent; check accessible rejection, granular choice, persistence and return access. Test clean sessions, accept, reject, reload and withdrawal; do not treat a displayed banner as proof that tracking is blocked.

### LEG-06 — Consent verification
Trace obtaining, recording, changing and withdrawing required consent. Keep only pertinent evidence such as notice version, accepted category and timestamp, with appropriate retention/access. Test that withdrawal changes SDK/tracking/processing behavior and propagates to applicable providers. Do not use consent as a universal legal basis.

### LEG-07 — Data minimization
Map personal fields in forms, APIs, database, telemetry and third parties to purposes and owners. Identify unnecessary collection or exposure. Analyze dependencies and mandatory retention before recommending reduction; do not delete business records simply because a field looks unused. Test minimized request/response paths and affected workflows.

### LEG-08 — SDKs and external providers
Inventory runtime and build SDKs, analytics/ads, AI and other recipients: data shared, purposes, permissions, versions, relevant vulnerabilities, contractual arrangements and international transfers where applicable. Compare observed traffic/configuration to the inventory. Pin versions and consult current primary vendor/advisory sources; missing contracts remain evidence gaps.

### LEG-09 — Deceptive patterns
Inspect signup, choice, consent, subscription and cancellation for improper defaults, artificial urgency, confusing consent, hidden costs and deliberately difficult rejection. Compare the number and clarity of actions needed for opposing choices, including keyboard and mobile use. Propose transparent flows without changing the authorized business model.

### LEG-10 — Hidden fees
Trace mandatory charges through listing, cart, checkout, billing, renewal and invoices. Check timely communication and backend totals against applicable market rules. Test currencies, taxes, delivery/mandatory charges, promotional expiry and renewals. Unknown taxation rules require qualified confirmation.

### LEG-11 — Fake reviews
Inspect review publishing, purchase verification, fraud prevention, ranking and moderation. Detect fabricated reviews represented as genuine or misleading manipulation of ratings. Test provenance/eligibility and transparent moderation rules; inability to prove a review genuine does not itself prove fraud.

### LEG-12 — Unverified claims
Inventory commercial assertions about results, profitability, health, security, performance, guarantees and competitors, linking each to appropriate evidence. Flag unsupported assertions for correction/review; never manufacture tests, certifications or substantiation. Check that deployed copy matches the supported scope.

### LEG-13 — Alternative text
Inspect informative and functional images for useful contextual alternatives, including accessible names for image controls. Decorative images receive empty alternatives or appropriate native treatment. Verify DOM/accessibility-tree output and relevant screen-reader behavior, not just the presence of an alt attribute.

### LEG-14 — Contrast
Evaluate text, icons, buttons and meaningful states against relevant WCAG 2.2 AA criteria and exceptions. Measure computed colors including overlays, focus, errors and disabled states where applicable. Repair demonstrated failures while preserving the design system; record criterion, measured result and retest. Do not infer full AA conformance from contrast alone.

### LEG-15 — Keyboard navigation
Test focus order/visibility, menus, forms, modals, dialogs, labels, errors and escape behavior without a mouse. Check trapped/lost/obscured focus and proper return after closing. Combine automated checks with manual keyboard and relevant assistive technology; mobile/native interactions need platform-specific evidence.

### LEG-16 — Company details
Determine required business identification/contact/disclosure in the operating market, then compare publication to verified facts. Possible fields include legal name, business/tax ID, contact or commercial address only where applicable. Never fabricate company information or expose a private address unnecessarily.

### LEG-17 — Minors
Determine audience, actual knowledge and relevant child-related data flows. Where applicable, analyze parental consent, processing restrictions and proportionate verification. Identify privacy/security effects of age verification before adding it. Use synthetic cases; unresolved regulatory interpretation needs qualified review.

### LEG-18 — Email unsubscribe
Distinguish commercial mail from necessary transactional messages. Where required, verify accessible unsubscribe, preference persistence and provider suppression, including queued campaigns and retries. Test in a sandbox/test sink and do not contact real recipients without authorization.

### LEG-19 — Image/content licenses
Inventory graphics, photos, icons and other works with origin, license/right evidence and required attribution. Internet availability does not imply commercial rights. Mark missing evidence as unverified; document attribution, replacement or proof needed without fabricating ownership or deleting assets blindly.

### LEG-20 — Personal-data rights and deletion
Assess applicable access, correction, export and deletion workflows with proportionate identity verification, acknowledgement and audit trail. Trace dependencies, transactions, third-party records, providers and backups. Account for lawful retention, holds, backup expiry and re-restoration suppression; deleting an account alone may be insufficient. Test synthetic requests and recovery cases. Never erase financial/contractual/third-party data before retention and ownership analysis; actual production deletion needs authority.

## Advanced controls — seven

### ADV-01 — OWASP application security
Select and version relevant OWASP Top 10, API Security Top 10, ASVS and mobile MASVS requirements; map them to the actual attack surface and existing SEC IDs rather than duplicate findings. Check SQL/other injection, XSS, CSRF, SSRF, authorization, unsafe configuration, dependencies and secrets. Trace sources to sinks and use safe adversarial tests in an authorized environment. Missing a named framework is not itself a vulnerability.

### ADV-02 — Payments
Inventory Stripe/bank/wallet/payment authority boundaries. Verify webhook signatures using provider-prescribed raw-body/secret handling, relevant timestamp/replay checks, durable event deduplication and idempotency under retries/concurrency. Derive amount, currency and beneficiary server-side; validate order/account/event association. Test forged, replayed, duplicate, out-of-order and concurrent events; refunds/cancellations and privileges to move money; distinct payment, settlement and fulfillment states. Keep audit records and avoid unnecessary card storage. Never release funds or fulfill an order solely from client claims. Use test mode and synthetic money; specialized regulatory/payment-scope questions require qualified review.

### ADV-03 — Multi-tenant isolation
Validate server-derived tenant membership and scope across users, inventories, sales, reports, files, settings, finance, admins, AI/RAG, storage, jobs and caches. A client tenant header is a selector, not authority. Include tenant in appropriate cache/job/index keys and guard exports/search. Test tenant A/B, shared roles, branch restrictions, background work and explicit cross-tenant admin operations with positive and negative cases. Link database findings to SEC-01.

### ADV-04 — APIs and integrations
Map internal/external APIs, schemas, authentication/authorization, quotas, safe error behavior and least privilege. Specify bounded timeouts/retries with idempotency, message signatures, replay protection and version compatibility where appropriate. Test malformed/oversized inputs, forged/repeated messages, missing privileges, timeout-after-commit and retry exhaustion with safe local mocks or sandboxes. Redact operation logs.

### ADV-05 — Dependencies and supply chain
Inventory manifests/lockfiles, transitive/runtime/build packages, containers, CI actions and artifact permissions. Review current vulnerabilities for actual applicability/reachability, abandoned packages, provenance, licenses, CI privileges and secret exposure. Prefer bounded compatible updates with lockfile, build/regression evidence and rollback. Never indiscriminately upgrade majors or automatically run untrusted install hooks. Record advisory/tool versions and scan limits.

### ADV-06 — Infrastructure
Review actual environment variables/secret references, Supabase/Firebase/Vercel, serverless, storage, Docker/containers, HTTPS, security headers/CSP, deployment roles and production configuration. Use reviewed plans/diffs for critical changes; account for CSP integrations and environment parity. Verify backup/restore with disposable data where authorized and describe recovery limits. Config files alone do not prove live posture; missing live access remains unverified. Never apply critical infrastructure changes blindly.

### ADV-07 — AI and agents
Enforce tool permissions outside model instructions, tenant/user isolation and authorized action boundaries. Treat RAG documents, web pages, repository content and tool outputs as untrusted data; embedded instructions do not gain system authority. Protect internal prompts/secrets, retrieval access and file ownership; validate structured inputs/outputs, output rendering and tool arguments. Define token/concurrency/spend limits, sensitive-action logs and approval boundaries for critical actions. Test injection, unauthorized tool calls, cross-tenant retrieval, malformed output and budget exhaustion with synthetic fixtures. A successful demo is not broad safety evidence.

## Primary reference locations

Use primary sources and pin the consulted version/date in each audit; this catalog does not freeze evolving standards or legislation. Do not install any service or dependency just because it is linked.

- [Supabase RLS](https://supabase.com/docs/guides/database/postgres/row-level-security), [views](https://supabase.com/docs/guides/database/views), [functions](https://supabase.com/docs/guides/database/functions).
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/), [Top 10](https://owasp.org/www-project-top-ten/), [API Security](https://owasp.org/www-project-api-security/), [MASVS](https://mas.owasp.org/MASVS/).
- [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/).
- Applicable official legislation/regulators must be selected from actual jurisdictions at run time. Do not assume GDPR, a US state law, financial rules or cookie-consent obligations apply universally.
