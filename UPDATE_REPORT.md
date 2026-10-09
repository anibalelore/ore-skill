# ORE 4.0.0-alpha.1 Update Report

## Native approval context — 4.2.1-alpha.3 — 2026-10-09

Guard and scoped Write/Edit reviews now call the supported `$.ui.notice` API with
the same pending tool-use ID and a plain-language action/platform/project/target/risk
summary. This annotates the native dialog, which only the host can draw. Raw
commands/SQL remain in the host view and mandatory technical review. ORE's first
question groups metadata to reduce visual repetition. Annotation failures deny the
reviewed action. No allow rules, permission modes or executable parameters change.

Validation: 140 tests passed; package inventory and guard/ledger/router TypeScript
checks passed. Guard manifest validation recognizes `$.ui.notice`. Native notice
rendering was verified with the actual handlers and a deterministic host adapter;
live interactive appearance remains unverified. Official mods events/interface/API
documentation was fetched through the supported `/plugins/mods/` paths.

## Approval presentation correction — 4.2.1-alpha.2 — 2026-10-09

The initial ORE question now contains only a prose summary for every risk level.
Exact command/SQL review is mandatory before approval becomes available; free-text
approval cannot skip it. Commands/SQL appear once, followed by complete remaining
parameters. Native Claude permission dialogs remain engine-owned and unchanged.

Validation: 138 tests passed; package inventory validation passed (29 skills,
28 mods); guard, approval-ledger and model-router type checks and native manifest
validation passed. Actual interactive viewport rendering remains unverified.

Updated the separate installed marketplace source after checking it against the
clean baseline and backing up originals under `.ore/approval-alpha2-backup`.
All seven already-installed optional plugins were updated successfully through
`claude plugin update` to alpha.2. A Claude Code restart is required to apply them.
Approval-ledger is available in the updated source but was not already installed.

Date: 2026-10-08 (America/Denver).

## Result and release decision

Delivered a reviewable prerelease: 26 existing skills, six preserved display/guard
mods and 19 explicit runtime command adapters. README now explains the product,
installation, existing mods, new adapter limits and the update history. Existing
skill instructions changed only in version metadata; their scoped execution
policies and evidence requirements remain intact.

This is **not stable ORE 4.0.0** and does not fulfill every autonomous capability
in the master prompt. The capability matrix and acceptance contract identify the
unfinished behavior. The initial review was prepared without a commit or push. The user subsequently
authorized committing and pushing this prerelease to Git. No tag, deployment,
package publication or installation into the user's plugin registry is included.

## Implemented behavior

- Governance: confirmed path scopes/living rules, replacement, revocation,
  expiring exceptions, task-bound approval metadata, project identity and
  versioned internal events. Only ore_state.py writes .ore/governance.json,
  under the existing cross-process lock and expected task/governance revisions.
- Declared Write/Edit restrictions: filesystem resolution, reserved .ore paths,
  traversal/drive-relative/network spelling rejection, post-dialog revision
  rechecks, and explicit handling of missing/malformed governance. Runtime
  failure with a valid rule denies the declared edit. No shell inspection.
- Flow analysis: supplied schema, identities, cardinalities, provenance,
  transitions, permissions, idempotency, partial quantities and recovery.
  Synthetic factory/marketplace fixtures cover QA, logistics, multivendor
  ordering, cancellation and refunds. Model-only results leave CHANGE_IMPACT
  and TESTS pending and do not write evidence gates automatically.
- Flow watch: supplied authorized telemetry produces evidenced alerts; absent
  telemetry remains disconnected. No causal certainty or automatic repair.
- First Contact: optional real Playwright exploration in a bounded explicitly
  isolated loopback application. Outcome criteria remain outside action
  selection. Optional explicitly approved synthetic screenshots mask editable
  fields and export redacted action manifests outside .ore, with at most 24h
  retention and scoped expiry cleanup. No production screenshots or mutation
  requests; automated redaction cannot guarantee all personal data is removed.
- Supporting adapters: explicit bounded plans, test-map selection with mandatory
  broad fallback on incomplete coverage and preserved critical tests, contract
  comparison, declared review validation, local PR drafts, observed diagnostic
  summaries and matching-run efficiency comparisons. Native cost/context/project
  adapters need no process permissions; worktrees use fixed read-only Git argv.

## Validation

- Baseline before changes: **48 unittest tests passed**, package validation
  passed; clean Git state at **4ed4df85**.
