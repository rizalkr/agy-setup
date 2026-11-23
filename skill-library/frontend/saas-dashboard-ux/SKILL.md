---
name: saas-dashboard-ux
description: Data-dense SaaS dashboard, admin panel, form, table, and multi-tenant workflow UX patterns. Use when building or refining B2B dashboards, CRUD tables, filters, empty states, status badges, or complex multi-step forms.
---

# SaaS Dashboard & Data-Dense UX

## 1. Information Density & Scannability
- Prioritize fast operational scanning over oversized decorative cards.
- Limit top KPI summary strips to 3–4 decision-grade metrics, each paired with a concrete comparison (e.g., period delta, threshold, or mini sparkline) and `tabular-nums`.
- Keep persistent navigation lean (clear active indicator, logical grouping, collapsible sidebar on smaller screens) and surface primary page actions consistently in the top-right page header.

## 2. Data Tables & Filtering UX
- Keep table headers clean and scannable; use sticky headers for tall scroll containers.
- Align columns by data type: left-align text/names, right-align numbers/currency/quantities, use monospace (`font-mono tabular-nums`) for codes, invoice numbers, plate numbers, and IDs.
- Render statuses as compact semantic pills (small status dot + subtle tinted background + crisp text)—never loud full-saturation blocks.
- Sync search, filters, sort order, and pagination to URL search params so views are shareable and survive browser back/refresh.
- Provide contextual bulk-action toolbars only when rows are selected, and overflow row actions (`...`) when >2 actions exist.

## 3. Design All Four View States
Every data-driven panel, table, or detail view must handle:
- **Loading**: Structural skeletons matching the exact row/card dimensions to eliminate layout shift (CLS).
- **Empty**: Clear explanation of why no items exist (first-time vs filtered-out) plus a direct CTA ("Create item" or "Reset filters").
- **Error**: Non-destructive inline alert with specific failure context and a single-click Retry action.
- **Populated**: Safe truncation (`truncate` / `line-clamp-*`) with tooltip or detail drawer for overflowing descriptions.

## 4. Forms & Destructive Guardrails
- Structure long forms into logical sections or desktop 2-column fieldsets (section title & helper hint on the left, inputs on the right).
- Validate inline on blur/submit with field-level error messages linked via `aria-describedby`, preserving user input on failure.
- Require explicit confirmation dialogs stating concrete impact before destructive or irreversible financial/workflow mutations (approve, void, cancel, delete).
