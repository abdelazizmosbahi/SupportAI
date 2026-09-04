# TASK-019 — Implement Document Processing Worker

## Status

TODO

## Objective

Create a Celery worker that processes uploaded documents: extracts text, normalizes it, and updates document status.

## Context

TASK-018 configures Celery. This task creates the document processing pipeline.

## Requirements

- Create document processing Celery task
- Download file from MinIO
- Extract text based on file type:
  - PDF: PyPDF2 or pdfplumber
  - TXT: direct read
  - DOCX: python-docx
- Normalize text (whitespace, encoding)
- Update document status: UPLOADED → PROCESSING → PROCESSED/FAILED
- Handle errors gracefully
- Store extracted text temporarily
- Trigger on document upload

## Files Expected To Change

- `backend/app/workers/document_worker.py` (new)
- `backend/app/services/document_service.py` (update)
- `backend/pyproject.toml` (update)

## Implementation Plan

1. Create document processing task
2. Implement text extraction for each format
3. Integrate with MinIO download
4. Update document status
5. Handle errors
6. Test processing pipeline

## Acceptance Criteria

- [ ] PDF text extraction works
- [ ] TXT text extraction works
- [ ] DOCX text extraction works
- [ ] Document status updates correctly
- [ ] Failed processing sets FAILED status
- [ ] Task triggered on upload

## Tests Required

- [ ] Text extraction tests
- [ ] Status update tests
- [ ] Error handling test

## Dependencies

- TASK-017, TASK-018

## Notes

None

## Completion

Not completed.
