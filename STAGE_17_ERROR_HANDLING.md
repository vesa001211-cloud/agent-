# Stage 17 — Error Handling

## Goal
Make failures understandable and prevent silent fallback to an online service.

## Implemented
- Empty user input is ignored.
- Keyboard interruption and EOF shut down the CLI cleanly.
- Database lifecycle errors surface as runtime errors.
- Model connection failures produce an explicit local-runtime message.
- Invalid model responses are rejected instead of being treated as valid text.

## Security rule
A failed local model call must never automatically switch to a cloud API.

## Exit criteria
Common startup, storage, input, and local-model failures produce actionable messages without corrupting local state.
