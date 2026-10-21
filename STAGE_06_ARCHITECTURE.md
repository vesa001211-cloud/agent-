# Stage 6 — Application Architecture

## Design principle

The project should remain easy to explore in one primary Python file while keeping logical responsibilities separate. A single file does not mean one giant function: it means clear internal boundaries, explicit interfaces, and tests for each responsibility.

## Initial repository shape

```text
agent-/
├── agent.py
├── README.md
├── PHASE_01.md
├── STAGE_02_PERSONALITY.md
├── STAGE_03_RELATIONSHIP.md
├── STAGE_04_MVP.md
├── STAGE_05_OFFLINE_REQUIREMENTS.md
├── STAGE_06_ARCHITECTURE.md
├── STAGE_07_HARDWARE.md
├── STAGE_08_MODEL_SELECTION.md
├── STAGE_09_FEASIBILITY_TEST.md
└── STAGE_10_SUCCESS_CRITERIA.md
```

The local model and mutable user data are deliberately not placed in this tree.

## Logical components inside `agent.py`

1. **Constants and configuration** — defaults, paths, model name, context limits, and runtime endpoint.
2. **Application errors** — stable error types and human-readable recovery messages.
3. **Persona configuration** — load, validate, and render the stable character configuration.
4. **Local model backend interface** — one application-facing method for generating a reply from structured messages.
5. **Ollama backend** — implements the initial local chat call using Ollama's local HTTP API.
6. **Conversation/context builder** — chooses recent turns, character rules, and current input within a configured context budget.
7. **Local storage** — SQLite persistence for session metadata and conversation turns.
8. **Conversation engine** — orchestrates user input, context assembly, inference, and saving.
9. **Command router** — distinguishes documented slash commands from natural-language messages.
10. **CLI and startup** — verifies config/runtime readiness and starts the conversation loop.
11. **Self-checks and diagnostics** — simple checks for missing runtime, model, inaccessible data path, and storage errors.

Future capabilities such as long-term memory, retrieval, safe file tools, and code intelligence will be added behind explicit interfaces instead of being woven into the model call.

## Core data flow

1. Read user input.
2. If it is a documented command, validate and route that command.
3. Load stable persona settings and relevant session context.
4. Apply a fixed context budget and preserve message roles.
5. Call only the configured local model backend.
6. Display the generated response.
7. Persist the turn locally, with error handling that does not leak private content.
8. Return to the input loop.

## Interface boundaries

The inference engine must not own the user's memories or decide how sessions are stored. The context builder prepares messages; the model backend generates text; the conversation engine coordinates them.

The proposed backend contract is conceptually:

```python
generate(messages, *, options) -> str
```

The concrete type definitions and error signatures will be fixed when the first implementation task begins. The initial implementation should use Python's standard-library HTTP and JSON functionality where practical, avoiding an extra client dependency if it provides no needed capability.

## Context policy

Advertised model context size is not the app's default prompt budget. The application must choose a conservative configurable context size, keep room for the assistant response, and trim or summarize older turns in later phases. The first release may drop the oldest non-system turns when necessary, while preserving system/persona rules and the current user message.

## Storage

Use Python's built-in `sqlite3` for local structured storage. Database schema migrations must be versioned once the schema exists. Transactions should protect complete user/assistant turn writes.

The database path should be in an OS-appropriate user-data directory and must not be hard-coded to a repository path.

## Error and safety boundaries

- A timeout, invalid model response, or stopped runtime must not corrupt chat history.
- Future tool calls must be represented as explicit application functions with validated inputs.
- Do not execute model-generated shell commands automatically.
- Network calls default to loopback only.
- Configuration errors should be actionable without including private prompt contents in logs.

## Test strategy

Test the context builder and command router without a model. Test storage with a temporary database. Test the Ollama adapter with a mocked local HTTP response. Use a separate opt-in smoke test for a real model, since it downloads a model and consumes substantial resources.

## Acceptance criteria

The architecture is ready when each logical component has one responsibility, the model can be replaced without rewriting conversation storage/personality, normal operation is local-only, and the minimal repository structure remains understandable.
