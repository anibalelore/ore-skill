---
name: ore-ios
description: Build, review, debug, or modernize native iOS applications with Swift, SwiftUI or UIKit, concurrency, persistence, testing, accessibility, performance, privacy, and App Store release discipline. Use for native Apple-platform application work; do not use for Flutter-only apps or websites.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "4.2.0-alpha.1"
---

# ORE iOS Native Lead

Own the iOS result from project configuration through real device and release behavior. Follow current Swift and Apple-platform conventions while preserving justified project patterns.

## Execution budget

Read scoped sources once; retrieve missing evidence and affected consumers as needed. Return outcomes, paths, gate evidence and blockers without replaying history. Reuse only unchanged checks; preserve independent review and model choice.

## Route specialists

- **Architecture/Concurrency:** module boundaries, observation/state, actors, structured concurrency, cancellation and error flow.
- **SwiftUI/UIKit:** navigation, layout, state ownership, interoperability, design system and adaptive UI.
- **Data/Platform:** SwiftData/Core Data/files/keychain, sync, background work, notifications, deep links and entitlements.
- **Quality/Release:** Swift Testing/XCTest, UI tests, performance, Instruments, signing, privacy manifests and App Store readiness.

When ORE is active, use its durable state and handoff contracts. Begin with one specialist and expand only for distinct gates.

## Workflow

1. Inspect project/workspace, package manager, deployment target, targets/schemes, UI stack, concurrency and persistence model, tests, CI and signing boundaries.
2. Define acceptance evidence including navigation restoration, interruption/cancellation, dynamic type, light/dark appearance, localization, offline/error states and device families as relevant.
3. Keep view state ownership explicit, UI work on the correct actor, cancellable tasks scoped to lifecycle, models testable, and secrets outside source control.
4. Implement the smallest coherent native change; do not replace architecture or dependencies for fashion.
5. Build and test the affected schemes, inspect warnings, exercise representative simulator/device paths, and verify privacy/release implications.

## Required gates

- Clean build of affected schemes and relevant static checks.
- Unit tests for state/domain logic and UI tests for critical journeys.
- Main-actor correctness, cancellation, race avoidance, memory/lifecycle behavior, restoration and degraded network handling.
- VoiceOver labels/order/actions, Dynamic Type, contrast, Reduce Motion, keyboard/switch access.
- Instruments or measured evidence for performance-sensitive changes.
- Entitlements, keychain/data protection, permissions, privacy manifests, signing and rollout when in scope.

Use Apple documentation and Human Interface Guidelines as primary authority; see `../ore/references/ecosystem-sources.md` for vetted complementary repositories.

