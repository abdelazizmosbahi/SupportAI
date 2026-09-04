# TASK-023 — Configure Ollama and LLM Provider Abstraction

## Status

TODO

## Objective

Create an LLM provider abstraction and implement the Ollama provider for local LLM inference.

## Context

TASK-022 retrieves chunks. This task configures the LLM for Phase 6 — RAG.

## Requirements

- Create LLMProvider abstract base class
- Create OllamaProvider implementation
- Support `generate` and `stream` methods
- Configure model via environment variable (default: qwen or llama)
- Create Ollama service wrapper
- Add httpx for HTTP requests to Ollama
- Test Ollama connection

## Files Expected To Change

- `backend/app/llm/base.py` (new)
- `backend/app/llm/ollama_provider.py` (new)
- `backend/app/llm/factory.py` (new)
- `backend/app/core/config.py` (update)

## Implementation Plan

1. Create LLM provider interface
2. Implement Ollama provider
3. Create provider factory
4. Configure via environment
5. Test connection

## Acceptance Criteria

- [ ] LLM provider abstraction created
- [ ] Ollama provider implements interface
- [ ] Generate method works
- [ ] Stream method works
- [ ] Model configurable via env var

## Tests Required

- [ ] Provider factory test
- [ ] Ollama connection test

## Dependencies

- TASK-007

## Notes

Model choice depends on available hardware.

## Completion

Not completed.
