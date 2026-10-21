# Stage 11 — Repository Setup

## Goal
Establish a clean, reproducible repository baseline before application implementation.

## Decisions
- Default branch: `main`.
- Core application entry point: `agent.py`.
- Minimal source tree is a project constraint.
- Design documents stay in the repository root for easy inspection.
- Model weights, SQLite databases, private logs, secrets, caches, and personal configuration are excluded from version control.
- No cloud API is required by the application architecture.

## Repository contract
A fresh checkout must contain enough source and documentation to understand the project without requiring hidden files.

## Exit criteria
- Repository is reachable and writable.
- `README.md` documents the project direction.
- Stages 1–10 are documented.
- Stage 11 establishes the implementation baseline.
