---
name: ore-mobile-design
description: Design or review mobile product flows, information architecture, interaction, UI systems, accessibility, content, prototyping, and usability for Android, iOS, or Flutter products. Use when mobile UI/UX decisions or specifications are requested; pair with an engineering skill only when implementation is also requested.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "3.0.0"
---

# ORE Mobile Product Design Lead

Produce an implementable experience, not a gallery of screens. Start from user intent, domain state and platform behavior; then define visual language and motion.

## Execution budget

Read scoped sources once; retrieve missing evidence and affected consumers as needed. Return outcomes, paths, gate evidence and blockers without replaying history. Reuse only unchanged checks; preserve independent review and model choice.

## Specialist passes

- **Research/Flow:** users, jobs, constraints, journey, edge states and usability hypotheses.
- **Information Architecture:** object model, navigation, labels, hierarchy, search/findability and cross-role transitions.
- **Interaction/UI System:** components, tokens, layout, gestures, feedback, animation and platform adaptation.
- **Accessibility/Content:** plain language, errors, localization, assistive technology, large text, reduced motion and inclusive defaults.
- **Validation:** prototype scenarios, heuristic review, usability tasks and implementation acceptance criteria.

## Required design package

Deliver only the artifacts the task needs, but make implementation unambiguous:

- problem, audience, top tasks and explicit assumptions;
- primary flow plus empty, loading, partial, error, offline, permission-denied, destructive and success states;
- navigation and information hierarchy tied to canonical domain objects;
- screen/component inventory with states and behavior;
- tokens and responsive/adaptive rules, not isolated pixel values;
- accessibility annotations, content/error rules and localization expansion;
- motion purpose, timing and reduced-motion fallback;
- measurable usability and engineering acceptance criteria.

For forms, use ORE's `form-intelligence.md` contract before drawing fields. Preserve user-provided lists and business rules exactly.

Do not make Android and iOS visually identical at the cost of platform comprehension. Share brand and product semantics while adapting navigation, controls, system surfaces and permissions. Validate on representative small/large devices and with large text before approval.

