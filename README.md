# Task Tracker

A simple Task Tracker application built with FastAPI, vanilla JavaScript, and Pydantic.

## Project structure

- `app/main.py` — FastAPI backend with CRUD endpoints and static frontend routing
- `app/business_rules.py` — allowed task status transitions
- `app/models.py` — domain models for task creation and updates
- `app/static/` — vanilla JS frontend assets
- `tests/` — baseline and mid-course feature tests with pytest
- `docs/midcourse/` — required AI-assisted workflow evidence
- `.github/workflows/ci.yml` — CI pipeline for installs and tests
- `Dockerfile` — container image for the FastAPI app

## Install

```powershell
python -m pip install -r requirements.txt
```

## Run locally

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000` in your browser.

## Run tests

```powershell
pytest
```

## Task status workflow

The backend enforces these transitions:

- `TODO` → `IN_PROGRESS`
- `IN_PROGRESS` → `DONE`
- `DONE` → `IN_PROGRESS` (reopen)

Skipping directly from `TODO` to `DONE` and updating to the same status return
HTTP 422.

## Docker

Build and run the container:

```powershell
docker build -t task-tracker .
docker run --rm -p 8000:8000 task-tracker
```

Then open `http://127.0.0.1:8000`.

## Documentation

Required project documentation is available in `docs/midcourse/`:

- `docs/midcourse/user-stories.md`
- `docs/midcourse/mini-adr.md`
- `docs/midcourse/prompt-log.md`
- `docs/midcourse/verification.md`
- `docs/midcourse/reflection.md`

## Submission branch

The assessed version is on the `mid-course-project` branch.

```powershell
git switch mid-course-project
```
