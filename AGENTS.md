# Repository instructions for AI coding agents

## Read first

Before proposing a change, read `README.md`, the relevant source file, its tests, and the evidence document affected by the task. Treat repository code and test results as the source of truth; do not invent endpoints, status codes, commands, or behavior.

## Stack and layout

- Python 3.12, FastAPI, Pydantic, Uvicorn
- Vanilla HTML and JavaScript in `frontend/`
- pytest and HTTPX tests in `tests/`
- In-memory task storage for this course project
- CI in `.github/workflows/ci.yml`
- Container definition in `Dockerfile`

## Commands

```bash
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
python -m pytest
docker build -t task-tracker .
docker run --rm --name task-tracker -p 8000:8000 task-tracker
curl --fail http://127.0.0.1:8000/health
```

## Project rules

- Do not add product features during final release work.
- Preserve the status-transition rules in `app/business_rules.py`.
- Keep API, frontend, tests, README, and evidence documents consistent.
- Never add secrets, tokens, credentials, `.env` files, production logs, or personal/customer data.
- Do not use `continue-on-error`, `|| true`, skipped tests, or other failure-swallowing shortcuts in CI.
- Prefer small, reviewable changes and run the full test suite after each meaningful change.

## Guardrails

- Work docs-first/read-first: state the claim or risk, inspect the real file, then propose a bounded change.
- Do not modify `app/` or `frontend/` unless the requested work requires a small bug fix, security fix, or documented correction.
- If an AI task unexpectedly changes `app/` or `frontend/`, stop and explain the diff before continuing.
- Do not rewrite working files only for style.
- Record accepted, corrected, downgraded, or rejected AI suggestions in the relevant evidence document.
- If a command cannot be run in the current environment, report that honestly instead of claiming success.
