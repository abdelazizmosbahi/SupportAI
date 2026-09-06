# TASK-016 — Configure MinIO and File Storage Service

## What Was Done

Created the MinIO-backed file storage layer that Phase 4 (Knowledge Base) is
built on. The MinIO service and its settings already existed from TASK-007 /
TASK-006; this task added the client integration, the storage service, file
validation, tenant-scoped keys, and proof against both a fake and a live MinIO.

### `backend/app/services/storage_service.py` (new)

- `validate_file(filename, content_type, size_bytes)` — one function owning all
  upload validation:
  - non-empty size check,
  - extension allowlist (`settings.ALLOWED_EXTENSIONS`),
  - max size (`settings.MAX_UPLOAD_SIZE_MB`),
  - MIME type check against the extension, quietly accepting
    `application/octet-stream` / empty types for clients that do not sniff.
  - Raises `FileValidationError`.
- `generate_storage_key(org_id, category, filename)` — unique key
  `orgs/{org_id}/{category}/{uuid4}{ext}`; unique per upload, tenant-scoped by
  construction.
- `bucket_for_category(category)` — maps `documents`/`avatars`/`exports` to the
  bucket name in settings; unknown categories rejected.
- `StoredFile` result dataclass (`bucket` + `storage_key`).
- `StorageService` wrapping the MinIO client:
  - `ensure_buckets()` — idempotent creation of all configured buckets,
  - `upload(...)` — validate → generate key → `put_object`,
  - `download(...)` — enforce tenant scope → `get_object` → bytes,
  - `delete(...)` — enforce tenant scope → `remove_object`,
  - `_authorize()` — every read/delete re-verifies the key starts with
    `orgs/{org_id}/`, raising `StorageAccessError` otherwise. This makes
    cross-tenant access impossible even if a wrong key is passed.
- `get_storage_service()` — lazy process-wide singleton.

### Wiring

- MinIO settings were already present in `backend/app/core/config.py` and
  `backend/.env.example`; no config changes were required.
- `minio>=7.2.0` added to `requirements.txt` and `pyproject.toml`; installed
  (7.2.20) into the venv.

## Tenant Integration

TASK-015's `TenantContext` is threaded through every public method. Uploads
derive the key prefix from `tenant.organization_id`; downloads/deletes verify
the key belongs to that same org before touching MinIO. All org-scoped routes go
through `require_permission` → `resolve_tenant`, so the file API can rely on
tenant isolation end-to-end once wired in TASK-017.

## Activity Log

- 2026-09-06 — Installed `minio` client; wrote storage service + validation +
  key generation; added dep to manifests.
- 2026-09-06 — Unit tests with in-memory fake MinIO: validation matrix, key
  generation, bucket creation, upload/download/delete round trip, cross-tenant
  block, singleton.
- 2026-09-06 — `docker compose up -d minio`; ran live verification against
  `localhost:9000` (see Tests).

## Tests

- `pytest` — **29 passed** (18 new storage tests), ruff clean.
- Live MinIO (`minio/minio:latest`, root `minioadmin`/`minioadmin`):
  - buckets created: `documents`, `avatars`, `exports`
  - upload → download round trip returned identical bytes
  - cross-tenant download blocked with `StorageAccessError`
  - `.exe` upload rejected by `FileValidationError`
  - delete removed the object (subsequent download → `FileNotFoundError`)

## Future Tasks

- TASK-017 will add the `Document` model + upload API using this service.
- Consider presigned URLs for large downloads later.

## Related Files

- `backend/app/services/storage_service.py` (new)
- `backend/tests/test_storage_service.py` (new)
- `backend/requirements.txt`, `backend/pyproject.toml` (minio dep)
- `docker-compose.yml` (MinIO service, pre-existing)