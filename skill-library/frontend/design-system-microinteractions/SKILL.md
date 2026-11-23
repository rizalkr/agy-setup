---
name: design-system-microinteractions
description: Design token architecture, component state consistency, choreography, and tactile micro-interactions. Use when creating or auditing design systems, interactive components, transitions, command palettes, or polish details.
---

# Design System & Tactile Micro-Interactions

## 1. Semantic Design Token Architecture
- Separate raw primitive palette values from semantic tokens (`--bg-canvas`, `--bg-surface`, `--bg-elevated`, `--border-subtle`, `--border-strong`, `--text-primary`, `--text-secondary`, `--accent`, `--danger`).
- Enforce contrast across both light and dark modes: >=4.5:1 for normal text and >=3:1 for UI borders, icons, and focus rings (WCAG AA).
- Maintain consistent radius nesting so nested elements feel optically concentric: `outer_radius = inner_radius + padding` (e.g., `rounded-xl` card with `p-1.5` around `rounded-lg` inner item).

## 2. Interactive State Completeness
Every clickable or focusable control must explicitly define all states:
- `default`: Clean resting contrast.
- `hover`: Subtle background/border shift (never jump layout dimensions).
- `focus-visible`: High-contrast ring with offset (`focus-visible:ring-2 focus-visible:ring-offset-2`), never `outline-none` without replacement.
- `active`: Crisp tactile press (`active:scale-[0.98]`) on buttons and interactive cards.
- `disabled`: Reduced contrast + `pointer-events-none` + `aria-disabled` where appropriate.
- `loading`: Inline spinner that preserves button width/height so surrounding controls do not shift.

## 3. Snappy Motion & Easing Physics
- Use purposeful, fast easing curves (`cubic-bezier(0.22, 1, 0.36, 1)` or taut springs):
  - `120ms–180ms` for hover states, tooltips, toggles, and dropdowns.
  - `200ms–300ms` for dialogs, drawers, and tab indicator slides.
- Avoid sluggish (>400ms) UI transitions, linear easing on movement, or playful bounce overshoot on enterprise controls.
- Animate strictly `transform` and `opacity` (plus `clip-path` where needed), and respect `prefers-reduced-motion`.

## 4. Tactile Polish & Keyboard Ergonomics
- Support keyboard flows cleanly: `Cmd/Ctrl+K` for command/search palettes, `Esc` to dismiss top-most overlay, arrow keys inside menus/tabs, and `Enter` to confirm.
- Use staggered entrance animations sparingly (max 30–50ms step, capped total delay) and keep above-the-fold UI immediately interactive on first paint.
