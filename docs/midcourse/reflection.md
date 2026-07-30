# Reflection

I used ChatGPT/Codex as an AI coding assistant for planning, implementation suggestions, test design, debugging, and documentation. I used GitHub to keep the source and workflow visible, and pytest to decide whether an AI-generated change was acceptable. The two selected features were due dates with overdue filtering and tags with tag filtering. Both features required backend models and validation, API behavior, frontend controls, card display, and tests.

The AI was most helpful when it proposed an `AsyncClient` and `ASGITransport` test structure for the FastAPI application. That gave me a useful starting point for testing create, update, and filter behavior without starting a separate server. I did not accept the snippets blindly: I adapted them to the existing in-memory store, added an automatic reset fixture, and checked response bodies as well as status codes.

The AI also slowed me down. Its first due-date suggestion calculated overdue status only in JavaScript. That looked simple, but it would allow the API and frontend to disagree. I rejected that approach and kept the business rule in the backend. I later improved it so overdue values are refreshed when tasks are listed, preventing a future-dated task from remaining incorrectly marked after the date passes.

My review changed the tags result significantly. The first suggestion allowed unlimited tags and silently removed empty values. I limited tasks to five tags, limited each tag to twenty characters, and made empty tag values return 422. I then added tests for invalid tags, tag preservation after unrelated updates, tag filtering, and due-date updates.

Facilitator feedback later exposed three baseline gaps that my first review
missed: status transitions were not enforced, an explicit null title was
accepted, and frontend cards were created but never added to the page. I
reproduced each failure before editing. I then added a small transition rule,
rejected explicit null titles, restored the missing DOM insertion, and added
five regression tests. This also corrected my verification evidence: checking
an API response is not enough to claim that the UI displayed the result.

I used Break Tests to confirm that important tests were meaningful. When I deliberately changed the tag limit from five to six, the tag-limit test failed. When I reversed the overdue comparison, the overdue test failed. After restoring the correct code and applying the feedback fixes, all 17 tests passed. This process showed me that AI can accelerate coding, but I still need to define the contract, inspect every suggestion, test failure paths, verify the visible result, and keep ownership of the final decision.
