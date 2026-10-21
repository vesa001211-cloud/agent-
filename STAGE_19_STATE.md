# Stage 19 — Runtime State

## Goal
Define the minimum state required to continue a conversation safely.

## State model
- `Config` — runtime configuration.
- `Persona` — current character definition.
- `MemoryStore` — persistent local sessions, messages, and memories.
- `ConversationEngine.session_id` — active conversation session.

## Persistence
SQLite stores sessions, messages, and explicit memories. The database lives under the local data directory and is not part of the Git repository.

## Exit criteria
The process can start a new session, append messages, retrieve recent history, and close without losing committed database records.
