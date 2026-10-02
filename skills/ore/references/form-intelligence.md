# Form Intelligence Contract

Apply this contract before changing any form, wizard, onboarding sequence, settings editor, data-entry screen, checkout, upload, or role-based approval flow.

## Required artifact

Create `.ore/forms/<form-id>.json` before implementation and keep it synchronized. Validate it with `scripts/validate_form_contract.py`; when the user supplies an authoritative list, pass that JSON list with `--expected FIELD=FILE` so values and order are checked exactly. It must define:

1. user, role, job-to-be-done, entry point, exit state, and permissions;
2. canonical entity and stable identity; upstream sources and downstream consumers;
3. sections/steps and which role owns each field;
4. for every field: semantic type, required/optional/conditional state, default/source, allowed values, normalization, client validation, authoritative server validation, error text, accessibility name/help, privacy class, and persistence behavior;
5. controlled reference data and dependent selectors instead of duplicate free text where the system already owns a value;
6. draft, autosave, collaboration, conflict, retry, offline, cancellation, and resume behavior as relevant;
7. submission idempotency, duplicate prevention, audit events, success confirmation, and failure recovery;
8. responsive layout, keyboard order, focus movement, screen-reader announcements, touch targets, text scaling, localization, and reduced-motion behavior;
9. analytics that measure completion and failure without capturing sensitive field values.

Any list, taxonomy, ordering, required field, or business rule supplied by the user is authoritative. Preserve it exactly unless the user approves a change; never silently shorten, replace, reorder, or invent values.

## Implementation rules

- Do not ask users to re-enter known canonical data. Reference it and display the source.
- Do not infer global address or identity formats; use jurisdiction-aware inputs and configurable reference data.
- Validate close to the field for recoverable input errors and again on the server for authority. Preserve entered values after errors.
- Use the correct control for the data: bounded options, searchable canonical selector, date/time, currency/quantity with units, structured address, file constraints, or free text only when genuinely unbounded.
- Separate responsibilities by role without creating disconnected duplicate records.

## Mandatory validation matrix

`FORM_INTELLIGENCE` cannot pass until evidence covers happy, empty, invalid, boundary, duplicate, slow/failing network, retry, and double-submit cases; keyboard and assistive technology; narrow/wide layouts and text scaling; server rejection mapping; draft/resume and cross-role transitions when relevant; canonical reference integrity and downstream lineage.

If requirements are unknown, derive the safest project-consistent contract and list assumptions. Ask the user only for decisions that materially change workflow or business meaning.