- Final browser-enabled suite: **84 unittest tests passed**, including original
  state/form/audit/catalog coverage, real native TypeScript handlers, flow
  fixtures, governance and actual Chromium exploration/screenshot artifacts.
  Without optional Playwright, the browser test skips explicitly.
- Package validation: **26 skills, 25 mods, 4.0.0-alpha.1**. It verifies inventory,
  versions, local references, canonical readers, audited module templates and
  byte-identical bundled Python sources.
- **25 TypeScript checks**, **25 claude plugin validate checks**, and **25 real
  --plugin-dir status-command launches** with isolated Claude Code **2.1.295**.
  Status-command launches are smoke tests, not proof of every adapter operation.
- Real native ore-flow-intelligence command analyzed the factory fixture:
  valid=true, continuity_verified=true; CHANGE_IMPACT and TESTS stayed pending.
- Independent review reproduced three errors (reserved-path normalization,
  missing broad-test blocking, estimated-counter savings), then verified their
  fixes and the 10 runtime tests. Review also confirmed revision rechecks,
  task-binding safeguards and minimum native process permissions.
- One full-suite regression rejected legitimate authoritative-list JSON arrays;
  fixed by applying object validation only to active/task state. Full suite passed.

Reproduce core validation:

```text
python scripts/build_mods.py
python scripts/validate_package.py
python -m unittest discover -s evals -p "test_*.py" -v
python scripts/validate_mods.py --claude <2.1.295-executable> --tsc <typescript-executable>
```

Optional browser dependencies were installed only in temporary directories:
Playwright **1.63.0**, Chromium **153**. Set PYTHONPATH to the temporary dependency
folder and PLAYWRIGHT_BROWSERS_PATH to its browser folder for browser-enabled
validation. The isolated Claude runtime leaves installed **2.1.267** unchanged.
Node **24.19.0** and Python **3.12.10** were used. Codex **0.162.0-alpha.2** was
observed, not end-to-end certified. No behavior claims were tested for Opus,
Fable, Astra or other named models; no actual model token savings are claimed.

## Remaining requirements for stable ORE 4

- A persistent autonomous controller that executes bounded turns and verifies
  progress; the current autopilot only validates a caller-supplied plan/budget.
- Worktree creation, collision-aware parallel execution and reviewed merging;
  the current adapter only reads topology.
- Automatic contract/dependency/application discovery and integration with
  artifact-digest-bound completion gates; current engines validate supplied data.
- Live telemetry subscriptions, operational alert routing and authorized replay;
  the current watcher analyzes supplied records and never repairs production.
- Broader user profiles, independent fresh-user retesting, real-app write flows,
  visual comparison, accessibility checks and preview/release certification.
- Native asynchronous independent reviewer orchestration, compaction handling,
  actionable budget control, validated project routing and pull-request delivery.
- Independently sourced cross-model token/cost benchmarks and complete host
  compatibility certification. Comparative counters remain declared input.

These are explicit partial capabilities, not hidden placeholders or certified
outcomes. Malformed optional governance intentionally disables its layer;
filesystem aliases and review-to-execution races remain limits. High-impact
approval records never bypass host permissions or the original action guard.

See [adapter inventory](docs/runtime-mods.md),
[capability matrix](docs/ore-4-capability-matrix.md),
[acceptance contract](docs/ore-4-acceptance.md),
[First Contact](docs/first-contact.md) and [flow engine](docs/flow-intelligence.md).

---

# Historical ORE 3.0 report (preserved)

# ORE 3.0.0 Update Report

Date: 2026-10-08 (America/Denver).

## Result

Added six optional, independent Claude Code mods and a local `ore-mods`
marketplace. The domain workflows are retained. The lead and all specialists now use
minimum sufficient execution; audit detail loads conditionally. Codex and other
hosts use these skill instructions but do not load the optional mods. No commit, push, tag,
installation into the user's plugin registry, or publication was performed.

The sole shared behavior extension is explicitly opt-in: ore_state.py update
accepts --active-specialist, --department and --domain-lead together, records
identity at the new revision and appends a structured transition event.
Existing commands and old schema-v1 tasks retain their behavior.

## API verification

The installed CLI was 2.1.267. An isolated npm installation of 2.1.295 was
created under the user's temporary directory, leaving the installed CLI intact.
/plugin-types was unavailable in both versions, including an interactive
2.1.295 session. Loading an empty probe interactively with --plugin-dir generated
the actual API declarations. An unedited copy is preserved in mods/api-types.
All implementation events and calls were checked against that snapshot.

