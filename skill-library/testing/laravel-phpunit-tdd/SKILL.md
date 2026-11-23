---
name: laravel-phpunit-tdd
description: Automated feature and unit testing in Laravel 13 with PHPUnit 12. Use when writing Feature/Unit tests, factories, RBAC/tenant isolation assertions, or faking external services in Laravel.
---

# Laravel 13 & PHPUnit 12 TDD

## 1. Test Structure & Database State
- Use `RefreshDatabase` in Feature tests and model `Factory` states (`->approved()`, `->for($tenant)`) instead of manual raw `DB::table()->insert()` boilerplate.
- Follow Arrange-Act-Assert clearly; keep each test focused on one behavior or authorization boundary.

## 2. High-Value Coverage Areas
- **Tenant & RBAC isolation**: Test 403/404 responses when User A from Tenant 1 attempts to view, update, or delete Tenant 2's resources.
- **State machines & financial math**: Test valid and invalid transitions (e.g., `DRAFT -> APPROVED`, double-payment prevention, invoice totals, tax/discount rounding).
- **Validation**: Assert `assertSessionHasErrors([...])` or `assertUnprocessable()` on invalid payloads.

## 3. Faking External Side Effects
- Always fake external boundaries before acting: `Storage::fake('s3')`, `Queue::fake()`, `Mail::fake()`, `Notification::fake()`, `Http::fake()`.
- Assert uploaded file paths or queued jobs explicitly (`Storage::disk('s3')->assertExists(...)`, `Queue::assertPushed(...)`).

## Verification
Run targeted tests first (`php artisan test tests/Feature/MyFeatureTest.php --filter=test_name`), then run the relevant suite (`php artisan test`).
