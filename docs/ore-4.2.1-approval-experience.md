# ORE 4.2.1 — Human-Friendly Approval Experience

Prerelease: **4.2.1-alpha.3**. The shared presenter improves real ORE dialogs in
guard, approval-ledger, model-router, browser consent and scoped Write/Edit reviews.
Inventory remains 29 skills, 28 mods and 9 departments.

## Progressive disclosure

1. Summary: natural Spanish action and reason, platform, project and declared target.
2. Impact: resources, estimated risk, reversibility, permissions and unverified controls.
3. Technical details: complete exact JSON parameters, with real commands/SQL also
   displayed in code fences that safely accommodate backticks in the contents.

All requests first show a prose summary without commands, SQL or raw parameters.
Requests first offer “Rechazar” and “Revisar detalles”; after mandatory review, the full-details
dialog offers “Aprobar una vez”. Free text cannot skip the required details step.
Reviewing details grants nothing. The selected operation reaches `next(e)` unchanged.
High/critical actions also require this review: their critical details remain visible
on the second screen before an approval option becomes available.

For a ledger/policy mutation, one approval authorizes one write of the exact scope,
expiry, configuration and parameters shown. That written policy may last for its
explicitly authorized scope; it grants no native permissions or model switching.
No additional persistent or “approved by policy” option is offered because the
guard cannot prove and atomically enforce that native scope. The host's own policy
choices remain available in its native permission UI. Existing ledger expiry,
revocation, audit events and project isolation remain authoritative.

## Risks and exact content

| Risk | Classification |
| --- | --- |
| Bajo | Known-target operations without recognized mutation/external impact |
| Medio | Local file/schema changes and ORE metadata writes |
| Alto | Production, permissions, cloud/publication, execution with unknown destination |
| Crítico | Destructive SQL, mass deletion, force push, hard reset, infrastructure destruction |

Executable arguments and declared destinations determine risk. Descriptions and
reasons cannot downgrade an action; a benign tool name cannot hide destructive SQL.
This is conservative pattern analysis, not a shell/SQL interpreter, dry run or proof
of sufficient permissions. Hidden scripts, dynamic commands and indirect effects
still require host review. Custom guard patterns extend built-in protections.

Only prose normalizes literal escaped newlines. Command/SQL bytes, parameters,
evidence, diffs and escapes remain unchanged in the full details. Commands or SQL
appear once in a code block, followed by the remaining exact JSON parameters. User-supplied
descriptions stay in the parameter block rather than becoming ORE instructions.

Nothing is silently truncated. ORE blocks a request when the full rendered details
exceed its conservative 12,000-character limit. This is an ORE policy, not a guaranteed
host viewport limit. Split the operation and request consent again. Inline credentials,
terminal/bidi control characters and explicitly insufficient permissions also block
ORE approval. No redacted action is approved as though reviewed completely. Inspect
blocked originals in the secure host tool view and resubmit safely; ORE adds no
raw-action state/log. The native host's existing transcript policy still applies.
Presentation failure, dismissal, unknown responses, action/state
changes or aborted calls deny guarded execution.

## Supabase example

An actual CREATE TABLE public.activity_log request with a declared isolated project
produces this summary, followed by review of the full SQL before approval:

```text
Acción: Crear tabla de auditoría
Plataforma: Supabase
Entorno: isolated-test (declarado; sin verificar)
Recursos: public.activity_log y el identificador del proyecto
Impacto: Nueva estructura de datos o cambio de esquema
Riesgo: Medio
Verificar RLS, privilegios, autoría, integridad y protección frente a modificaciones
Estado: Pendiente de aprobación
```

Absent destination becomes “Detectar y verificar” and risk Alto. Production also
elevates risk to Alto. No immutability, working RLS, effective privileges, protected
authorship or integrity is claimed without tests. This update creates no Supabase table.

## Supported host integration

Existing `tool.call`/`command.run` hooks and `$.ui.ask` provide native interaction.
The engine alone draws Claude's native permission dialog. This update compacts
ORE's questions; it cannot hide or replace the host's command/SQL permission view.
Guard and scoped Write/Edit reviews now attach a concise action, platform, project,
destination and risk line with `$.ui.notice(e.tool_use_id, text)`. The engine binds
it to that pending call and removes it when the call resolves. A failed annotation
denies the reviewed operation; it grants no permission and never replaces exact
content with a summary. Command-only ledger/model decisions have no native tool
permission dialog to annotate.
The repository's generated 2.1.295 declarations document the native AskUserQuestion
dialog, 2–4 option labels, free text and dismissal/noninteractive rejection. Host calls
remain in register modules for static permission auditing; the shared engine is pure.

[Permissions](https://code.claude.com/docs/en/permissions) remain host-enforced.
[Hooks](https://code.claude.com/docs/en/hooks) distinguish PreToolUse from
PermissionRequest. ORE neither installs allow-returning PermissionRequest hooks nor
updates native allow rules or permission modes. [Plugins](https://code.claude.com/docs/en/plugins)
provide packaging; ORE's existing optional-mod marketplace remains unchanged.
Official pages were fetched on 2026-10-09. The working mods documentation paths are
[events](https://code.claude.com/docs/en/plugins/mods/events),
[interface](https://code.claude.com/docs/en/plugins/mods/interface) and
[API](https://code.claude.com/docs/en/plugins/mods/api). The interface guide explicitly
excludes permission prompts from render sites. Exact annotation contracts use the
checked-in 2.1.295 SDK declarations and installed manifest validator.

The existing ledger writer records durable approvals/revocations. Guard choices stay
ephemeral in the native interaction and create no reusable grant. Departments retain
task ownership, cost-controller supplies reported usage, and model-router shares the
same consent presenter. No new state, billing or permission subsystem is introduced.

Use existing installation/commands and reload the updated optional mod on a compatible
host. There is no decorative browser UI, fake approval button or background process.
Installed Claude Code now reports **2.1.295**, matching the checked-in API contract.
Real interactive rendering remains separate from manifest/type/handler validation.
Native `ore-guard-status`, `ore-approval-ledger-status` and `ore-model-router-status`
successfully launched through their actual plugin packages with no model inference.
The router observed `claude-sonnet-5-5`, cost USD 0, and modelChanged false; this is
a status observation, not a routing switch or provider benchmark.
No global upgrade, paid provider call, production
action, publication or model switch is performed. Previous routing limitations remain.

## Validation

Tests cover long/excessive actions, multiline SQL, escapes, production, unknown
resources, insufficient permissions, secrets, rejection, expired approvals, presentation
failure, state/action races, safe fences and custom-pattern preservation. Existing
state, regulatory, browser and runtime regressions remain. Exact final results are
recorded in UPDATE_REPORT.md.
