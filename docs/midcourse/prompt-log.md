# Prompt Log (summary)

Feature: Due dates + overdue filter

1) Prompt (initial): "Add due date support to Task Tracker backend and frontend" — AI returned a plan including model changes, form fields, and a date comparison in the UI.
   - What I accepted: model and form changes.
   - What I edited: moved overdue computation to backend rather than UI.

2) Prompt (validation): "Add tests for overdue detection and overdue filter" — AI returned pytest snippets using AsyncClient.
   - What I accepted: structure of tests.
   - What I edited: unified test harness to use `ASGITransport` for compatibility.

3) Prompt (bugfix): "Fix failing date parsing when PATCHing task" — AI suggested `exclude_unset=True` when applying patches; I accepted and applied it.


Feature: Tags / labels

1) Prompt (initial weak): "Add tags to tasks" — AI returned a permissive implementation with no limits.
   - Weak->strong rewrite: "Add tags to tasks, normalize input by trimming, reject empty tags, max 5 tags, max 20 chars per tag, and add tag filtering support in GET /tasks?tag=..." — this produced the final validators.
   - What I rejected: unlimited tags, complex tag relations.

2) Prompt (tests): "Add tests for tag normalization and tag filter" — AI provided tests; I adapted them for the project's test harness and added an edge-case for too many tags.

3) Prompt (frontend): "Render tags as chips and add filter input" — AI generated DOM code; I reviewed and adjusted label text and CSS.


For each prompt above I recorded the AI suggestion, what I accepted, and any edits. The repository contains these prompts and the final edited outputs in `docs/midcourse/prompt-log.md` (abridged here).
