---
name: ore-form-workflows
description: Design, build, review, or repair material forms and data-entry workflows with authoritative field lists, role ownership, canonical data, semantic validation, reference data, accessibility, drafts, collaboration, security, and idempotent submission. Use across web or mobile whenever a form is more than a trivial isolated input.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "4.2.1-alpha.3"
---

# ORE Form Workflows Lead

Treat a form as a stateful business workflow and data contract, not a collection of text boxes.

## Execution budget

Read scoped sources once; retrieve missing evidence and affected consumers as needed. Return outcomes, paths, gate evidence and blockers without replaying history. Reuse only unchanged checks; preserve independent review and model choice.

## Mandatory first artifact

Before implementation, produce a form contract with:

- user/role, job, entry/exit state, authorization and canonical record;
- upstream sources, downstream consumers and identity/lineage;
- sections or steps with role ownership;
- every field's label, semantic type, source/default, required/conditional rule, allowed values, normalization, client and server validation, error/help text, privacy class and persistence;
- controlled lists, search/select dependencies, jurisdiction rules and unknown/other handling;
- draft/autosave/resume, collaboration/conflict, offline/retry/cancel behavior;
- idempotency, duplicate protection, audit events and success/failure recovery;
- keyboard/focus/screen-reader, text scaling, localization, responsive and reduced-motion behavior.

Any list, order, required field or business rule supplied by the user is authoritative. Preserve it exactly across UI, schema, validation, persistence and tests unless the user explicitly approves a change.

## Route specialists

- **Workflow/Role:** stages, ownership, permissions, transitions and canonical entity.
- **Field/Validation:** semantic types, normalization, client/server schemas and errors.
- **Reference Data:** controlled vocabularies, canonical selectors, location/jurisdiction and lineage.
- **State/Collaboration:** drafts, autosave, resume, concurrency, conflict, retry and idempotency.
- **Form UX/Accessibility:** grouping, progressive disclosure, input controls, focus, announcements, touch and localization.

## Gate

`FORM_INTELLIGENCE` requires evidence for happy, empty, invalid, boundary, duplicate, unauthorized, slow/failing network, retry and double-submit paths; keyboard and assistive technology; narrow/wide layouts and large text; server errors mapped to actionable controls; draft/resume and cross-role transitions when applicable; canonical list integrity and downstream lineage.

Do not mark the form complete because it renders. Under ORE, this lead and the platform lead are siblings with separate owned outputs; neither delegates to the other. ORE integrates them and owns durable progress.

