# TASK-017 — Implement Document Upload API

## Status

TODO

## Objective

Implement document upload endpoint with file validation, MinIO storage, and database record creation.

## Context

TASK-016 configures MinIO. This task creates the upload API.

## Requirements

- Create Document model (id, organization_id, filename, mime_type, storage_key, size, status, error_message, created_by, created_at, updated_at)
- Create upload endpoint `POST /api/v1/documents`
- Accept multipart/form-data
- Validate file type (PDF, TXT, DOCX)
- Validate file size
- Store in MinIO
- Create database record with status UPLOADED
- Return document metadata
- Create list endpoint `GET /api/v1/documents`
- Create detail endpoint `GET /api/v1/documents/{id}`
- Create delete endpoint `DELETE /api/v1/documents/{id}`
- Create migration

## Files Expected To Change

- `backend/app/models/document.py` (new)
- `backend/app/api/documents.py` (new)
- `backend/app/services/document_service.py` (new)
- `backend/app/schemas/document.py` (new)

## Implementation Plan

1. Create Document model
2. Create schemas
3. Create document service
4. Create upload endpoint
5. Create list/detail/delete endpoints
6. Create migration
7. Test upload flow

## Acceptance Criteria

- [ ] Document upload works
- [ ] File validation rejects invalid files
- [ ] Document record created in database
- [ ] List documents works
- [ ] Delete document works
- [ ] Tenant isolation enforced

## Tests Required

- [ ] Upload creates record
- [ ] Invalid file rejected
- [ ] Delete removes record

## Dependencies

- TASK-016

## Notes

None

## Completion

Not completed.
