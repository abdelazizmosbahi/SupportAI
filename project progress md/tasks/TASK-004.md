# TASK-004 — Configure PostgreSQL and SQLAlchemy

## Status

DONE

## Objective

Configure PostgreSQL with pgvector extension and set up SQLAlchemy 2 with async support, connection pooling, and base model classes.

## Context

TASK-003 creates the FastAPI backend. This task adds database connectivity.

## Requirements

- Add PostgreSQL driver (asyncpg) to dependencies
- Create SQLAlchemy async engine and session factory
- Create base model class with common fields (id, created_at, updated_at)
- Enable pgvector extension in PostgreSQL
- Create database configuration using environment variables
- Add `DATABASE_URL` to environment configuration
- Create dependency for getting database sessions
- Test database connection

## Files Expected To Change

- `backend/app/core/database.py` (new)
- `backend/app/core/config.py` (update)
- `backend/app/models/base.py` (new)
- `backend/pyproject.toml` (update dependencies)

## Implementation Plan

1. Add asyncpg and sqlalchemy[asyncio] to dependencies
2. Create database configuration in `config.py`
3. Create async engine and session factory in `database.py`
4. Create base model class
5. Test connection to PostgreSQL

## Acceptance Criteria

- [ ] Database connection established
- [ ] pgvector extension enabled
- [ ] Base model class created with common fields
- [ ] Session dependency works
- [ ] `DATABASE_URL` configurable via environment variable

## Tests Required

- [ ] Database connection test
- [ ] Session creation test

## Dependencies

- TASK-003

## Notes

PostgreSQL will be provided via Docker Compose in TASK-007.

## Completion

Completed: 2026-09-04 15:42

Git commit: TASK-004: Configure PostgreSQL and SQLAlchemy with async support — 2026-09-04 15:42
