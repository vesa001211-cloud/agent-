# Stage 4 — Version 0 Scope (MVP)

## Goal

Define the smallest useful release that proves this project can behave like a natural, character-driven AI companion locally. This is a scope decision, not the implementation itself.

## Version 0 user experience

The user runs `python agent.py` (or a documented subcommand), talks to the companion in a terminal, and receives responses from a model running on the same computer. The first version should be simple to launch and easy to debug.

## Included in Version 0

1. **Local conversation:** multi-turn text chat through a terminal interface.
2. **Local neural model:** inference through a model runtime on the same device; no cloud-model fallback.
3. **Configurable character:** name, identity description, tone, friendliness, humor, verbosity, language preference, and core traits.
4. **Consistent instruction hierarchy:** application rules, stable persona, session context, then the current user message.
5. **Short-term continuity:** recent turns are included in the model context with a hard limit.
6. **Local session history:** conversations may be saved locally so the user can inspect or resume them; raw history is not automatically treated as verified long-term memory.
7. **Basic controls:** help, exit, clear/reset current context, show current model/runtime status, and handle missing model or runtime errors clearly.
8. **Offline operation after setup:** ordinary conversation keeps working when external network access is disabled.
9. **Explicit disclosure:** the product is an AI system; it must not invent human experiences or memories.
10. **Small dependency footprint:** core app logic remains in `agent.py`; model files and user data stay outside the Git repository.

## Not included in Version 0

- Training a new foundation model from scratch.
- Automatic emotional manipulation, gamified affection scores, or forced intimacy.
- Advanced semantic long-term memory, automatic memory extraction, embeddings, or vector databases.
- Voice input/output, avatar, graphical interface, image understanding, web browsing, or phone app.
- Autonomous file edits, unrestricted shell commands, arbitrary code execution, or repository-wide coding agent behavior.
- Multi-user accounts, network server deployment, telemetry, or cloud sync.

Those features can be considered in later roadmap stages after the conversational foundation is reliable.

## Proposed interaction commands

The exact aliases can be finalized during implementation, but the first release should offer equivalents of:

- `/help` — show supported commands.
- `/exit` — close the session safely.
- `/reset` — clear the active conversation context, with confirmation if saved data could be affected.
- `/model` — show the configured local model and runtime status.
- `/history` — show local saved sessions, if session persistence is enabled.

Commands must not be confused with ordinary user messages; a command is only invoked through a documented prefix.

## Local data

Conversation history and settings belong in a user-data directory, not in the source tree. SQLite is the proposed store for session metadata and transcript records. The application should provide clear behavior for a first run and for a missing/corrupt database.

The MVP does not infer permanent user facts from every sentence. Durable memory extraction and user-controlled memory management are a separate, explicitly planned capability.

## Acceptance criteria

The MVP scope is accepted when a release can be tested against all of these:

- The app starts with a clear error when the local model runtime is missing.
- The app successfully performs a multi-turn chat using the configured local model.
- Character settings affect responses and remain stable during a session.
- Context length is bounded; a long transcript cannot grow the prompt without limit.
- A session can end cleanly without losing already committed local history.
- With external network access disabled, a previously downloaded model still answers.
- No request content is sent to a cloud API by this application.
- No model weights, personal database, secrets, or user logs are committed to GitHub.

## Scope rule

A proposed feature is not part of Version 0 unless it is necessary for one of the acceptance criteria above. This keeps the first usable version achievable without limiting the long-term vision.
