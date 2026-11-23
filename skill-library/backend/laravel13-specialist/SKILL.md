---
name: laravel13-specialist
description: Architecture, security, and performance patterns for Laravel 13 and PHP 8.3+. Use when writing controllers, Eloquent models, migrations, FormRequests, services, Excel imports/exports, or S3 file workflows in Laravel.
---

# Laravel 13 & PHP 8.3 Specialist

## 1. PHP 8.3 & Code Structure
- Use `declare(strict_types=1);` in new PHP files, typed properties, constructor property promotion, and PHP 8.3 enums for statuses/roles instead of magic strings.
- Keep controllers thin: validate via `FormRequest`, delegate multi-step business logic to `App\Services\*` or Action classes, and authorize via Policies or explicit tenant checks.

## 2. Multi-Tenant & Authorization Safety
- Never trust client-supplied `tenant_id` or `user_id`; scope every query, route model binding, and write operation to the authenticated user's permitted tenant(s).
- Enforce state-transition guards in services (e.g., `DRAFT -> APPROVED -> ONGOING`) before mutating invoices, orders, or payments.

## 3. Eloquent Performance & Transactions
- Prevent N+1 queries: eager-load relations with `with(['rel:id,name'])`, select only required columns, and use `chunk()` / `lazy()` for large batches.
- Wrap multi-table financial, inventory, or status mutations in `DB::transaction(fn () => ...)`, using `lockForUpdate()` when preventing race conditions on counters or balances.
- Guard nullable relations and handle empty collections gracefully in Blade/API resources.

## 4. Migrations, Excel & File Storage
- Write reversible migrations (`up` and `down`) with explicit foreign keys and composite indexes on `(tenant_id, status)` or frequent filter columns.
- Validate uploaded files (MIME, max size, extension) in `FormRequest`; stream S3 uploads via `Storage::disk('s3')` and queue heavy `maatwebsite/excel` imports/exports.

## Verification
Run `vendor/bin/pint --test` (or `vendor/bin/pint` to format) and targeted `php artisan test --filter=<TestName>` after edits.
