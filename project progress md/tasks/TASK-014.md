# TASK-014 — Implement Memberships and RBAC

## Status

DONE

## Objective

Implement member management (invite, update role, remove) and role-based access control with permission checking.

## Context

TASK-013 creates organizations. This task adds RBAC.

## Requirements

- Create membership CRUD endpoints
- Create role assignment
- Create permission checking dependency
- Implement OWNER, ADMIN, AGENT, VIEWER roles with defined permissions
- Create invitation system (basic)
- Enforce permissions on all endpoints
- Create migration for roles/permissions data

## Files Expected To Change

- `backend/app/api/members.py` (new)
- `backend/app/services/member_service.py` (new)
- `backend/app/schemas/member.py` (new)
- `backend/app/core/permissions.py` (new)

## Implementation Plan

1. Define role permissions
2. Create permission checking dependency
3. Create membership endpoints
4. Create seed data for roles
5. Test RBAC

## Acceptance Criteria

- [x] OWNER can manage all members
- [x] ADMIN can manage members (except OWNER)
- [x] AGENT can only manage conversations
- [x] VIEWER has read-only access
- [x] Unauthorized actions return 403

## Tests Required

- [x] RBAC enforcement tests
- [x] Permission matrix test

## Dependencies

- TASK-013

## Notes

- Roles: OWNER, ADMIN, AGENT, VIEWER defined centrally in `app/core/permissions.py` with permission codes.
- Permission checking dependency `require_permission(permission)` validates membership + role permission and returns 403 on failure.
- Member endpoints: GET/POST `/organizations/{org_id}/members`, PATCH/DELETE `/organizations/{org_id}/members/{user_id}`.
- Invitation is basic: invites an existing registered user by email (no invite email/link yet).
- OWNER protection rules: only OWNER can manage OWNER role; a member cannot demote themselves from OWNER; the last OWNER cannot leave.
- Seed migration `0002_seed_roles` inserts the four roles with their permission sets.
- Organization write endpoints refactored to use `require_permission` (PATCH requires `organization.update`, DELETE requires `organization.delete` = OWNER-only).

## Completion

Completed.
