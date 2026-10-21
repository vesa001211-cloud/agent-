# Stage 16 — Command Line Interface

## Goal
Provide a simple local interface for development and testing.

## Commands
- `/help` — show commands
- `/memory` — inspect stored local memories
- `/exit` — quit

Normal text is sent to the conversation engine.

## Design
The CLI is intentionally thin. It should not contain personality, memory, or model logic.

## Exit criteria
A user can start the program, enter text, inspect local memory, and exit cleanly from a terminal.
