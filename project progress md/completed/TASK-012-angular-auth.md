# TASK-012 — Implement Angular Auth Module

## Status

DONE

## Completed At

2026-09-04 17:20

## Summary

Implemented the Angular authentication module with login, registration, auth service, HTTP interceptor, and route guards.

## Implementation

- Created `AuthService` with login, register, logout, getCurrentUser, refreshToken, token storage in localStorage, and user state management
- Created `authInterceptor` — attaches `Authorization: Bearer <token>` header, handles 401 by refreshing the token with queueing for concurrent requests
- Created `authGuard` — redirects unauthenticated users to `/login`
- Created `MainLayoutComponent` — wraps protected routes with sidebar/header (moved from app root)
- Restructured `app.routes.ts` — auth pages render standalone; protected routes are children of MainLayoutComponent guarded by authGuard
- Updated login/register components with working forms, loading states, error handling, validation, and navigation
- Added logout to header with user email display
- Added `provideHttpClient` with interceptor to app config

## Files Changed

- `frontend/src/app/core/auth/auth.service.ts` (new)
- `frontend/src/app/core/interceptors/auth.interceptor.ts` (new)
- `frontend/src/app/core/guards/auth.guard.ts` (new)
- `frontend/src/app/core/models/auth.ts` (new)
- `frontend/src/app/layout/main-layout/main-layout.component.ts` (new)
- `frontend/src/app/features/auth/login/login.component.ts` (update)
- `frontend/src/app/features/auth/register/register.component.ts` (update)
- `frontend/src/app/app.routes.ts` (update)
- `frontend/src/app/app.config.ts` (update)
- `frontend/src/app/app.ts` (update)
- `frontend/src/app/layout/header/header.component.ts` (update)

## Tests Added

- Frontend production build: PASS
- ESLint: PASS (all files)

## Important Decisions

- Tokens stored in localStorage
- Refresh token rotation handled in interceptor with request queueing to prevent duplicate refresh calls
- Login/register pages render outside the main layout (standalone)
- Protected routes wrapped in a guarded MainLayoutComponent
- Used Angular built-in control flow (@if) instead of *ngIf

## Known Limitations

- Integration test with backend pending Docker/PostgreSQL (deferred)

## Follow-up Work

TASK-013 — Implement User Management

## Git Commit

TASK-012: Implement Angular auth module with login, registration, interceptor, and guards — 2026-09-04 17:20

## Notes For Next Task

Angular auth module working. Next task adds user profile management.