Reviewed the official overview/create/reference/admin pages and the official
Anthropic examples, including blast-radius, sec-default and agents-md. The
guard uses the typed ui.ask method instead of the example's process-based
waiting and shell dry runs. No mod uses network, model, process, filesystem
writes, persistent store, environment or settings APIs.

## Validation

- Python package validator: 26 skills, six mods, version 3.0.0; passed.
- Full unittest discovery: 48 tests passed, including nine new mod regression tests.
- claude plugin validate: all six mods passed; local marketplace passed.
- TypeScript 5.9.3 against generated 2.1.295 types: all six passed.
- Native claude plugin test: 18 tests passed across the six plugins. These include
  guard cancellation/approval via mocked AskUserQuestion, and rendering on both
  terminal/Desktop while preserving the existing band.
- Each mod loaded separately with claude -p /<name>-status --plugin-dir mods/<name>.
  Each returned the persisted workspace handoff without requesting a model.
- Combined interactive load using six repeated --plugin-dir flags: /plugin
  showed `6 mods active`; progress, gates and the old-state ORE lead fallback
  rendered together in the terminal.
- No destructive operation was executed; guard execution was mocked. A mistaken
  initial combined CLI invocation passed a directory as prompt; a model request
  was rejected by the account's organization policy. The corrected interactive
  invocation loaded all six without a model turn. Live model-driven end-to-end
  actions were not exercised; native host tests cover those event paths offline.

## Explicit limits

- CLI minimum is documented as 2.1.287; this release was tested on 2.1.295 only.
- State updates are polled every second, not delivered by a filesystem watcher.
  Revisions identify changes, not the writer/window.
- active.json is a pointer. The reader also reads the task record and checks
  the pointer again; absent/corrupt/unsupported state is inert.
- Gates warn at turn end and explicit Bash completion commands without reading
  conversational claims. ore_state.py still enforces actual completion.
- Guard reports declared arguments and labels impact as unmeasured. Patterns
  cannot prove script/alias/remote effects. Pattern options replace defaults;
  invalid options require confirmation and oversized arguments do too.
- State has no approval/scope-exception ledger, so matched actions request
  confirmation each time an active or blocked task exists. Confirmation never
  bypasses the host's permission chain; headless confirmation denies actions.
- Specialist display reflects recorded assignment, not inferred execution.
  The existing skills do not automatically populate the opt-in identity fields.
- UI availability/layout may hide or scroll the band. Explicit status commands
  provide headless handoffs. Mods run as the user and are not sandboxed.

## Review scope

Implementation: mods/, evals/mods_harness.mjs, evals/test_mods_state.py,
skills/ore/scripts/ore_state.py, scripts/validate_package.py.
Documentation: README.md, CHANGELOG.md, this report and mods/README.md.
Skills: minimum sufficient execution policy in the core, efficiency lead and
24 domain specialists; both root manifests and skill versions remain 3.0.0.
The Codex marketplace is unchanged; the Claude marketplace lives under mods/.

## Token-efficiency instruction update

Applied the skill-creator workflow to the core and all specialists. Moved the
original audit mode/surface section verbatim (adjusting relocated links) into
references/audit-modes.md, loaded only when relevant. Shortened the duplicated
specialist index; the detailed routing and domain workflows remain accessible.
Added scoped reads, incremental handoffs, bounded evidence returns and reuse
only of unchanged validation. Model choice/reasoning settings, acceptance
criteria, risk-sensitive coverage and independent reviews are preserved.
The lightweight policy runs within each owning lead; it does not require an
extra efficiency agent or authorize delegation.

Measured source size against the working tree immediately before this update:

- Core SKILL.md: 11,446 to 9,895 characters (13.6% smaller).
- Core plus backend SKILL.md: 14,097 to 12,807 characters (9.2% smaller).
- Domain cards add a small standalone execution rule; the dedicated efficiency
  skill expands its guidance and is not loaded for every ordinary task.

These are source-context measurements, not actual tokens, cache savings or
billed usage. Actual token savings: unmeasured. End-to-end behavioral equivalence
on the named model families: unmeasured. The existing 48-test suite passes,
all 26 skills pass skill-creator validation, and original domain bodies/audit
rules were checked for preservation. Acceptance scenarios for a future same-task,
same-model/gates benchmark are in evals/context-efficiency-scenarios.md.
No runtime model settings, state schema or mod behavior changed in this update.

## Previous 2.4.0 report (historical)

# Informe de actualización de ORE

Fecha: 2026-10-08, America/Denver. Repositorio: `C:\Users\aniba\Downloads\ORE-SKILL`.

