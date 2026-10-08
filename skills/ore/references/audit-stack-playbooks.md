# Technology, business and jurisdiction playbooks

## Discovery before choosing checks

Inspect version-control status, package manifests/lockfiles, routes, middleware, schemas/migrations/rules, deployment/CI configuration, tests and relevant documentation. Distinguish detected components, inferred architecture and unknown live settings. Do not execute untrusted project scripts or install dependencies until their behavior and authorization are understood. Record runtime versions, environments, auth provider, trust/tenant model, public endpoints, data classification, payment/AI/file paths and existing check commands. Run the cheapest safe relevant baseline, then select catalog IDs and gates. Reuse project test runners and providers; tools are optional, not implied integrations.

## Stack-specific execution

| Detected stack | Inspect | Safe verification and limitations |
| --- | --- | --- |
| Angular / TypeScript | Routes/guards, interceptors, template bindings, sanitization bypasses, forms, client configuration and backend contracts. | Existing build/typecheck/unit/E2E; prove server denial even when client guards are bypassed; render keyboard/error flows and response redaction. Never place secrets in client environments. |
| Next.js | Route handlers, server actions, middleware, server/client boundaries, environment exports, caching and data serialization. | Test each server entry independently for authorization; tenant/user cache isolation and rendering XSS; test relevant deployed runtime separately when local behavior differs. Middleware alone is not proof of endpoint authorization. |
| Supabase / PostgreSQL | Exposed schemas, grants, tables/views, policies, RPC, Storage, privileged paths and auth claims. | Local disposable database and real-role positive/negative SELECT/INSERT/UPDATE/DELETE/RPC/storage tests; migrations plus authorized schema introspection. An absent database leaves live RLS unverified. Do not use service_role to prove user isolation. |
| Firebase | Firestore/Realtime Database/Storage rules, Auth, Functions, Admin SDK/IAM and App Check where used. | Emulator rules tests for anonymous, user, tenant and admin behavior plus function/API tests. Rules do not protect privileged Admin SDK paths; separately prove function authorization. Do not retrofit PostgreSQL RLS language onto Firebase. |
| Python | Framework routes/dependencies, serializers, ORM/raw SQL, parsers/uploads, tasks, auth and CORS middleware. | Existing pytest/unittest/lint/type checks; integration tests against ephemeral stores; check raw queries, SSRF destinations, parser resource limits and safe errors. |
| Docker / Vercel / serverless | Images/users/capabilities, build inputs, environment/secret scope, logs, headers/CSP, deployment roles and recovery. | Validate configuration, reviewed infrastructure plans, existing container/build checks and local header tests; use authorized live read access only. Local config cannot establish actual cloud IAM or backups. |
| Android / iOS / Flutter | Actual native/shared stack, secure storage, permissions, deep links, embedded web content, network transport, SDKs and offline cache. | Existing native/Flutter tests, emulator/device flows, permission denial and logout/cache cleanup; applicable MASVS checks plus backend authorization. State missing platform tooling rather than inferring a device pass. |
| Stripe / bank / wallet | Authoritative order/ledger state, webhook routes/signatures, secrets, money privileges and payment/settlement/fulfillment transitions. | Test-mode provider or local mocks: tampered amounts/currency/beneficiary, forged webhook, duplicate/concurrent/reordered events, retries and partial failure. No production charge/refund/fund release in an audit without authority. |
| Third-party APIs | Contracts, credentials, request/response handling, quotas, retry/timeout/idempotency and callbacks. | Mocks or permitted sandboxes for authentication failure, malformed data, replay, timeout-after-commit and bounded retries; actual vendor limits remain unknown without current evidence. |
| AI / agents / RAG | Model/tool schemas, server enforcement, retrieval ACLs, file ownership, rendering, logs and budgets. | Existing representative/adversarial evaluation with synthetic tenant data, injection, denied tool execution and quota exhaustion; keep secrets out of prompts/traces and do not run dangerous proposed tools. |

Select relevant commands from the repository rather than inventing a script name. Record exact command, environment, artifact revision, outcome and what the check proves. Runtime/tool incompatibility is a blocked check; a static observation is not a substitute for an available runtime check.

## Business priorities

- **Marketplace / commerce:** buyer/seller/order boundaries, price provenance, payments/refunds, fraud/reviews, PII and consumer transparency.
- **ERP / POS / B2B SaaS:** company/branch/employee/role isolation, inventory/sales/report integrity, shared permissions, billing and tenant-scoped cache/files/jobs.
- **Logistics / delivery apps:** location purpose/retention, route/driver assignment, delivery evidence uploads, customer addresses and role-scoped tracking.
- **Finance / digital wallets:** money movement authority, ledger integrity/reconciliation, concurrent/replayed operations, audit trails, recovery and jurisdiction-specific specialist review. Never invent a financial license or certification.
- **AI platforms:** tenant retrieval and tool authority, personal-data/provider boundaries, budget controls, abuse detection and output safety.

Models may overlap; use actual operations rather than a product label to determine coverage.

## Jurisdiction procedure

1. Establish operating entity, locations/markets, customer/user locations and types, minors, data categories, purposes, vendors/transfers and commercial/financial operations from evidence. Project language or currency alone cannot establish jurisdiction.
2. Retrieve current authoritative legislation/regulator guidance for candidate obligations. Record source URL, version/effective date and facts supporting applicability. Do not claim compliance from this skill's checklist.
3. Map requirements to relevant LEG/SEC/ADV controls, owners, implementation and operating evidence. Separate a design gap, unavailable evidence and a legal interpretation question.
4. If facts/sources are missing, continue independent technical checks and mark affected legal conclusions pending. Prepare factual policy amendments or requirements questions for qualified review; never invent business identities, contractual terms, licenses or guarantees.
5. Evaluate consent, retention and deletion conflicts before changing behavior. Destructive deletion, changes to live configuration and consequential financial operations require appropriate existing authority at the action boundary.
