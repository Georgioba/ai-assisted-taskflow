# Prompt Log

## Feature 1 — Due dates and overdue filter

### Prompt 1: plan and constrain the feature

**Prompt:** “Add optional due-date support to the existing FastAPI Task Tracker. Keep the in-memory architecture, support create and PATCH, calculate overdue status in the backend, expose an overdue filter, and add only the necessary frontend controls.”

**AI response summary:** The AI proposed model fields, a date comparison, an API query parameter, a form date input, and an overdue badge.

**Decision:** I accepted the model, API, and form changes. I edited the original suggestion by moving overdue calculation out of JavaScript and into the backend. I rejected adding a scheduler or database because both were outside the project scope.

### Prompt 2: test the behavior

**Prompt:** “Write focused pytest tests for a valid due date, invalid date format, past-date detection, updating the due date, and `GET /api/tasks?overdue=true`. Use the project’s in-memory store and isolate every test.”

**AI response summary:** The AI returned asynchronous examples using `AsyncClient`.

**Decision:** I accepted the main assertions and edge cases. I edited the harness to use `ASGITransport` and an automatic store-reset fixture. I rejected tests that depended on a running external server because they would make CI less reliable.

### Prompt 3: debug and refactor

**Prompt:** “PATCHing one field must not erase the task’s other fields. Diagnose the update path, preserve omitted values, recalculate overdue status, and keep the response contract unchanged.”

**AI response summary:** The AI identified full-model replacement as the risk and suggested `model_dump(exclude_unset=True)` with `model_copy(update=...)`.

**Decision:** I accepted that update strategy and added a due-date update test. I edited the list endpoint to refresh overdue status so it does not become stale as dates pass. I rejected client-side-only recalculation because the API must remain the source of truth.

## Feature 2 — Tags and tag filtering

### Prompt 1: weak prompt rewritten

**Weak prompt:** “Add tags to tasks.”

**Why it was weak:** It did not define input format, limits, validation, filtering, update behavior, or frontend expectations. The AI returned a permissive implementation with unlimited tags.

**Stronger prompt:** “Add tags to Task Tracker create and PATCH operations. Trim every tag, reject empty values, allow at most five tags, limit each tag to twenty characters, preserve tags during unrelated updates, add case-insensitive `GET /api/tasks?tag=...`, and render tag chips plus a compact tag filter in the frontend.”

**AI response summary:** The stronger prompt produced a bounded validator, API filter, frontend input, and tag-chip rendering.

**Decision:** I accepted the small list-based design. I edited validation so empty values return 422 instead of being silently removed. I rejected a separate tag database table and unlimited tags as unnecessarily complex.

### Prompt 2: test tags

**Prompt:** “Add pytest tests for empty tag rejection, too many tags, tag filtering, tag updates, and preservation after an unrelated PATCH. Assert status codes and response bodies.”

**AI response summary:** The AI proposed success and failure-path tests.

**Decision:** I accepted the suggested coverage and added an explicit preservation assertion. I edited the empty-tag test to match the final 422 contract. I rejected a UI-only test because validation belongs to the backend and must also protect API clients.

### Prompt 3: frontend integration

**Prompt:** “Add a comma-separated tag field to the existing create/edit form, render safe tag chips on cards, and add a tag filter without removing the existing task list or empty state.”

**AI response summary:** The AI generated DOM code, filter query construction, and chip styles.

**Decision:** I accepted the basic UI integration. I edited labels, CSS, and parsing so the form does not send blank entries. I rejected animations and a tag-management panel because they did not improve the assessed end-to-end behavior.

## Review outcome

For every prompt, I inspected the proposed change, ran the relevant test or manual check, and recorded what I accepted, edited, or rejected. The final code reflects these reviewed decisions rather than the AI’s first response.
