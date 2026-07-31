# Task Tracker

A small Task Tracker built with FastAPI, Pydantic, and vanilla JavaScript. It supports task creation and editing, enforced status transitions, due dates, overdue filtering, tags, and tag filtering.

## Project structure

- `app/` - FastAPI API, models, and business rules
- `frontend/` - browser UI served by the FastAPI app
- `tests/` - pytest API and frontend regression tests
- `docs/midcourse/` - mid-course feature and AI-workflow evidence
- `docs/` - final release, AI-review, and ownership evidence
- `.github/workflows/ci.yml` - pytest and Docker smoke checks
- `Dockerfile` and `.dockerignore` - container configuration

## Install

```bash
python -m pip install -r requirements.txt
```

## Run locally

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000` for the Task Tracker. Check release health with:

```bash
curl --fail http://127.0.0.1:8000/health
```

Expected response: `{"status":"ok"}`.

## Run tests

```bash
python -m pytest
```

## Task status workflow

The backend enforces these transitions:

- `TODO` -> `IN_PROGRESS`
- `IN_PROGRESS` -> `DONE`
- `DONE` -> `IN_PROGRESS` (reopen)

Skipping directly from `TODO` to `DONE` or updating to the same status returns HTTP 422.

## Run with Docker

```bash
docker build -t task-tracker .
docker run --rm --name task-tracker -p 8000:8000 task-tracker
```

In another terminal:

```bash
curl --fail http://127.0.0.1:8000/health
```

The image runs the API as a non-root user and does not copy `.env` files, tests, or documentation into the image.

## Final Project

Branch reviewed: `final-project`

### What this submission demonstrates

- The existing Task Tracker still runs inside the intended course scope.
- CI runs the full pytest suite on push and pull request.
- CI also builds the Docker image, runs it, and checks that `/health` returns HTTP 200.
- AI review, security, and ownership evidence is stored in `docs/`.
- No new product feature was added.

### How to run locally

Install and run commands are in the **Install** and **Run locally** sections above.

### How to run tests

```bash
python -m pytest
```

### How to run with Docker

Use the exact build, run, and health-check commands in **Run with Docker** above.

### Evidence files

- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`

### AI assistance summary

AI helped audit CI, Docker, documentation, and security risks. I verified the result with the full pytest suite, API health checks, frontend regression checks, a repository secret scan, and inspection of every final diff. I rejected suggestions that would add product scope or hide failing checks.

## Mid-course evidence

The earlier due-date and tag feature evidence remains in `docs/midcourse/`.
