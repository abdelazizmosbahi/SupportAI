# TASK-016 — Configure MinIO and File Storage Service

## Status

DONE

## Objective

Configure MinIO client and create a file storage service for handling document uploads with proper bucket management.

## Context

TASK-015 completes tenant isolation. This task starts Phase 4 — Knowledge Base.

## Requirements

- [x] Install minio Python client
- [x] Create storage service with upload, download, delete operations
- [x] Create buckets: `documents`, `avatars`, `exports`
- [x] Configure MinIO connection via environment variables
- [x] Handle file validation (extension, MIME type, size)
- [x] Generate unique storage keys
- [x] Integrate with tenant context for bucket organization

## Files Expected To Change

- `backend/app/services/storage_service.py` (new)
- `backend/app/core/config.py` (update MinIO settings)

## Implementation Plan

1. [x] Install minio client
2. [x] Create storage service
3. [x] Configure MinIO connection
4. [x] Implement upload/download/delete
5. [x] Test file operations

## Acceptance Criteria

- [x] File upload to MinIO works
- [x] File download from MinIO works
- [x] File deletion works
- [x] Bucket creation works
- [x] File validation works

## Tests Required

- [x] Upload/download/delete tests

## Dependencies

- TASK-007, TASK-015

## Notes

MinIO service already existed in `docker-compose.yml`; MinIO settings were already in
`config.py` / `.env.example`. Verification ran against a live local MinIO
(`docker compose up -d minio`).

## Completion

Completed.