Se actualizó el ORE existente de 2.3.0 a 2.4.0. El nombre «ORE v2.0» del pedido se trató como especificación de capacidades, evitando degradar la versión ya instalada en este repositorio. La implementación y la validación local están realizadas; la aceptación de comportamiento integral en una aplicación real sigue pendiente.

## Descubrimiento y compatibilidad

- Entrada directa: `SKILL.md`; protocolo canónico: `skills/ore/SKILL.md`.
- Paquete existente: 26 skills, dos manifiestos, catálogo de marketplace, políticas/UI en `agents/openai.yaml`, referencias compartidas y evaluaciones.
- Herramientas existentes: `ore_state.py` para estado/revisión/progreso/handoff; `validate_form_contract.py` para contratos de formularios; `validate_package.py` y unittest para validación.
- Ya existían seguridad/privacidad, cumplimiento, observabilidad, accesibilidad, riesgos L0–L5, revisión de impacto, memoria, contratos de formularios y reparación iterativa. Se conservaron y se enlazaron al catálogo único.
- Faltaban los IDs SEC/LEG/ADV completos, siete modos de petición explícitos, equivalencia P0–P3, estados de hallazgos y un límite de cinco iteraciones. El ciclo anterior se describía como acotado pero no tenía ese límite numérico.
- El árbol de Git estaba limpio al comenzar. No se cambiaron el esquema de estado, scripts de estado/formularios, los nombres/directorios de skills, las políticas de invocación, las interfaces YAML ni el marketplace. Los demás skills recibieron solamente el incremento coherente de versión.
- No se encontraron copias de ORE en el directorio personal `.codex/skills`, que contenía únicamente `.system`. Se modificó el paquete existente del workspace; no se afirma que otro cliente lo haya instalado/recargado. La lista de skills de esta conversación no se actualiza mediante la edición de archivos.

## Integración realizada

Las cinco capacidades son pases internos del coordinador ORE y comparten alcance, registro de hallazgos y evidencia. Los especialistas originales continúan disponibles; no se crearon cinco agentes independientes.

| Capacidad | Integración |
| --- | --- |
| ORE SECURITY | SEC-01–09, controles avanzados aplicables y lead de seguridad existente. |
| ORE PRIVACY & COMPLIANCE | LEG aplicables, jurisdicción real, evidencia de operación y lead de gobernanza existente. |
| ORE ACCESSIBILITY & TRUST | LEG-09–15, precios, reseñas, afirmaciones, contenido y pruebas accesibles. |
| ORE OBSERVABILITY | SEC-09, registro mínimo seguro, retención/acceso, alertas verificables y operaciones existente. |
| ORE AUTOFIX & VALIDATION | Hallazgos confirmados, autorización vigente, retest/regresión, reauditoría, cinco iteraciones y checkpoint. |

Se documentaron 36 controles únicos: SEC-01–09, LEG-01–20 y ADV-01–07. Cada sección incluye decisiones de aplicabilidad, aspectos a inspeccionar y evidencia/pruebas pertinentes. Los playbooks cubren Angular, Next.js, TypeScript, Supabase/PostgreSQL, Firebase, Python, Docker/Vercel/serverless, plataformas móviles, pagos, APIs e IA; las prioridades comerciales incluyen marketplaces, ERP/POS, SaaS B2B, logística, comercio y finanzas.

`ORE audit`, `security`, `compliance`, `accessibility`, `fix`, `loop` y `report` son modos expresados en lenguaje natural al invocar `$ore`, no ejecutables nuevos. Auditoría por defecto no autoriza reparaciones; fix/loop autoriza cambios pertinentes en el repositorio y respeta los límites de acciones externas. Las comprobaciones cotidianas son proporcionales a la superficie modificada.

Se conservó la severidad anterior como alias: Critical/High/Medium/Low ↔ P0/P1/P2/P3; los riesgos operacionales L0–L5 siguen separados. Los estados `suspected`, `confirmed`, `fixed_unvalidated`, `resolved` y `accepted_risk` no se confunden. Riesgo aceptado no equivale a reparación. Las pruebas omitidas o antiguas no permiten resolver un hallazgo.

El nuevo validador JSON comprueba consistencia, referencias de evidencia, cobertura integral y límite de iteración. No es un escáner, motor de reparación autónomo, verificador de la verdad de la evidencia ni intérprete de legislación. El ciclo de auditoría es el procedimiento del skill, ejecutado por el agente con las herramientas reales del proyecto.

## Archivos modificados y añadidos

