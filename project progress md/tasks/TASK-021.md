# TASK-021 — Implement Embedding Generation

## Status

TODO

## Objective

Implement embedding generation using sentence-transformers and store vectors in pgvector.

## Context

TASK-020 creates chunks. This task generates embeddings.

## Requirements

- Install sentence-transformers
- Create embedding service
- Use a lightweight model (e.g., all-MiniLM-L6-v2)
- Generate embeddings for document chunks
- Store embeddings in pgvector column
- Update document processing worker to generate embeddings
- Configure embedding model via environment variable

## Files Expected To Change

- `backend/app/services/embedding_service.py` (new)
- `backend/app/workers/document_worker.py` (update)
- `backend/app/core/config.py` (update)

## Implementation Plan

1. Install sentence-transformers
2. Create embedding service
3. Generate embeddings for chunks
4. Update document worker
5. Test embedding generation

## Acceptance Criteria

- [ ] Embedding generation works
- [ ] Embeddings stored in pgvector
- [ ] Document worker generates embeddings
- [ ] Model configurable via env var

## Tests Required

- [ ] Embedding generation test
- [ ] Storage test

## Dependencies

- TASK-020

## Notes

Model: all-MiniLM-L6-v2 (384 dimensions)

## Completion

Not completed.
