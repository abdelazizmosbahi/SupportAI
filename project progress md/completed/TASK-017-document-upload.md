# TASK-017 — Implement Document Upload API

## What Was Done

Built the document upload/management API: multipart upload → validation →
MinIO storage → database record (status UPLOADED), plus list / detail / delete,
all tenant-scoped end to end.

### `backend/app/models/document.py` (new)

`Document` (table `documents`) with:
- `id`, `created_at`, `updated_at` (via `BaseModel`),
- `organization_id` (FK → organizations, indexed),
- `filename` (200), `mime_type` (200),
- `storage_key` (500, unique, indexed),
- `size` (BigInteger),
- `status` (string, indexed) + `DocumentStatus` enum
  (UPLOADED / PROCESSING / PROCESSED / FAILED),
- `error_message` (nullable, for TASK-019),
- `created_by` (FK → users, indexed).

Registered in `app/models/__init__.py`.

### `backend/app/schemas/document.py` (new)

`DocumentResponse` — serializes the full metadata record (`from_attributes`).

### `backend/app/services/document_service.py` (new)

- `create_document(...)` — validates + uploads to MinIO **first**; only on a
  successful upload creates the `Document` row with `status=UPLOADED`.
  Invalid files raise `FileValidationError` before any persistence.
- `list_documents(db, org_id)` — newest-first, scoped to the org.
- `get_document(db, org_id, id)` — returns a row only if it belongs to the org.
- `delete_document(...)` — deletes the MinIO object (tolerating a missing
  object) then removes the record.

### `backend/app/api/documents.py` (new)

Router mounted at `/organizations/{org_id}/documents`:
- `POST` (upload) — `documents.create`, 201, `UploadFile` + `python-multipart`.
- `GET` (list) — `documents.read`.
- `GET /{id}` (detail) — `documents.read`, 404 if missing.
- `DELETE /{id}` — `documents.delete`, 204.

Every route resolves the tenant context first via `require_tenant`.

### Dependency: `require_tenant`

Extracted a shared `_authorize(db, user_id, org_id, permission)` helper in
`app/core/permissions.py` and added `require_tenant(permission)` — identical to
`require_permission` but returns the full `TenantContext` so endpoints can read
`organization_id` / `user_id` without a second membership lookup. Reads and
deletes are additionally scoped by `org_id` in the query, so cross-tenant
access is blocked both at the permission dependency and at the row scope.

### `backend/app/services/storage_service.py` tweak

`StoredFile` now carries `content_type` (the effective stored MIME type) so the
document record stores exactly what was written to MinIO.

### Migration `0003_add_documents_table`

Creates `documents` with the four indexes (org, status, created_by, unique
storage_key) and FKs. Applied to the cloud Supabase database
(`alembic upgrade head` → `0002 -> 0003`).

### Dependencies added

- `minio` (already, TASK-016)
- `python-multipart>=0.0.9` (required by FastAPI `UploadFile`) — added to
  `requirements.txt` + `pyproject.toml`, installed in venv.

## Tenant Isolation

`/api/v1/documents` itself is not a real reachable route: the router is
org-scoped (`/organizations/{org_id}/documents`), matching organizations and
members. Every handler requires `documents.*` permission through
`require_tenant` → `resolve_tenant`, and all queries filter by
`organization_id`. Verified live: user B gets 403 listing/reading org A's docs.

## Activity Log

- 2026-09-06 — Created Document model, schema, service, API, migration.
- 2026-09-06 — Added `require_tenant` + `_authorize`; `StoredFile.content_type`.
- 2026-09-06 — Unit tests (service-level, fake MinIO + fake document session).
- 2026-09-06 — Applied migration to Supabase; live HTTP smoke test over
  authentic MinIO + Supabase (see Tests).

## Tests

`pytest` — **38 passed**, ruff clean. New coverage:
- upload creates UPLOADED record + object; invalid file rejected with no record;
  MIME fallback to guessed type,
- list scoped by org; get/detail scoped by org (returns None for foreign org),
- delete removes record + object; tolerates missing object,
- `require_tenant` returns full context and enforces 403 on missing permission.

Live HTTP flow (real MinIO + Supabase): upload 201 `UPLOADED` → list 200 →
detail 200 → invalid `.exe` 400 → foreign tenant 403 → own empty list 200 →
delete 204 → 404 after.

## Future Tasks

- TASK-018/019 add processing (Redis/Celery) and advance status
  UPLOADED → PROCESSING → PROCESSED/FAILED using `error_message`.

## Related Files

- `backend/app/models/document.py` (new)
- `backend/app/schemas/document.py` (new)
- `backend/app/services/document_service.py` (new)
- `backend/app/api/documents.py` (new)
- `backend/alembic/versions/0003_add_documents_table.py` (new)
- `backend/app/core/permissions.py` (`require_tenant`, `_authorize`)
- `backend/app/services/storage_service.py` (`StoredFile.content_type`)
- `backend/app/models/__init__.py`, `backend/app/main.py`, `backend/tests/test_documents.py`,
  `backend/tests/test_rbac.py`