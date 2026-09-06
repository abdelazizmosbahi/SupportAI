# TASK-017 — Implement Document Upload API

## Status

DONE

## Objective

Implement document upload endpoint with file validation, MinIO storage, and database record creation.

## Context

TASK-016 configures MinIO. This task creates the upload API.

## Requirements

- [x] Create Document model (id, organization_id, filename, mime_type, storage_key, size, status, error_message, created_by, created_at, updated_at)
- [x] Create upload endpoint `POST /api/v1/documents`
- [x] Accept multipart/form-data
- [x] Validate file type (PDF, TXT, DOCX)
- [x] Validate file size
- [x] Store in MinIO
- [x] Create database record with status UPLOADED
- [x] Return document metadata
- [x] Create list endpoint `GET /api/v1/documents`
- [x] Create detail endpoint `GET /api/v1/documents/{id}`
- [x] Create delete endpoint `DELETE /api/v1/documents/{id}`
- [x] Create migration

## Files Expected To Change

- `backend/app/models/document.py` (new)
- `backend/app/api/documents.py` (new)
- `backend/app/services/document_service.py` (new)
- `backend/app/schemas/document.py` (new)

## Implementation Plan

1. [x] Create Document model
2. [x] Create schemas
3. [x] Create document service
4. [x] Create upload endpoint
5. [x] Create list/detail/delete endpoints
6. [x] Create migration
7. [x] Test upload flow

## Acceptance Criteria

- [x] Document upload works
- [x] File validation rejects invalid files
- [x] Document record created in database
- [x] List documents works
- [x] Delete document works
- [x] Tenant isolation enforced

## Tests Required

- [x] Upload creates record
- [x] Invalid file rejected
- [x] Delete removes record

## Dependencies

- TASK-016

## Notes

Endpoints are mounted under `/organizations/{org_id}/documents` (with `org_id`
scoping) so tenant isolation flows through the existing
`require_permission` → `resolve_tenant` boundary, matching the existing
organizations/members routing style.

## Completion

Completed.
