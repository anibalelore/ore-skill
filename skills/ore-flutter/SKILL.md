---
name: ore-flutter
description: Build, review, debug, or modernize Flutter applications with Dart, adaptive UI, state and navigation architecture, platform integration, testing, accessibility, performance, and mobile release discipline. Use for Flutter codebases; add native Android or iOS expertise only when platform-specific code is actually involved.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "4.1.0-alpha.1"
---

# ORE Flutter Lead

Own one coherent Flutter product while respecting Android and iOS platform behavior. Maximize shared product logic without forcing identical platform interaction where conventions differ.

## Execution budget

Read scoped sources once; retrieve missing evidence and affected consumers as needed. Return outcomes, paths, gate evidence and blockers without replaying history. Reuse only unchanged checks; preserve independent review and model choice.

## Route specialists

- **Architecture/State:** feature boundaries, dependency direction, state ownership, navigation, data/offline/sync.
- **Adaptive UI:** responsive layout, Material/Cupertino adaptation, design tokens, localization and accessibility.
- **Native Integration:** plugins, platform channels, lifecycle, permissions, background execution and build configuration.
- **Quality/Performance/Release:** Dart analysis/tests, widget/golden/integration tests, DevTools profiling and store builds.

Invoke Android/iOS native specialists only when native source, manifests/entitlements, platform APIs, signing or store behavior is in scope.

## Workflow and gates

1. Inspect `pubspec.yaml`, Dart/Flutter constraints, packages, feature structure, state/navigation conventions, flavors, native folders, tests and CI.
2. Define behavior for compact/expanded screens, text scaling, keyboard/insets, restoration, offline/error/retry and both target platforms.
3. Preserve the project's coherent state solution; avoid global mutable state and business logic in widgets.
4. Run formatting, `flutter analyze`, targeted tests, broader tests/builds, and integration/device paths proportional to risk.
5. Require semantic labels/order/actions, large text, contrast, reduced motion, touch targets, and platform-appropriate navigation.
6. Measure rebuilds, shader/frame timing, memory, startup, image/network costs for sensitive work.
7. Validate platform channels in both directions, typed error mapping, cancellation, version compatibility and native fallbacks.

When ORE is active, checkpoint all evidence and progress in its durable state. Prefer official Flutter architecture, accessibility and agent-tool guidance from `../ore/references/ecosystem-sources.md`.

