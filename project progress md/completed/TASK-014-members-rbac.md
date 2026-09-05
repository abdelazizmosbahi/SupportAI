# TASK-014 — Implement Memberships and RBAC

## Status

DONE

## Completed At

2026-09-05

## Summary

Implemented membership management (invite, update role, remove) and role-based access control with centralized permission checking.

## Implementation

- Created `app/core/permissions.py` with:
  - Permission codes (organization, members, documents, conversations, messages, tickets, evaluations, analytics, audit)
  - Role definitions OWNER / ADMIN / AGENT / VIEWER with permission sets
  - `require_permission(permission)` dependency: validates membership + role permission, returns 403 otherwise
- Created `app/services/member_service.py`:
  - `list_members()`, `invite_member()`, `update_member_role()`, `remove_member()`
  - OWNER protection: only OWNER manages OWNER role, no self-demotion from OWNER, last OWNER cannot leave, only OWNER removes an ADMIN
- Created `app/api/members.py` endpoints:
  - `GET /api/v1/organizations/{org_id}/members`
  - `POST /api/v1/organizations/{org_id}/members` (invite registered user)
  - `PATCH /api/v1/organizations/{org_id}/members/{user_id}` (update role)
  - `DELETE /api/v1/organizations/{org_id}/members/{user_id}`
- Created `app/schemas/member.py` (MemberResponse, MemberInvite, MemberRoleUpdate)
- Refactored `organizations.py` write endpoints to use `require_permission` (PATCH uses `organization.update`, DELETE uses `organization.delete` which is OWNER-only)
- Update `organization_service.get_or_create_owner_role` to seed via centralized role map
- Created seed migration `0002_seed_roles` inserting the four roles with permission sets
- Registered members router in `main.py`

## Files Changed

- `backend/app/core/permissions.py` (new)
- `backend/app/services/member_service.py` (new)
- `backend/app/api/members.py` (new)
- `backend/app/schemas/member.py` (new)
- `backend/app/api/organizations.py` (updated - use require_permission)
- `backend/app/services/organization_service.py` (updated - seed via role map)
- `backend/app/main.py` (updated - register members router)
- `backend/alembic/versions/0002_seed_roles.py` (new)
- `backend/tests/test_rbac.py` (new)

## Database Changes

- New `0002_seed_roles` migration: inserts OWNER, ADMIN, AGENT, VIEWER roles with JSON permission sets

## Tests Added

- `tests/test_rbac.py`: permission matrix tests (all 4 roles) + `require_permission` enforcement tests (allow/403 non-member/403 insufficient/403 unknown role) — 9 passed

## Important Decisions

- Permissions centralized in `permissions.py` to avoid duplication and enable reuse across endpoints
- `require_permission` returns 403 for both non-members and members lacking the permission
- Basic invitation: adds an existing registered user by email (no invite email/link yet)
- OWNER role granted full permissions via ALL_PERMISSIONS
- Seed roles via Alembic migration so permissions are versioned with schema

## Known Limitations

- Invitation is basic (no email notifications or invite codes) — extended in future signup flow
- Live DB integration not executed (PostgreSQL/Docker deferred)
- Members endpoints not yet wired into the React UI (frontend member management deferred)

## Follow-up Work

TASK-015 — Implement Tenant Isolation Middleware

## Git Commit

TASK-014: Implement memberships and RBAC with permission checking — 2026-09-05

## Notes For Next Task

RBAC permission dependency ready for reuse. Tenant isolation middleware (TASK-015) will centralize membership resolution.
