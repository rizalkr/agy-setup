---
name: nextjs-react19-best-practices
description: Best practices for Next.js 15/16 App Router and React 19 development. Use when building or optimizing App Router pages, Server Components, Server Actions, Suspense streaming, or fixing client-server boundary and waterfall issues.
---

# Next.js 15/16 & React 19 Best Practices

## 1. Async Request APIs (Next.js 15/16)
- Always `await` dynamic request APIs: `const { id } = await params;`, `const query = await searchParams;`, `const cookieStore = await cookies();`, `const hdrs = await headers();`.
- Type route props explicitly as `Promise<...>` in page, layout, and metadata functions.

## 2. Server vs Client Component Boundaries
- Default to React Server Components (RSC); add `'use client'` only at interactive leaf components (forms, modals, event handlers, browser APIs).
- Never import server-only secrets, DB clients, or Node modules into Client Components; enforce with `import 'server-only'`.
- Pass serializable props across the RSC boundary; lift shared state up or compose Server Components inside Client wrappers via `children`.

## 3. Eliminate Waterfalls & Stream Early
- Fetch independent data in parallel using `Promise.all([...])` or start promises before awaiting.
- Wrap slow async subtrees in `<Suspense fallback={<Skeleton />}>` instead of blocking the entire route in `page.tsx` or `layout.tsx`.
- Deduplicate repeated server-side reads within a render pass using `React.cache()`.

## 4. Server Actions & React 19 Forms
- Validate all Server Action inputs with a schema (e.g., Zod) and re-check authentication/authorization inside every action—never trust client-supplied IDs or roles.
- Use React 19 `useActionState` and `useFormStatus` for pending states and structured field errors without manual `useState` boilerplate.
- Call `revalidatePath` / `revalidateTag` immediately after mutations; return typed error objects rather than throwing raw exceptions for expected validation failures.

## 5. Bundle & Runtime Performance
- Use `next/dynamic` (`{ ssr: false }` when browser-only) for heavy charts, editors, or modal trees.
- Optimize images with `next/image` (explicit `sizes` and `priority` only for LCP hero images) and avoid barrel-file re-exports that bloat client bundles.

## Verification
Run `npm run typecheck && npm run lint` (and `npm run build` for route/RSC boundary checks) after completing changes.
