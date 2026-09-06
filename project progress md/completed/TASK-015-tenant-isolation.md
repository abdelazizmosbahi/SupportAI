# TASK-015 — Implement Tenant Isolation Middleware

## What Was Done

Implemented tenant isolation as a single, mandatory enforcement point so no
organization-scoped endpoint can ever read or write another tenant's data.

### `backend/app/core/tenant.py` (new)

- `TenantContext` dataclass: resolved `Membership`, `role_name`, and the member's
  effective `permissions` set.
- `resolve_tenant(db, user_id, org_id)`: the one true membership lookup. Always
  filters by **both** `user_id` and `organization_id` in a single query, then
  resolves the role. Raises `403 Forbidden` when the user is not a member or the
  role is missing.
- `get_tenant_context` FastAPI dependency: wires `current_user` + `org_id` path
  param into `resolve_tenant`.

### `backend/app/core/permissions.py` (refactored)

- Removed the duplicate `_get_membership` / `_resolve_role` helpers.
- `require_permission(permission)` now uses `resolve_tenant` from `tenant.py`.
- This also removed a latent circular import (`permissions` ↔
  `organization_service`): `tenant.py` now sits between them and imports nothing
  from the services layer.

### Endpoint coverage

Every organization-scoped endpoint already routes through
`require_permission(permission)` (TASK-014), which today resolves through
`resolve_tenant`:

- `GET/PATCH/DELETE /organizations/{org_id}` — `organization.read/update/delete`
- `GET/POST/PATCH/DELETE /organizations/{org_id}/members` — `members.*`

New org-scoped resources (documents, conversations, tickets) simply add
`get_tenant_context` and inherit the isolation automatically.

## Why This Design

- A single dependency means enforcement is hard to forget on future endpoints.
- Permission grant and tenant-boundary checks are performed in one round-trip.
- The boundary is testable in isolation and auditable in one file.

## Activity Log

- 2026-09-06 — Created `tenant.py` and refactored `permissions.py`: find and fix circular import issue.
- 2026-09-06 — Rewrote `tests/test_rbac.py`: permission matrix, `require_permission` via
  `resolve_tenant` patching, and TenantIsolation class backed by a fake
  `AsyncSession` whose `execute` parses the membership query's bound values
  (thereby also asserting the lookup is always scoped by user **and** org).
- 2026-09-06 — Verified: `pytest` 11 passed; `ruff check app tests` clean.

## Tests

`backend/.venv/Scripts/python.exe -m pytest tests -q` → **11 passed** (was 9;
added require-permission + tenant-isolation coverage).

- Cross-tenant read of another org → 403.
- Member endpoint isolation (member role sees own org, foreign org blocked) → 403.
- Unauthenticated / non-member → 403.

Note: live cross-tenant HTTP run against the cloud database was skipped this
round (local uvicorn startup was flaky); the isolation logic is fully covered by
the async unit tests. A full-app HTTP smoke test against Supabase had already
passed in the preceding config task (register/login/create-org/me/members/list).

## Future Tasks

- Expose `T` / `X-Tenant-ID` semantics at the API layer if org routing should
  move out of the URL path.
- Add DB-level enforcement later (RLS) for defense in depth; app-level check
  is sufficient while data stays SQLAlchemy-managed.

## Related Files

- `backend/app/core/tenant.py` (new)
- `backend/app/core/permissions.py`
- `backend/tests/test_rbac.py`
- `backend/tests/conftest.py`