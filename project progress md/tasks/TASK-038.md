# TASK-038 — Implement CI/CD with GitHub Actions

## Status

TODO

## Objective

Create GitHub Actions CI/CD pipeline for lint, tests, security scanning, and Docker builds.

## Context

TASK-037 writes tests. This task adds Phase 14 — CI/CD.

## Requirements

- Create GitHub Actions workflow
- Backend CI: ruff, mypy, pytest
- Frontend CI: npm ci, lint, test, build
- Docker CI: build images, health checks
- Security scanning: Trivy, Bandit, pip-audit, npm audit
- RAG evaluation in CI
- Create `.github/workflows/ci.yml`

## Files Expected To Change

- `.github/workflows/ci.yml` (new)

## Implementation Plan

1. Create CI workflow
2. Add backend lint/test jobs
3. Add frontend lint/test/build jobs
4. Add Docker build job
5. Add security scanning
6. Test workflow

## Acceptance Criteria

- [ ] CI workflow created
- [ ] Backend lint passes
- [ ] Backend tests pass
- [ ] Frontend lint passes
- [ ] Frontend tests pass
- [ ] Docker builds succeed
- [ ] Security scans run

## Tests Required

- [ ] CI workflow validates

## Dependencies

- TASK-037

## Notes

None

## Completion

Not completed.
