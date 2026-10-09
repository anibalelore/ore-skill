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
