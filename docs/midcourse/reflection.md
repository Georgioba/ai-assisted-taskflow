# Reflection

I used AI (Copilot-style assistant) to sketch and implement two small, end-to-end features: due dates with overdue detection, and tags/labels with filtering. The AI helped me generate code snippets for models, validators, frontend DOM updates, and pytest cases; this sped up iteration and suggested useful test cases.

One moment AI helped: when I asked for tests for overdue detection, it suggested an `AsyncClient`-based structure which I adapted to the project's `ASGITransport` setup — that saved time on test scaffolding.

One moment AI slowed me down: an early AI suggestion computed overdue status purely in the UI, which would have created inconsistent server-client state; I spent time reworking prompts and verifying server-side computation instead of immediately accepting the suggestion.

One place my review changed the result: AI proposed allowing unlimited tags; I constrained the design to 5 tags and 20 chars each to keep the UI and tests simple.

Overall, I used an iterative loop: prompt, inspect, run tests, and adjust. The repository shows the final accepted changes and the docs explain the decisions, prompts, and verification evidence.
