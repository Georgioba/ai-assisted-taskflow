# Release Evidence

## Baseline

- Branch: `final-project`, created from the completed mid-course work.
- Date: 2026-07-31.
- Baseline test command: `UV_CACHE_DIR=/tmp/georgio-final-uv-cache uv run --with-requirements requirements.txt python -m pytest -q`.
- Baseline test result: `22 passed in 0.53s`.
- Initial `/health` result: the route was missing, so I added the small release-readiness endpoint required by the final brief.
- Local app run command: `UV_CACHE_DIR=/tmp/georgio-final-uv-cache uv run --with-requirements requirements.txt uvicorn app.main:app --host 127.0.0.1 --port 8010`.
- Final `/health` result: HTTP 200 with `{"status":"ok"}`.
- Frontend check: the root route returned the Task Tracker HTML. I checked the board container, create/edit form, due-date and tag controls, filters, and the regression assertion that rendered cards are appended to the visible task container.
- Final test result: `24 passed in 0.28s` after the release and security corrections.
- Dependency audit: `pip-audit -r requirements.txt` returned no known vulnerabilities after the FastAPI update.

## Scope control

No product feature was added. The only runtime changes were the required `/health` route, moving the existing UI to the required top-level `frontend/` directory, and replacing unsafe title interpolation with DOM `textContent`.

## CI evidence

- Workflow file: `.github/workflows/ci.yml`.
- Trigger: every push and pull request, including `final-project`.
- Test command used by CI: `python -m pytest` with Python 3.12 after installing `requirements.txt`.
- Docker check: a dependent job builds the image, runs it, and requires `/health` to succeed.
- Latest run link or note: pending the first pushed `final-project` workflow run; replace this line with the green run URL before submission.
- Shortcut check: no `continue-on-error`, no `|| true`, and pytest is not skipped.

## Docker evidence

- Build command: `docker build -t task-tracker .`.
- Run command: `docker run --rm --name task-tracker -p 8000:8000 task-tracker`.
- Health check: `curl --fail http://127.0.0.1:8000/health` must return `{"status":"ok"}`.
- Non-root check: `Dockerfile` creates and switches to the system user `app`.
- No-baked-secrets check: `.dockerignore` excludes `.env`, `.env.*`, Git data, caches, tests, and docs; the Dockerfile copies only requirements, `app/`, and `frontend/`.
- Local environment note: Docker was not installed in the coding workspace, so the image verification is enforced by the GitHub Actions Docker smoke job rather than falsely recorded as a local success.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| The test command runs the complete suite. | Ran `python -m pytest -q` through the pinned requirements environment. | Pass: 24 tests with no warnings. | README and CI both use `python -m pytest`. |
| `/health` returns HTTP 200 and JSON status. | Started Uvicorn and called the endpoint with `curl --fail`. | Pass: `{"status":"ok"}`. | Added the missing route and a regression test. |
| The frontend is served at `/` and cards enter the visible task list. | Root response, `frontend/index.html`, `frontend/app.js`, and frontend regression tests. | Pass. | Moved existing assets to `frontend/`; updated paths without redesigning the UI. |
| Invalid `TODO` to `DONE` transitions return 422. | `app/business_rules.py` and `test_todo_to_done_transition_returns_422`. | Pass. | No behavior change. |
| Docker uses a clear non-root runtime command and contains the frontend. | `Dockerfile`, `.dockerignore`, and CI Docker smoke job. | Configured; CI run URL pending. | Added pinned dependency install, frontend copy, non-root user, and health smoke test. |
