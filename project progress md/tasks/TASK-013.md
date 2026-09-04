# TASK-013 — Implement Organizations

## Status

TODO

## Objective

Implement organization CRUD with multi-tenant support. Each organization represents an isolated tenant.

## Context

TASK-012 completes auth. This task starts Phase 3 — Organizations.

## Requirements

- Create Organization model (id, name, slug, created_at, updated_at)
- Create Membership model (id, user_id, organization_id, role_id, created_at)
- Create Role model (id, name, permissions JSON)
- Create Permission model
- Create CRUD endpoints for organizations
- Auto-create membership for creator as OWNER
- Create migration
- Tenant isolation on all queries

## Files Expected To Change

- `backend/app/models/organization.py` (new)
- `backend/app/models/membership.py` (new)
- `backend/app/models/role.py` (new)
- `backend/app/api/organizations.py` (new)
- `backend/app/services/organization_service.py` (new)
- `backend/app/schemas/organization.py` (new)

## Implementation Plan

1. Create models
2. Create schemas
3. Create service layer
4. Create API endpoints
5. Create migration
6. Test CRUD

## Acceptance Criteria

- [ ] `POST /api/v1/organizations` creates org
- [ ] Creator becomes OWNER
- [ ] `GET /api/v1/organizations` returns user's orgs
- [ ] `GET /api/v1/organizations/{id}` returns org details
- [ ] `PATCH /api/v1/organizations/{id}` updates org
- [ ] Only OWNER can delete
- [ ] Tenant isolation enforced

## Tests Required

- [ ] Organization CRUD tests
- [ ] Tenant isolation test

## Dependencies

- TASK-010

## Notes

None

## Completion

Not completed.