| Archivos | Cambio |
| --- | --- |
| `skills/ore/SKILL.md` | Cinco capacidades, siete modos y revisiones durante desarrollo cotidiano. |
| `skills/ore/references/audit-and-improve.md` | Catálogo compartido, P0–P3, evidencia/estados, validación y parada del loop. |
| `skills/ore/references/quality-gates.md` | Asociación de IDs a gates existentes y límites de las excepciones. |
| `skills/ore-security-privacy/SKILL.md` | Reutilización del catálogo, playbooks y reportes. |
| `skills/ore-compliance-governance/SKILL.md` | Reutilización LEG, aplicabilidad jurídica y evidencia real. |
| `skills/ore-delivery-operations/SKILL.md` | Integración del pase de observabilidad de seguridad. |
| `skills/ore/references/audit-controls.md` — nuevo | Checklist canónico de los 29 controles originales y siete avanzados. |
| `skills/ore/references/audit-stack-playbooks.md` — nuevo | Descubrimiento y pruebas según stack, negocio y jurisdicción. |
| `skills/ore/references/audit-report.md` — nuevo | Plantilla, ledger opcional, evidencia y checkpoint. |
| `skills/ore/scripts/validate_audit_report.py` — nuevo | Validación determinista del ledger, sin dependencias externas. |
| `evals/test_audit_report.py` — nuevo | Diez pruebas de consistencia, cierre, límites y caso sintético. |
| `evals/behavioral-scenarios.md` | Tres escenarios para evaluación posterior de comportamiento real. |
| `scripts/validate_package.py` | Versión 2.4.0, recursos requeridos y links locales de todos los skills/referencias. |
| `SKILL.md`, `plugin.json`, `.codex-plugin/plugin.json`, todos los `skills/*/SKILL.md` | Metadatos coherentes en 2.4.0; configuración restante preservada. |
| `README.md`, `CHANGELOG.md` | Uso, activación, alcance, cambios y limitaciones. |
| `UPDATE_REPORT.md` — nuevo | Este informe de actualización y aceptación. |

## Pruebas ejecutadas

| Verificación | Resultado |
| --- | --- |
| Baseline `python -m unittest discover -s evals -v` | 29 pruebas aprobadas antes de modificar. |
| Baseline `python scripts/validate_package.py` | 26 skills, 2.3.0, aprobado. |
| Suite final `python -m unittest discover -s evals -v` | 39 pruebas aprobadas: las 29 anteriores y diez nuevas. |
| `python scripts/validate_package.py` final | 26 skills, 2.4.0, aprobado; links locales válidos. |
| `skill-creator/scripts/quick_validate.py`, función `validate_skill` | 27 entradas aprobadas: raíz y 26 skills. |
| Conteo del catálogo | 36 encabezados SEC/LEG/ADV, 36 IDs únicos. |
| `git diff --check` | Aprobado; sin errores de whitespace. |
| Caso local sintético multi-tenant | Baseline permite acceso A→B; corrección valida membresía del servidor, niega acceso cruzado/anónimo y preserva acceso propio/colega; revalidación del ledger aprobada. |

El validador de skill-creator inicialmente no pudo ejecutarse por falta de PyYAML. Se instaló PyYAML 6.0.3 únicamente en `.ore/validation-deps` (ignorado por Git), y se cargó en el proceso de validación con Python en modo UTF-8. No se modificó el entorno Python global ni se agregó una dependencia de runtime a ORE. El script nuevo también se ejecutó por CLI dentro de sus pruebas, verificando aceptación de JSON válido y rechazo de JSON inválido sin eco de su contenido.

Las pruebas del ledger comprueban rechazo de cierre sin retest/regresión, evidencia fallida/omitida/obsoleta, sexto ciclo, valores JSON malformados, IDs duplicados/desconocidos y aceptación de riesgos sin autoridad documentada. No prueban que un agente siga las instrucciones ni que una aplicación externa sea segura.

## Criterios de aceptación y pendientes

