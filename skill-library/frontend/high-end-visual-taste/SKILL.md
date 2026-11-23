---
name: high-end-visual-taste
description: High-craft frontend aesthetic direction, typography, color hierarchy, and anti-AI-slop rules inspired by Linear, Stripe, and Vercel. Use when designing landing pages, marketing sites, portfolios, hero sections, or establishing visual direction.
---

# High-End Visual Taste & Anti-AI-Slop

## 1. Anti-AI-Slop Mandate
Never ship generic AI template defaults:
- Avoid cliché purple/indigo-to-pink gradients, glowing ambient neon blobs behind every card, and dark backgrounds with unmotivated neon borders.
- Avoid 3-equal-column feature grids filled with generic rounded-square icon boxes and symmetrical filler copy.
- Avoid using default `Inter`/`Roboto` at uniform weights without contrast, scale tension, or intentional character.
- Avoid gratuitous glassmorphism (`backdrop-blur`) on flat content cards where crisp solid surfaces read cleaner.

## 2. Choose an Aesthetic Direction First
Before writing CSS or JSX, commit to one coherent visual paradigm tailored to the brand:
- **Precision Technical / Linear-style**: Deep tinted charcoal (`#0A0A0C`), hairline `1px` borders (`border-white/10`), crisp monospace metadata, razor-sharp contrast.
- **Refined Enterprise Light / Stripe-style**: Crisp warm off-white canvas (`#FAFAFA`/`#F8FAFC`), subtle elevated white surfaces, crisp hairline borders, authoritative navy/slate ink.
- **Swiss Editorial / Portfolio**: Generous whitespace, asymmetric 12-column grids, expressive serif or geometric display headings paired with disciplined sans-serif body.
- **Warm Tactile**: Stone/sand neutrals, subtle surface warmth, restrained earthy or vermilion accents.

## 3. Typography & Visual Hierarchy
- Create clear scale contrast between display (`clamp(...)`, `tracking-tight`, `leading-[1.05]–[1.12]`, `text-balance`) and body (`15px–16px`, `leading-relaxed`, `max-w-[65ch]`).
- Pair at most two font families (e.g., an expressive display/sans + a clean technical sans), plus monospace with `font-variant-numeric: tabular-nums` for metrics, timestamps, IDs, and prices.
- Use font weight, opacity/tint, and spacing for hierarchy before adding extra borders or background boxes.

## 4. Color, Surface & Border Craft
- Keep accent colors disciplined (<10% of the viewport) and reserve saturated hues strictly for primary actions, active states, or semantic signals.
- Tint neutrals subtly toward your primary hue instead of pure `#000000` or flat `#808080`.
- Build depth through controlled surface stepping (`canvas` -> `surface` -> `elevated`) and subtle `1px` hairline borders rather than heavy drop shadows.

## 5. Spatial Choreography
- Prefer asymmetric bento layouts, clear left-edge vertical alignment rails, and generous breathing room (`py-20` to `py-32` section rhythm on marketing pages).
- Place one deliberate visual anchor per viewport (product UI preview, interactive data visual, or bold typographic statement) rather than competing focal points.
