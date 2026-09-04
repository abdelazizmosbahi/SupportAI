# TASK-020 — Configure pgvector and Implement Chunking

## Status

TODO

## Objective

Configure pgvector extension and implement text chunking for document processing.

## Context

TASK-019 extracts text. This task adds chunking for Phase 5 — Embeddings.

## Requirements

- Enable pgvector extension in PostgreSQL
- Create DocumentChunk model (id, document_id, organization_id, content, chunk_index, embedding, metadata, created_at)
- Implement text chunking with configurable chunk_size and overlap
- Update document processing worker to chunk text
- Create migration for document_chunks table
- Create vector index

## Files Expected To Change

- `backend/app/models/document_chunk.py` (new)
- `backend/app/workers/document_worker.py` (update)
- `backend/app/services/chunking_service.py` (new)

## Implementation Plan

1. Enable pgvector
2. Create DocumentChunk model
3. Implement chunking service
4. Update document worker
5. Create migration
6. Test chunking

## Acceptance Criteria

- [ ] pgvector extension enabled
- [ ] DocumentChunk model created
- [ ] Text chunking works with configurable size
- [ ] Overlap works correctly
- [ ] Chunks stored in database
- [ ] Migration applies

## Tests Required

- [ ] Chunking produces correct chunks
- [ ] Overlap works
- [ ] Metadata preserved

## Dependencies

- TASK-019

## Notes

Chunk size: 500-1000 tokens. Overlap: 50-150 tokens.

## Completion

Not completed.
