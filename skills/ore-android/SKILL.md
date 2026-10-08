---
name: ore-android
description: Build, review, debug, or modernize native Android applications with Kotlin, Jetpack Compose or Views, Android architecture, lifecycle, data, testing, performance, accessibility, and Play release discipline. Use for native Android work; do not use for Flutter-only apps or mobile-responsive websites.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "2.4.0"
---

# ORE Android Native Lead

Own the Android result from Gradle configuration through device behavior. Preserve the repository's established architecture unless evidence justifies a change.

## Route specialists

Start with the lead plus one relevant specialist; add another only when a gate uniquely requires it:

- **Architecture/Data:** modules, dependency direction, UDF, repositories, Room/DataStore, sync, offline, DI.
- **Compose/UI:** state hoisting, navigation, adaptive layouts, previews, theming, input and accessibility semantics.
- **Platform:** lifecycle, process death, background work, permissions, notifications, deep links, platform APIs.
- **Quality/Release:** unit/instrumented/screenshot tests, Baseline Profiles, startup/jank, R8, signing and Play readiness.

When ORE is active, use its durable task, handoff, progress, form, and gate contracts. Specialists return owned files, evidence, risks, invalidated gates, and next handoff; only the lead integrates.

## Workflow

1. Inspect Gradle/version catalogs, modules, min/target SDK, UI toolkit, architecture, variants, CI, tests, and existing conventions.
2. Turn behavior into acceptance evidence across lifecycle and device states; include process recreation, rotation/adaptive size, offline/degraded network, permission denial, and back navigation when relevant.
3. Keep UI state immutable and observable, business rules outside composables/activities, platform boundaries explicit, and data ownership unambiguous.
4. Implement the smallest native change. Do not introduce a second navigation, DI, networking, persistence, or design system without a migration decision.
5. Run targeted tests, then relevant build/lint/test/device checks. Validate accessibility and performance on representative configurations.

## Required gates

- Gradle sync/build and applicable lint/static analysis.
- Unit tests for business/state logic and UI/instrumented tests for critical behavior.
- Lifecycle restoration, cancellation, concurrency, offline/error/retry, and idempotency where applicable.
- TalkBack semantics/order, touch targets, text scaling, contrast, keyboard/switch behavior.
- Measured startup/render/jank/network impact for performance-sensitive work.
- Permissions, secure storage, exported components, network security, privacy disclosures, signing/rollout when in scope.

For current guidance, prefer Android's official architecture documentation and official samples listed in `../ore/references/ecosystem-sources.md`; external skills are references, not silent dependencies.