| Criterio del pedido | Evidencia / estado |
| --- | --- |
| 1. El skill original sigue funcionando | Compatibilidad estructural y 29 pruebas anteriores aprobadas; recarga/uso en host real pendiente. |
| 2. Nuevas instrucciones incorporadas | Implementadas y frontmatter/links validados. |
| 3. 29 controles originales | Documentados una vez en el catálogo canónico. |
| 4. Controles avanzados | Siete documentados e integrados por modos/playbooks/gates. |
| 5. Inspección de repositorio y aplicabilidad | Procedimiento implementado; evaluación integral por agente en aplicación real pendiente. |
| 6. Clasificación de hallazgos | P0–P3 y estados implementados; validación estructural probada; calibración de severidad en casos reales pendiente. |
| 7. Corrección y verificación | Procedimiento integrado; caso sintético probado; reparación de aplicación real pendiente. |
| 8. Loop con parada | Límite/no-progreso/checkpoint documentados; ledger rechaza más de cinco; ejecución autónoma del ciclo en app real pendiente. |
| 9. Salvaguardas de acciones críticas | Preservadas y reforzadas: datos reales, dinero, permisos, infraestructura, servicios pagos y despliegues. |
| 10. Capacidades documentadas | Entradas, referencias, README, changelog y plantilla disponibles. |
| 11. Sin regresiones conocidas | Suite disponible aprobada; no implica ausencia de regresiones fuera de esa cobertura. |
| 12. Pruebas y resultados registrados | Pruebas disponibles ejecutadas y registradas arriba; escenarios de agente 27–29 definidos, no ejecutados. |

Este workspace contiene el paquete del skill, no una aplicación desplegada con base de datos, auth, pagos, dispositivos y país/negocio verificables. El caso sintético es una prueba local y no sustituye una auditoría Supabase/Firebase, una evaluación jurídica o una validación E2E de los siete modos. No se inventaron resultados de esos servicios.

Siguiente paso verificable: cargar el paquete actualizado en el host y ejecutar el escenario 27 sobre una aplicación de prueba autorizada con dos tenants, permisos compartidos y herramientas de prueba disponibles; después evaluar 28–29 y registrar resultados en el ledger y estado existentes. Jurisdicciones y configuraciones reales deben verificarse en cada proyecto. No se considera demostrada la aceptación integral mientras falte esa evidencia.

## Fuentes y alcance de la investigación

