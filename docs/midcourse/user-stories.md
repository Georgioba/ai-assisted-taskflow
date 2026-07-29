# User Stories

## Feature A — Due dates + overdue filter

1. As a user, I want to add a due date to a task so I can track deadlines.
   - Acceptance criteria: The create/edit form accepts a valid ISO date; the task card shows the due date; creating a task with a past due date marks it as overdue (`is_overdue` = true).
   - AI assumption corrected: AI suggested client-side-only overdue computation; I changed to backend computation to keep the source of truth consistent.

2. As a user, I want to see overdue tasks highlighted so I can prioritize them.
   - Acceptance criteria: Overdue tasks show an "Overdue" pill on cards, and the filter "Show overdue only" returns only overdue tasks.

3. As a user, I want to filter the task list to show only overdue tasks.
   - Acceptance criteria: The GET `/api/tasks?overdue=true` endpoint returns only tasks where `is_overdue` is true and status != DONE.

## Feature B — Tags / labels

1. As a user, I want to add tags to tasks via the create/edit form using comma-separated input.
   - Acceptance criteria: Tags are normalized (trimmed, lower/upper preserved), empty tag entries are removed, maximum 5 tags, maximum 20 characters per tag.
   - AI assumption corrected: AI proposed unlimited tags; I constrained to 5 tags to keep the UI simple.

2. As a user, I want to see tag chips on task cards.
   - Acceptance criteria: Task cards render tag chips for each tag on the task.

3. As a user, I want to filter tasks by tag.
   - Acceptance criteria: GET `/api/tasks?tag=NAME` returns tasks having that tag (case-insensitive match of normalized tag text).


Notes: Each story above is intentionally small and testable end-to-end. At least one story per feature is frontend-visible (due date pill, tag chips, filters).
