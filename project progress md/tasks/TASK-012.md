# TASK-012 — Implement Angular Auth Module

## Status

TODO

## Objective

Implement the Angular authentication module with login page, auth service, HTTP interceptor for token attachment, and route guards for protected routes.

## Context

TASK-011 completes backend auth. This task builds the frontend auth.

## Requirements

- Create login page component
- Create registration page component
- Create auth service (login, register, logout, getCurrentUser)
- Create HTTP interceptor to attach `Authorization: Bearer <token>`
- Create auth guard for protected routes
- Store tokens in localStorage
- Handle token refresh on 401
- Configure routing for auth pages
- Handle loading and error states

## Files Expected To Change

- `frontend/src/app/features/auth/` (new)
- `frontend/src/app/core/auth/` (new)
- `frontend/src/app/core/guards/` (new)
- `frontend/src/app/core/interceptors/` (new)
- `frontend/src/app/app.routes.ts` (update)

## Implementation Plan

1. Create auth service
2. Create HTTP interceptor
3. Create auth guard
4. Create login component
5. Create registration component
6. Configure routing
7. Test auth flow

## Acceptance Criteria

- [ ] Login page renders and submits
- [ ] Registration page renders and submits
- [ ] Token stored in localStorage
- [ ] Interceptor attaches token to requests
- [ ] Guard protects routes
- [ ] Unauthenticated users redirected to login

## Tests Required

- [ ] Auth service tests
- [ ] Guard tests

## Dependencies

- TASK-002, TASK-011

## Notes

None

## Completion

Not completed.
