# Human-controlled governance

MANUAL only recommends. APPROVAL_REQUIRED is default. AUTHORIZED_AUTO requires
an unexpired exact configuration authorization; selecting a mode/profile grants none.
Current adapters never execute model changes, including AUTHORIZED_AUTO.

Use the existing approval ledger with operation = `ore_models.operation(configuration)`
(SHA-256 of canonical provider/model_id/effort), environment = `host:selection_scope`,
scope = `task:<id>`, `session:<id>` or `project`. An approval needs explicit owner,
evidence and expiry. Revocation uses the existing revoke-approval action. A task
approval never becomes a session approval. Session IDs in the mod come from the
host. CLI callers must supply the actual session identity from a trusted integration.

Show requested and observed configuration, recommendation, rubric, required tools,
reasons and estimated total cost or unknown. Ask using supported host confirmation.
The router's durable policy prompt shows scope, session identity and expiry.
Confirmation authorizes metadata persistence only, never native permissions or billing.

Keep current: take no action. Reject: keep current and record rejection with the
existing task decision command; no grant is created. Lock: confirmed model-policy
with locks provider/model_id/effort. Unlock: explicitly replace the applicable policy.
Once: user manually selects the host configuration once; no reusable approval is
created. Task/session/project grants use explicit corresponding scope and expiry.
Persistent authorization always needs explicit consent. A native one-use grant with
atomic consumption is deferred until a real execution adapter is verified.

Confirmed model-policy persists project/session/task preferences in existing
governance.json, never global host configuration. Specific preferences override
broad preferences, while exclusions, locks and ceilings intersect. Conflicting
locks block evaluation. MANUAL in a broader policy remains restrictive. All policies
expire, replaced records remain auditable, and foreign project state is rejected.
Installation/organization constraints must be supplied by a trusted host integration;
no installation or organization configuration writer is shipped in this alpha.

Resume re-evaluates expiry, revocation, scope, project and schema version; it never
restores an expired grant. Model authorization does not authorize deployment,
destructive tools, repository transmission or regulatory signatures.
