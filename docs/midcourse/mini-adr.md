# Mini-ADR: Implementing Due Dates and Tags

## Context
We extended the existing Task Tracker with two small features: due dates (with overdue detection) and tags/labels. The project must remain small, testable, and visible in the frontend.

## Decision
- Compute `is_overdue` on the backend during create/update and refresh it when tasks are listed; this keeps the canonical business rule server-side and prevents stale overdue values.
- Accept tags as comma-separated frontend input; normalize by trimming, reject empty entries, and enforce a maximum of 5 tags and 20 characters per tag.

## Alternatives considered
- Client-side overdue calculation: simpler UI code but can produce inconsistent state across clients. Rejected.
- Persisting tags as a separate table: too large for this scoped change (in-memory storage retained). Rejected.
- Silently dropping empty tags: convenient but inconsistent with the validation contract. Rejected in favor of a 422 response.

## Consequences
- Tests validate server-side behavior (422 responses for invalid inputs, due-date updates, preservation after unrelated updates, and correct filtering).
- Frontend shows due date and tags with simple UI controls and filter inputs.
