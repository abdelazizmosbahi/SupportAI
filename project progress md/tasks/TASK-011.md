# TASK-011 — Implement Refresh Tokens

## Status

TODO

## Objective

Implement refresh token mechanism for obtaining new access tokens without re-authentication.

## Context

TASK-010 implements access tokens. This task adds refresh tokens.

## Requirements

- Create RefreshToken model (id, user_id, token, expires_at, created_at)
- Create refresh endpoint `POST /api/v1/auth/refresh`
- Generate refresh token on login
- Store refresh tokens in database
- Validate refresh token on refresh request
- Invalidate old refresh token on use (rotation)
- Create logout endpoint `POST /api/v1/auth/logout`
- Create Alembic migration

## Files Expected To Change

- `backend/app/models/refresh_token.py` (new)
- `backend/app/api/auth.py` (update)
- `backend/app/services/auth_service.py` (update)

## Implementation Plan

1. Create RefreshToken model
2. Implement refresh token generation
3. Create refresh endpoint
4. Implement token rotation
5. Create logout endpoint
6. Create migration
7. Test refresh flow

## Acceptance Criteria

- [ ] Login returns both access and refresh tokens
- [ ] `POST /api/v1/auth/refresh` returns new access token
- [ ] Old refresh token is invalidated
- [ ] `POST /api/v1/auth/logout` invalidates refresh token
- [ ] Expired refresh token returns error

## Tests Required

- [ ] Refresh token flow works
- [ ] Token rotation works
- [ ] Logout invalidates token

## Dependencies

- TASK-010

## Notes

None

## Completion

Not completed.
