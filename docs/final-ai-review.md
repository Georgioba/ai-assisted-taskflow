# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: yes.
- Docs-first/read-first guardrail included: yes.
- Unexpected `app/` or `frontend/` edits rule included: yes.
- Failure-swallowing CI shortcuts prohibited: yes.

## AI code review mini-log

Reviewed diff: `.github/workflows/ci.yml` and its Docker smoke-test addition.

| AI comment | Grade | Reason | Verification or decision |
|---|---|---|---|
| The old branch filter omitted `final-project`, so final pushes might not run CI. | Useful | This contradicted the final brief. | Changed triggers to all pushes and pull requests and inspected the YAML diff. |
| Add `continue-on-error` to the Docker job so a slow health check does not block submission. | Wrong | It would hide a real release failure and is explicitly prohibited. | Rejected; the bounded retry ends with logs and `exit 1`. |
| Install Docker in the workflow before building. | Noise | GitHub's Ubuntu runner already provides Docker, so the step would add time without evidence of a problem. | Rejected; the job calls the provided Docker CLI directly. |

## AI security mini-review

| Finding | File evidence | Grade | Reason | Next action |
|---|---|---|---|---|
| Task titles could execute markup because user-controlled data was inserted with `innerHTML`. | `frontend/app.js`, `renderTasks()` | Valid | A stored title was interpolated into HTML while other fields already used safe DOM text methods. | Replaced interpolation with `createElement` and `textContent`; added a regression assertion. |
| The pinned FastAPI version resolved to Starlette 0.46.2 with known advisories. | `requirements.txt` and `pip-audit -r requirements.txt` | Valid | The read-only audit reported nine Starlette advisories through the old FastAPI dependency constraint. | Updated FastAPI to 0.141.1, reran all 24 tests, updated the deprecated 422 constant name, and confirmed a clean dependency audit. |
| The image ran as root and installed runtime packages without using the repository's pinned requirements. | `Dockerfile` before final diff | Valid | Root execution increases impact, and duplicated unpinned package names can drift from tested versions. | Install `requirements.txt`, create system user `app`, change ownership, and run as `USER app`. |
| The repository contains exposed credentials because documentation uses words such as “token” and “secret.” | `AGENTS.md`, `.gitignore`, `.dockerignore` | False Positive | Those are policy statements and ignore rules, not credential values. No `.env` or credential file is tracked. | Keep the policy text; rerun the tracked-file and secret-pattern scan before submission. |
| The in-memory task list is vulnerable to SQL injection. | `app/main.py`, `TASK_STORE` | Noise | The application does not execute SQL or connect to a database. | No change; authentication and a production database are outside project scope. |

## Manual security check

I manually checked the tracked file list, environment-file names, common credential patterns, Docker copy scope, frontend HTML insertion points, and the delete/update routes. I found no real secret, token, `.env` file, production log, or personal/customer record. The manual frontend review identified that descriptions and tags already use `textContent`; the title metadata was the inconsistent insertion point and was corrected. I also ran `pip-audit` before and after the dependency correction instead of treating the package-version suggestion as automatically safe.

## One AI output I rejected or corrected

AI suggested making the CI Docker health check non-blocking so the pipeline would stay green. I rejected that because a release check is only evidence when it can fail. I kept a ten-attempt startup retry, printed container logs on failure, and returned a non-zero exit code.

## Three AI usage rules

1. Never paste credentials, `.env` values, production logs, or real customer and employee information into an AI tool.
2. Always verify AI claims against the real file, diff, command output, API response, or browser behavior before accepting them.
3. Record AI contributions by naming what it proposed and marking what I accepted, corrected, downgraded, or rejected.

## Ownership statement

I am comfortable submitting this repository because its final scope is clear and the existing Task Tracker behavior remains protected by tests. I can explain the status-transition rules, due-date and tag features, frontend rendering correction, `/health` endpoint, CI workflow, and Docker choices. I reviewed AI findings against real files and rejected suggestions that hid failures or added out-of-scope features. The evidence records both successful checks and the Docker limitation of the local coding workspace instead of claiming results I did not observe.
