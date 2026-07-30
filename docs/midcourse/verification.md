# Verification

## Baseline
- Before the focused correction/refactor, the full suite completed with `11 passed, 6 warnings in 0.22s`.
- The warnings were all caused by Pydantic v1-style `@validator` and class-based `Config` usage.
- Baseline smoke contract: `GET /` returned the frontend, `GET /api/tasks` returned 200, and create/update/delete behavior remained available.
- Before the facilitator-feedback correction, `12 passed`, but the three
  reported baseline behaviors were not covered. Reproduction confirmed:
  `TODO` → `DONE` returned 200, `{"title": null}` returned 200 and stored null,
  and `renderTasks()` created cards without inserting them into `#tasks`.

## Current backend test result

```
.................                                                        [100%]
17 passed in 0.22s
```

The final run includes the original tests, the six focused mid-course tests,
and five facilitator-feedback regression tests. It covers valid creation,
invalid date format, empty tags, too many tags, overdue detection/filtering,
tag filtering, tag preservation, due-date updates, valid and invalid status
transitions, explicit-null title rejection, visible card insertion, unrelated
updates, and 404 behavior.

## Frontend and application checks

| Check | Observed result |
|---|---|
| Open the app | PASS — frontend returned 200 and the create form, filters, and board were visible. |
| Execute the real HTML and JavaScript with one API task | PASS — one `.task-card` was inserted into `#tasks`, and its title was visible. |
| Create a task with a due date and tags | PASS — response was 201 and the response preserved the due date and tags. |
| Create a past-due task | PASS — the API returned `is_overdue: true`. |
| Apply “Show overdue only” | PASS — only the overdue task was returned. |
| Filter by `urgent` | PASS — only the task containing that tag was returned. |
| Edit the due date | PASS — the updated date was returned and overdue status was recalculated. |
| Submit an empty tag through the API | PASS — the server returned 422. |
| Update `TODO` directly to `DONE` | PASS — the server returned 422 and retained `TODO`. |
| Update title to explicit null | PASS — the server returned 422 and retained the original title. |

The earlier verification incorrectly claimed that cards were displayed without
checking the final DOM insertion. Facilitator feedback exposed that gap. The
new frontend regression test and DOM execution check now verify the visible
result, not only the API response or card construction.

## Behavior contract before and after refactor

| Contract | Before focused refactor | After refactor |
|---|---|---|
| Valid due date and tags create a task | PASS | PASS |
| Invalid date returns 422 | PASS | PASS |
| More than five tags returns 422 | PASS | PASS |
| Unrelated PATCH preserves tags | PASS | PASS |
| Updating a due date recalculates overdue status | Manually checked | Automated test added; PASS |
| Overdue filter returns only overdue tasks | PASS | PASS |
| Tag filter is case-insensitive | PASS | PASS |
| Empty tag is rejected | Gap: empty values were silently removed | Corrected to 422; PASS |
| `TODO` cannot skip directly to `DONE` | Gap: returned 200 | Corrected to 422; PASS |
| Explicit null title is rejected | Gap: returned 200 and stored null | Corrected to 422; PASS |
| API tasks appear in the board | Gap: cards were built but not inserted | `appendChild` restored and DOM-verified; PASS |

After correcting the empty-tag contract, the model validators were refactored from deprecated Pydantic v1 syntax to Pydantic v2 `field_validator` and `ConfigDict`. The full behavior contract passed afterward with no warnings.

## Break Test evidence

### Break Test 1 — maximum tag count

1. In an isolated copy, changed `if len(normalized) > 5` to `> 6`.
2. Ran `test_too_many_tags_returns_422`.
3. Expected failure occurred: the broken API returned `201` instead of `422`.
4. Restored the correct limit and reran the full suite: PASS.

### Break Test 2 — overdue comparison

1. In a separate isolated copy, reversed the comparison from `due_date < date.today()` to `due_date > date.today()`.
2. Ran `test_overdue_flag_detected`.
3. Expected failure occurred because the past-due task was absent from the overdue results.
4. Restored the correct comparison and reran the full suite: PASS.

These failures show that both tests protect real behavior rather than passing regardless of the implementation.
