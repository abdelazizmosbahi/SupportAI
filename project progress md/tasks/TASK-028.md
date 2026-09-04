# TASK-028 — Implement Tickets and Human Handoff

## Status

TODO

## Objective

Implement the ticket system for human handoff when AI confidence is low or customer requests a human agent.

## Context

TASK-027 builds chat UI. This task adds Phase 8 — Human Handoff.

## Requirements

- Create Ticket model (id, organization_id, conversation_id, assigned_agent_id, status, priority, reason, created_at, updated_at)
- Create ticket CRUD endpoints
- Implement auto-escalation on low confidence
- Create agent assignment
- Track ticket status (OPEN, IN_PROGRESS, RESOLVED, CLOSED)
- Create migration

## Files Expected To Change

- `backend/app/models/ticket.py` (new)
- `backend/app/api/tickets.py` (new)
- `backend/app/services/ticket_service.py` (new)
- `backend/app/schemas/ticket.py` (new)

## Implementation Plan

1. Create Ticket model
2. Create schemas
3. Create ticket service
4. Create API endpoints
5. Create migration
6. Test ticket flow

## Acceptance Criteria

- [ ] Ticket creation works
- [ ] Agent assignment works
- [ ] Status updates work
- [ ] Auto-escalation triggers
- [ ] Tenant isolation enforced

## Tests Required

- [ ] Ticket CRUD test
- [ ] Escalation test

## Dependencies

- TASK-025

## Notes

None

## Completion

Not completed.
