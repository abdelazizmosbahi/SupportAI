# TASK-012 — Implement React Auth Module

## Status

TODO

## Objective

Implement the React authentication module with login page, auth context/service, axios interceptor for token attachment, and protected routes.

## Context

TASK-011 completes backend auth. This task builds the frontend auth.

## Requirements

- Create login page
- Create registration page
- Create AuthContext + auth service (login, register, logout, getCurrentUser)
- Create axios interceptor to attach `Authorization: Bearer <token>`
- Create ProtectedRoute component for protected routes
- Store tokens in localStorage
- Handle token refresh on 401
- Configure routing for auth pages
- Handle loading and error states

## Files Expected To Change

- `frontend/src/api/` (new)
- `frontend/src/auth/` (new)
- `frontend/src/pages/` (new)
- `frontend/src/App.tsx` (update)

## Implementation Plan

1. Create auth API service
2. Create axios interceptor
3. Create AuthContext
4. Create ProtectedRoute
5. Create login page
6. Create registration page
7. Configure routing
8. Test auth flow

## Acceptance Criteria

- [ ] Login page renders and submits
- [ ] Registration page renders and submits
- [ ] Token stored in localStorage
- [ ] Interceptor attaches token to requests
- [ ] ProtectedRoute protects routes
- [ ] Unauthenticated users redirected to login

## Tests Required

- [ ] Auth service tests
- [ ] ProtectedRoute tests

## Dependencies

- TASK-002, TASK-011

## Notes

None

## Completion

Not completed.

## Update Notes

Git commit: TASK-012: Implement React auth module with login, registration, interceptor, and guards — 2026-09-04 18:00