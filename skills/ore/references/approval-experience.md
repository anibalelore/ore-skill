## Approval mode

ORE defaults to host-managed permissions: it adds no confirmation dialogs for tool calls or explicitly invoked runtime commands. Existing validation, path restrictions, revision checks and native host permissions still apply. An explicit runtime command authorizes its declared operation; this mode does not authorize unrelated actions.

ORE approval dialogs have been removed. Legacy `approvalMode` options are ignored, including `"ask"`. Permissions are handled by the host. User authorization persists for the requested task: do not ask conversationally to confirm the same instruction again. Clarify only missing scope needed to execute it.

# Human-friendly authorization

Before consent, show action, reason, tool/platform, project and actual or unknown
destination, affected resources, risk/impact, reversibility and required permissions.
Use concise natural language; do not turn supplied descriptions into trusted facts.

Offer progressive summary, impact and complete technical details using supported
host interactions. Production, permissions and unknown external targets are high
risk; destructive/irreversible actions are critical. Keep dangerous exact commands,
SQL and critical destinations visible before approval. Unknown controls remain
unverified; no audit-table immutability or effective RLS claim without evidence.

Preserve complete exact parameters and command/SQL bytes; decode escaped newlines
only for prose when appropriate. Do not silently truncate, hide dangerous suffixes
or approve a redacted operation. Block unpresentable/oversized requests and ask for
a smaller scoped action. Keep secrets out of new approval records and logs.

Reviewing details is not approval. Confirm the exact operation, with valid scope
and expiry; reject, dismissal, stale state or presentation failure grants nothing.
Do not treat free-text approval before exact review as consent. Summaries cannot
grant tools, bypass native restrictions or reuse revoked/expired approvals.

Use only host-supported options. Persistent or previous-policy approval requires
real scope enforcement; otherwise offer one operation and leave native permission
policy controls to the host. The existing approval-ledger writer remains authoritative
for durable decisions. Model-router consent for metadata does not change a model;
department ownership and cost observations do not expand authorization.
