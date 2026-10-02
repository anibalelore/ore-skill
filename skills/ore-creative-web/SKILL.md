---
name: ore-creative-web
description: Design and implement expressive web experiences using scroll storytelling, motion, playful interaction, canvas, WebGL, or 3D while preserving content clarity, accessibility, responsive behavior, and performance. Use when the user explicitly wants a modern dynamic or narrative site; do not activate for ordinary web UI.
license: Apache-2.0
metadata:
  author: anibalelore
  version: "2.2.0"
---

# ORE Creative Web Lead

Build a story whose content remains understandable without animation. Motion must communicate hierarchy, causality, progression or delight—not conceal weak information architecture.

## Specialist passes

- **Narrative/Art Direction:** story beats, emotional arc, visual motif, pacing and content hierarchy.
- **Interaction/Motion:** scroll choreography, transitions, gestures, physics and feedback.
- **Rendering:** DOM/CSS/SVG first; canvas/WebGL/3D only when it materially improves the concept.
- **Performance/Accessibility:** frame budget, loading strategy, device fallback, keyboard, reduced motion and readable static flow.

## Creative brief before code

Define audience, single narrative premise, sections/beats, interaction purpose, visual system, media inventory, target devices, motion budget, reduced-motion/static fallback and measurable acceptance criteria. Align with the existing brand; do not default to fashionable gradients or effects unrelated to the story.

## Required gates

- Every section is reachable and comprehensible by keyboard and without animation.
- `prefers-reduced-motion` provides a deliberate experience, not merely zero-duration chaos.
- Touch, wheel, trackpad, keyboard and resize/orientation paths do not trap navigation or hijack expected controls.
- Text remains semantic/selectable where practical; headings, landmarks, focus and announcements are correct.
- Progressive enhancement preserves core content when advanced rendering fails.
- Measure mobile and desktop frame stability, long tasks, memory, asset weight, LCP, INP and CLS against explicit budgets.
- Lazy load responsibly, avoid layout shifts, clean up observers/timelines/render loops, and pause hidden work.

Use GSAP/ScrollTrigger, Three.js or similar libraries only after checking license, bundle/performance cost, project fit and maintenance. See `../ore/references/ecosystem-sources.md` for reference implementations.

