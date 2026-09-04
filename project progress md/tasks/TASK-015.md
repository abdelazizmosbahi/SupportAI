# TASK-015 — Implement Tenant Isolation Middleware

## Status

TODO

## Objective

Create a robust tenant isolation system that ensures all database queries are filtered by `organization_id` and that users cannot access data from other organizations.

## Context

TASK-014 implements RBAC. This task hardens multi-tenancy.

## Requirements

- Create tenant context dependency that extracts `organization_id` from current user
- Ensure all query endpoints filter by `organization_id`
- Create tests proving cross-tenant access is blocked
- Audit all existing endpoints for tenant isolation
- Document tenant isolation approach

## Files Expected To Change

- `backend/app/core/tenant.py` (new)
- `backend/app/api/` (audit and update all endpoints)
- `backend/tests/` (tenant isolation tests)

## Implementation Plan

1. Create tenant context dependency
2. Audit all existing endpoints
3. Add tenant filtering to all queries
4. Write tenant isolation tests
5. Test cross-tenant access is blocked

## Acceptance Criteria

- [ ] Tenant context dependency works
- [ ] All endpoints enforce tenant isolation
- [ ] Cross-tenant access returns 403 or 404
- [ ] Tests prove isolation

## Tests Required

- [ ] Cross-tenant document access blocked
- [ ] Cross-tenant conversation access blocked
- [ ] Cross-tenant organization access blocked

## Dependencies

- TASK-014

## Notes

Critical security requirement.

## Completion

Not completed.
