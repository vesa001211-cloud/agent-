# Stage 20 — First Run

## Goal
Reach the first observable end-to-end application state.

## Expected flow
1. Start `python agent.py`.
2. A local data directory is created.
3. Configuration is created if missing.
4. SQLite schema is initialized.
5. The CLI prompt appears.
6. `/help` and `/memory` work without a model call.
7. Normal text is routed through the local model adapter.
8. If the local runtime is unavailable, the user receives a clear error rather than an online fallback.
9. `/exit` closes the database cleanly.

## Important validation note
This stage is implemented in code, but actual model inference still requires the target computer to have the selected local runtime and model installed. Hardware-specific performance remains pending the Stage 9 feasibility test.

## Exit criteria
The software has a complete startup → input → orchestration → local model boundary → persistence → shutdown path, with the final model-inference check performed on the target machine.
