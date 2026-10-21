# Stage 18 — Logging

## Goal
Provide enough diagnostics to understand failures without turning logs into a privacy leak.

## Implemented
- Standard-library logging is used.
- Debug mode is opt-in with `--debug`.
- Normal logs go to stderr.
- User messages and model responses are not automatically logged by the logger.

## Privacy rule
Do not add conversation-content logging by default. If future diagnostics require it, make the behavior explicit and local.

## Exit criteria
Runtime failures can be diagnosed from structured log messages while conversation content remains out of normal logs.
