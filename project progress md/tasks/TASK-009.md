# TASK-009 — Implement User Registration

## Status

TODO

## Objective

Implement user registration with email, password hashing using Argon2, input validation, and proper error handling.

## Context

TASK-008 containerizes the backend. This task starts Phase 2 — Authentication.

## Requirements

- Create User model (id, email, password_hash, first_name, last_name, is_active, created_at, updated_at)
- Create User schema (Pydantic)
- Create registration endpoint `POST /api/v1/auth/register`
- Hash passwords with Argon2
- Validate email format
- Check for duplicate emails
- Return user data (excluding password hash)
- Create Alembic migration for users table
- Add argon2-cffi to dependencies

## Files Expected To Change

- `backend/app/models/user.py` (new)
- `backend/app/schemas/auth.py` (new)
- `backend/app/api/auth.py` (new)
- `backend/app/services/auth_service.py` (new)
- `backend/app/core/security.py` (new)
- `backend/pyproject.toml` (update)

## Implementation Plan

1. Create User model
2. Create registration schema
3. Implement password hashing
4. Create registration endpoint
5. Create Alembic migration
6. Test registration

## Acceptance Criteria

- [ ] `POST /api/v1/auth/register` creates a user
- [ ] Password is hashed with Argon2
- [ ] Duplicate email returns error
- [ ] Invalid input returns validation error
- [ ] Migration applies successfully

## Tests Required

- [ ] Registration creates user
- [ ] Duplicate email rejected
- [ ] Password is hashed

## Dependencies

- TASK-005, TASK-008

## Notes

None

## Completion

Not completed.