Se consultaron ubicaciones primarias de [Supabase RLS](https://supabase.com/docs/guides/database/postgres/row-level-security), [vistas](https://supabase.com/docs/guides/database/views), [funciones](https://supabase.com/docs/guides/database/functions), [OWASP MASVS](https://mas.owasp.org/MASVS/), proyectos OWASP y [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/). Las referencias del skill ordenan verificar la versión vigente al ejecutar cada auditoría. No se adoptó una legislación universal ni se copiaron manuales externos.

Los cambios quedan en el árbol de trabajo local para revisión. Token efficiency: 0 tokens demonstrated; no se contó con una comparación válida de consumo.
# ORE 4.1 regulatory extension — 2026-10-09

Added two regulatory skills and two shared-runtime adapters while preserving the
26 prior skills, 25 prior mods and the ORE 4.0 roadmap. Current prerelease:
4.1.0-alpha.1; inventory: 28 skills and 27 mods.

Implemented reusable signature/binding/session/supersession patterns, regulatory
flow preconditions, six evidence-backed gates, completion hash rechecks and FTC
incident readiness without automatic notification. See
[the extension report](docs/ore-4.1-regulatory.md) for interfaces and limitations.

Validation: 100 tests (99 passed; one optional Playwright test skipped), package
validation, both skill validators, both new mod manifests and TypeScript checks
passed. Real native launch remains blocked by installed Claude Code 2.1.267 versus
the repository requirement of 2.1.287+. Production adapters and organizational
evidence require application-specific validation. No FDA/FTC certification claimed.

## Required Playwright dependency — 2026-10-09

Installed Playwright 1.63.0 and matching Chromium in the runtime Python environment.
Added pinned requirements to the repository and core skill, vendored them into
Python runtime mods, and documented both package and browser installation. Browser
acceptance now fails when dependencies are absent rather than skipping execution.
Updated the historical catalog check to allow this explicitly required browser
dependency while preserving its exclusion of reference-study repositories.

Latest validation: all 100 tests passed without omissions, including real isolated
Chromium exploration and screenshot export; package validation and diff checks passed.
# ORE 4.2 Adaptive Model Intelligence candidate — 2026-10-09

Work branch: `feat/ore-4.2-adaptive-routing`. Starting tree was clean at
`40dbb83`; no existing user edits were overwritten. Changes remain local and
unpublished. No commit, push, tag, release, global configuration write, provider
inference or background agent installation was performed.

## Implemented

- `ore-adaptive-model-routing` skill with seven focused references and discovery UI.
- Optional `ore-model-router`, registered in the existing generated marketplace;
  native requested/effective model diagnostics and reported usage, no model call.
- Versioned expiring observed registry, ten-dimensional explicit L0–L4 rubric,
  eligibility/ranking engine and conservative complete-cost estimates.
- MANUAL/APPROVAL_REQUIRED/AUTHORIZED_AUTO metadata modes, model/provider/effort
  locks, restrictive scoped preferences, exact ledger authorization matching,
  expiry/revocation/project checks, retry/delegation limits and cycle diagnostics.
- Existing single writer and governance file extended with optional schema-v1
  routing metadata, confirmation, atomic locking and task/governance revision checks.
- Explicit allowlisted local Claude JSON and Codex TOML configuration readers;
  safe ChatGPT manual adapter and unsupported-provider rejection.
- Preserved task acceptance/gates and risk floor; native usage remains separate
  from estimates; no second billing ledger. Existing guard, gates, regulatory,
  resume, context and department contracts remain authoritative.
- Reproducible synthetic evaluation for ten categories and fixed/adaptive/escalating
  strategies, plus routing and actual TypeScript-handler contract tests.

Inventory verified from package directories and marketplace: **29 skills, 28 mods,
9 existing departments**. All 28 previous skills and 27 previous mods are preserved.
Shared scripts were re-vendored using the existing builder; other adapters retain
their entrypoint templates. Metadata identifies **4.2.0-alpha.1 as a candidate**.

## Verification and review

The previous complete suite comprised 100 tests. Routing adds deterministic contract,
local host inspection, writer integration and native-handler tests; the final suite
contains 122 tests. No provider inference measurements are included.

| Check | Evidence |
| --- | --- |
| Regression suite | `python -m unittest discover -s evals -q`: **122 passed, no omissions**; includes isolated Chromium exploration and regulatory/state/runtime contracts |
| Package inventory/discovery/links/vendoring | `python scripts/validate_package.py`: 29 skills, 28 mods, 4.2.0-alpha.1 |
| New skill | skill-creator `quick_validate.validate_skill`: valid |
| New native mod | `claude plugin validate mods/ore-model-router`: passed, audited calls listed |
| TypeScript | TypeScript `tsc -p mods/ore-model-router --noEmit`: passed against checked-in 2.1.295 API types |
| Synthetic benchmark | 30 comparisons, 0 provider calls, no measured usage/cost/success/savings |
| Whitespace | `git diff --check`: passed |
| Live host | Installed Claude Code **2.1.267**, below repository requirement **2.1.287+**; compatible native launch remains unverified |

Independent read-only reviewer exercised core contracts and found authoritative task
requirements could be replaced, session identity was caller-controlled, policy scope
was omitted from the confirmation, and malformed delegation/state inputs were not
fully guarded. Fixed those findings and added regression coverage. Review is local
code/contract evidence, not independent certification of provider execution.

Follow-up review confirmed all five findings fixed and found no remaining blocker
within the manual/advisory scope. Its audit-detail recommendation was also addressed:
decisions now retain fixed rationale, host, scope, level/dimensions, timestamp,
governance revision and requirement/registry hashes without storing sensitive profiles.

## Acceptance status and pending work

The local package and offline routing behavior are reviewable. **The master request
is not fully accepted or certified.** No stable release or measured savings is claimed.

| Requirement | Status |
| --- | --- |
| Skill discovery and inventory | Verified locally |
| Mod package and marketplace registration | Verified locally; actual install/launch on compatible host pending |
| Registry, analyzer and adaptive policy | Verified with synthetic trusted observations; empirical calibration pending |
| Consent, locks, preferences and recovery | Local contract/writer tests passed; real host end-to-end approval execution pending |
| Effective model and reported usage | Native SDK calls validated by types and handler mocks; live observation pending |
| Safe incompatible-host fallback | Implemented manual selection; unknown effective values remain unknown |
| Native model/provider/effort changes | Not implemented as verified execution; current adapters inspect/recommend only |
| Persistent configuration scopes | Project/session/task implemented; installation/organization writer absent |
| Once/reject/keep/revoke controls | Manual once/keep; existing ledger revocation and task decisions; atomic one-use execution grant deferred |
| Benchmarks | Synthetic policy set executed; real providers and token/cost improvements unmeasured |
| Quality and regulatory preservation | Authoritative task requirements retained; existing regressions exercised |
| Release certification | Pending compatible-host execution and remaining adapter evidence |

Model/provider/effort changes, persistent authorization, expanded budget, provider
transmission, global configuration and publication retain their applicable user
authorization requirements. The existing model selected by this user was not changed.
No credentials were requested or read. Other-provider compatibility is not claimed.

Details, installation/removal commands, configuration examples, documented sources,
known limits and next-version work are in
[the 4.2 guide](docs/ore-4.2-adaptive-routing.md). Official Claude and OpenAI host
documentation was fetched on 2026-10-09; model access still requires actual observation.
# ORE 4.2.1 — Human-Friendly Approval Experience — 2026-10-09

Implemented on `feat/ore-4.2.1-friendly-approvals`, starting from clean main at
`6bb6fed`. This update stays local for review; earlier Git publication authorization
was for the previous update. No release/tag, global configuration, model switch,
production operation, cloud/Supabase write or background process was created.

## Changes

- Pure shared `mods/sdk/approval.ts`: structured natural-language summaries and
  impact, four risk classes, full exact JSON plus multiline SQL/command code blocks.
- Guard, shared runtime/ledger, model-router, scope reviews and browser consent use
  the same real native dialog. No second approval ledger or permission subsystem.
- Dangerous full details remain visible before approval. Progressive requests first
  require details, then approve the exact action. Free text cannot bypass that sequence.
- Missing destinations/resources remain unknown; declared targets are not claimed
  verified. RLS/privilege/authorship/integrity/mutation protection remain unproved
  unless separate evidence exists. No table immutability claim is introduced.
- No silent truncation: excessive rendered requests, secrets, control characters,
  explicit insufficient permissions and presentation failure block approval.
- Prose-only newline normalization; SQL/commands/parameters stay byte-for-byte
  equivalent. Safe code fences and escaped labels prevent misleading presentation.
- Native deny/ask/allow rules, unchanged next(e), task revisions, action snapshots,
  ledger expiry/revocation and project scopes remain authoritative. Invalid custom
  guard configuration blocks; custom patterns cannot remove base protections.
- Canonical presenter is vendored by the existing builder and checked by the package
  validator. Metadata is 4.2.1-alpha.1; inventory remains **29 skills / 28 mods / 9 departments**.

## Verification

The dedicated approval suite contains **15 tests**, added to the previous 122.
Full regression: **137 tests passed, no omissions**, including isolated Chromium,
state, runtime, routing, business-flow and regulatory contracts. New cases cover
long/oversized requests, multiline SQL, literal escapes, destructive/production/cloud
operations, unknown resources, insufficient permissions, secrets, rejection, expired
approval, presentation failure, action/state changes, safe fences and policy patterns.

Package validation passed with coherent inventory, references and canonical vendoring.
The three changed native packages (guard, approval-ledger, model-router) passed
`claude plugin validate` and TypeScript checks against the generated 2.1.295 API.
TypeScript additionally passed for **all 28 mods**. Package validation and
`git diff --check` passed. The skill frontmatter and self-contained approval reference
are preserved; no new skill or department is added.
Native status commands for all three packages launched successfully with
`--plugin-dir --no-session-persistence -p`; no inference was requested by these
implemented commands. Router status observed claude-sonnet-5-5, USD 0 usage and
modelChanged false. Installed Claude Code is now **2.1.295**; this agent did not
upgrade it. Native observations do not imply a provider benchmark or model switch.

## Compatibility and limitations

`$.ui.ask` is the supported native AskUserQuestion dialog; arbitrary “Other” text
is not treated as approval beyond exact labels and the detail-review phase. Dismissal
or noninteractive inability to present consent blocks mutation. No native permission
rule, mode or PermissionRequest allow decision is installed or changed.

Persistent/previous-policy choices are intentionally absent from ORE's presenter
because this guard cannot prove and enforce such native scope. Host-native policy
controls are retained. One-time metadata writes still require explicit review of
their displayed durable scope/expiry. Guard consent is ephemeral; the existing writer
audits durable ledger/policy decisions. ORE adds no raw-action state/log; native
transcript behavior remains the host's responsibility.

Real interactive dialog viewport/rendering across supported surfaces remains
unverified. The 12,000-character limit is a conservative ORE bound, not a guarantee
about host rendering. Classification remains pattern-based and cannot inspect
hidden scripts, dynamic shell effects or remote permissions. Required quality and
regulatory evidence remains unchanged. No guaranteed savings or stable certification.

Official [permissions](https://code.claude.com/docs/en/permissions),
[hooks](https://code.claude.com/docs/en/hooks) and
[plugin](https://code.claude.com/docs/en/plugins) documentation was fetched on
2026-10-09; unavailable mods documentation was supplemented by checked-in native SDK
declarations and actual local plugin validation. See
[the approval guide](docs/ore-4.2.1-approval-experience.md) for UX, examples and scope.
