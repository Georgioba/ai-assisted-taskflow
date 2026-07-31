# My AI Playbook

## When I reach for AI first

I use AI first when a task is bounded and I can verify the result: drafting test cases, explaining an error message, reviewing a small diff, checking documentation against code, or proposing a CI/Docker checklist. In this project, AI was especially useful for listing edge cases for due dates, tags, null updates, and status transitions.

## When I do not reach for AI first

I slow down when the task contains private data, unclear requirements, security-sensitive choices, or a change I do not understand. I also do not ask AI to redesign a working application when the assignment is only about release readiness. I read the brief and repository first so the prompt contains real constraints.

## My non-negotiables

- Never paste passwords, tokens, `.env` values, credentials, production logs, or real customer/employee data.
- Never submit an AI change I cannot explain.
- Never hide failing tests with `continue-on-error`, `|| true`, skipped commands, or rewritten evidence.
- Keep changes small and inside the requested scope.
- Treat code, tests, runtime behavior, and official requirements as stronger evidence than a confident AI answer.

## My review rules

I inspect the diff, identify each changed behavior, and run the closest test before running the full suite. I grade review findings as Useful, Noise, or Wrong and security findings as Valid, False Positive, or Noise. I check generated documentation against real commands and endpoints. When AI recommends extra features or complexity, I reject it unless the requirement and verification plan justify it.

## What I am still figuring out

I am still learning when a second AI review adds useful independent evidence and when it only repeats the first answer. I also want clearer team rules for recording AI contributions without creating long logs that nobody reads.

## Decision Card

| Situation | My decision |
|---|---|
| New feature | Ask for a small plan and acceptance criteria; confirm it is in scope before code. |
| Code review | Require file evidence, grade every comment, and verify useful comments with tests or inspection. |
| Debugging | Start from the failing output and reproduce it; do not let AI guess the cause without evidence. |
| Infrastructure | Review every CI and Docker line, pin the runtime version, and make checks fail honestly. |
| Never paste | Credentials, secrets, `.env` values, private logs, or real personal/customer data. |
| One rule | AI proposes; I inspect, test, decide, and own the final result. |
