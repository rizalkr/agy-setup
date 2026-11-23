---
name: tailwind-v4-shadcn-ui
description: UI engineering with Tailwind CSS v4 (and v3 compatibility), shadcn/ui, Radix UI primitives, and Framer Motion. Use when styling components, configuring CSS theme tokens, building accessible dialogs/tables/forms, or tuning animations.
---

# Tailwind CSS v4, shadcn/ui & Motion

## 1. Tailwind Version Detection & Theme Config
- Inspect `package.json` and global CSS first:
  - **Tailwind v4** (`@tailwindcss/postcss`): Uses `@import "tailwindcss";` and `@theme { --color-...; --font-...; }` directly in CSS instead of `tailwind.config.js`. Use CSS variables for design tokens and `@custom-variant` / `@utility` when extending.
  - **Tailwind v3**: Uses `@tailwind base; @tailwind components; @tailwind utilities;` and `tailwind.config.*`. Do not mix v4 CSS directives into v3 projects.

## 2. shadcn/ui & Radix Composition
- Merge conditional classes with `cn(...inputs)` (`clsx` + `tailwind-merge`) so consumer overrides work predictably.
- Keep `class-variance-authority` (`cva`) variants small and semantic (`variant`, `size`).
- Preserve Radix UI accessibility: keep `DialogTitle`/`DialogDescription` (use `sr-only` if visually hidden), proper `aria-*` labels on icon buttons, and keyboard focus traps.
- Avoid `z-index` wars: rely on Radix portals and consistent semantic scale tokens.

## 3. Responsive & Layout Discipline
- Design mobile-first (`base -> sm -> md -> lg -> xl`), verifying dense tables and dashboards wrap or scroll cleanly (`overflow-x-auto`) without horizontal page overflow.
- Use `lucide-react` icons with explicit sizing (`size-4`, `size-5`) and `shrink-0` inside flex rows.

## 4. Framer Motion Performance
- Animate only GPU-composited properties (`transform`, `opacity`)—avoid animating `width`, `height`, `top`, `left`, or `box-shadow` in hot lists.
- Respect reduced motion (`useReducedMotion()` or CSS `motion-reduce:`) and wrap route/conditional exits cleanly in `<AnimatePresence>`.

## Verification
- Check `npm run lint` and `npm run build` (or `tsc --noEmit`) to catch invalid class/component props.
- Visually verify mobile (~375px) and desktop (~1280px) viewports when modifying layout or navigation.
