# TASK-039 — Create Frontend Dockerfile and Complete Docker Compose

## Status

TODO

## Objective

Create Dockerfile for the React frontend and complete the Docker Compose configuration with Nginx reverse proxy.

## Context

TASK-038 adds CI/CD. This task starts Phase 15 — Production.

## Requirements

- Create `frontend/Dockerfile` with multi-stage build
- Add frontend service to Docker Compose
- Configure Nginx reverse proxy
- Route: `/` → React, `/api` → FastAPI, `/docs` → FastAPI docs
- Configure proper headers
- Set up SSL placeholder
- Complete production Docker Compose

## Files Expected To Change

- `frontend/Dockerfile` (new)
- `docker-compose.yml` (update)
- `docker/nginx/nginx.conf` (new)

## Implementation Plan

1. Create frontend Dockerfile
2. Configure Nginx
3. Add services to Docker Compose
4. Test complete stack

## Acceptance Criteria

- [ ] Frontend container builds
- [ ] Nginx routes correctly
- [ ] Full stack starts with `docker compose up`
- [ ] Frontend accessible via Nginx
- [ ] Backend API accessible via Nginx

## Tests Required

- [ ] Full stack integration test

## Dependencies

- TASK-002, TASK-008, TASK-036

## Notes

None

## Completion

Not completed.
