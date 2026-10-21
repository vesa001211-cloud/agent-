# Stage 15 — Application Runtime

## Goal
Create one predictable entry point that initializes local state and starts the companion.

## Implemented
- `main()` parses CLI arguments.
- Configuration is loaded before runtime initialization.
- Local data directory is created automatically.
- SQLite memory store is opened before the conversation loop.
- Conversation engine is created from configuration, memory, and persona.
- Shutdown closes the database cleanly.

## Exit criteria
Running `python agent.py` reaches the interactive prompt instead of requiring a framework or cloud service.
