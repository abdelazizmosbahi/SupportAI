# TASK-006 — Create Application Configuration System

## Status

DONE

## Completed At

2026-09-04 16:00

## Summary

Created comprehensive configuration system using pydantic-settings covering all application settings: database, Redis, MinIO, JWT, LLM, embeddings, RAG, file upload, rate limiting, CORS, and logging.

## Implementation

- Expanded `backend/app/core/config.py` with all settings
- Added field validators for:
  - `JWT_SECRET` (warns when using default in production)
  - `DATABASE_URL` (must be PostgreSQL)
  - `ALLOWED_EXTENSIONS` (normalizes to lowercase, strips dots)
- Updated `.env.example` with all documented variables
- Verified app still starts and health endpoint works

## Files Changed

- `backend/app/core/config.py` (update)
- `.env.example` (update)

## Dependencies Added

None

## Database Changes

None

## Configuration Changes

- Added config for: MinIO, LLM, embeddings, RAG, file upload, rate limiting
- Added `API_V1_PREFIX` for versioned API routes
- Added `model_config = {"extra": "ignore"}` to tolerate unknown env variables

## Tests Added

- Config loading verification: PASS
- Field validator behavior spotted (database URL validation): PASS
- Health endpoint after config change: PASS

## Verification

- All settings load correctly: PASS
- `LLM_MODEL=qwen2:0.5b`, `RAG_TOP_K=5`, `MINIO_ENDPOINT=localhost:9000`: PASS
- `ALLOWED_EXTENSIONS=['pdf','txt','docx']` normalized: PASS
- FastAPI app starts and `/health` returns 200: PASS

## Important Decisions

- Default LLM model: `qwen2:0.5b` (small, runs on local hardware)
- Default embedding model: `all-MiniLM-L6-v2` (384 dims)
- RAG defaults: K=5, chunk_size=800, overlap=100
- File upload limit: 10MB, PDF/TXT/DOCX
- Rate limits: login 5/min, API 100/min, AI 20/min

## Known Limitations

- JWT_SECRET validation only warns when APP_ENV is production (not enforced in dev)

## Follow-up Work

TASK-007 — Create Docker Compose Development Environment

## Git Commit

TASK-006: Create comprehensive application configuration system — 2026-09-04 16:00

## Notes For Next Task

Full config system ready. All settings load from `.env` or environment variables. Next task creates Docker Compose for PostgreSQL, Redis, MinIO, and Ollama.