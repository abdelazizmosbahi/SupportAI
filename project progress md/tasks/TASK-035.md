# TASK-035 — Implement Rate Limiting

## Status

TODO

## Objective

Implement API rate limiting using Redis.

## Context

TASK-034 completes UI. This task starts Phase 11 — Security.

## Requirements

- Create rate limiting middleware using Redis
- Configure rate limits per endpoint type:
  - Login: 5 requests/minute
  - General API: 100 requests/minute
  - AI: 20 requests/minute
- Return 429 with proper headers
- Make limits configurable via environment

## Files Expected To Change

- `backend/app/core/rate_limit.py` (new)
- `backend/app/main.py` (update)

## Implementation Plan

1. Create rate limiter
2. Configure per-endpoint limits
3. Add to middleware
4. Test rate limiting

## Acceptance Criteria

- [ ] Rate limiting works
- [ ] Different limits per endpoint
- [ ] 429 returned when exceeded
- [ ] Configurable via env

## Tests Required

- [ ] Rate limit test

## Dependencies

- TASK-007

## Notes

None

## Completion

Not completed.
