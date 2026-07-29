# Task Tracker

A simple Task Tracker application built with FastAPI, vanilla JavaScript, and Pydantic.

## Project structure

- `app/main.py` — FastAPI backend with CRUD endpoints and static frontend routing
- `app/models.py` — domain models for task creation and updates
- `app/static/` — vanilla JS frontend assets
- `tests/test_main.py` — API tests with pytest
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

## Docker

Build and run the container:

```powershell
docker build -t task-tracker .
docker run --rm -p 8000:8000 task-tracker
```

Then open `http://127.0.0.1:8000`.

## Documentation

Additional project documentation is available in the `docs/` directory:

- `docs/user-stories.md`
- `docs/mini-adr.md`
- `docs/prompt-log.md`
- `docs/verification.md`
- `docs/reflection.md`

## Branch workflow

1. Create a feature branch: `git checkout -b feature/due-date-tags`
2. Commit incremental changes.
3. Push and open a pull request for review.
