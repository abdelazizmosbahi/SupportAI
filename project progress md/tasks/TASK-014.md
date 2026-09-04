# TASK-014 — Implement Memberships and RBAC

## Status

TODO

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

- [ ] OWNER can manage all members
- [ ] ADMIN can manage members (except OWNER)
- [ ] AGENT can only manage conversations
- [ ] VIEWER has read-only access
- [ ] Unauthorized actions return 403

## Tests Required

- [ ] RBAC enforcement tests
- [ ] Permission matrix test

## Dependencies

- TASK-013

## Notes

None

## Completion

Not completed.
