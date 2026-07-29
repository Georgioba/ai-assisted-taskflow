# Mini-ADR: Implementing Due Dates and Tags

## Context
We extended the existing Task Tracker with two small features: due dates (with overdue detection) and tags/labels. The project must remain small, testable, and visible in the frontend.

## Decision
- Compute `is_overdue` on the backend during task create/update; this keeps the canonical business rule server-side and avoids UI drift.
- Accept tags as comma-separated input; normalize by trimming and dropping empty entries; enforce a maximum of 5 tags and 20 chars per tag.

## Alternatives considered
- Client-side overdue calculation: simpler UI code but can produce inconsistent state across clients. Rejected.
- Persisting tags as a separate table: too large for this scoped change (in-memory storage retained). Rejected.

## Consequences
- Tests validate server-side behavior (422 responses for invalid inputs, correct filtering).
- Frontend shows due date and tags with simple UI controls and filter inputs.
