# Stage 14 — Internal Structure

## Goal
Keep a single source file while maintaining strong logical boundaries.

## `agent.py` sections
1. Configuration
2. Logging
3. Local storage / memory
4. Persona
5. Model adapter
6. Conversation engine
7. CLI

## Rule
Single-file does not mean unstructured. Each section exposes a small interface so later features can be added without turning the whole program into one giant function.

## Exit criteria
The application has clear boundaries for configuration, persistence, personality, inference, conversation orchestration, and user interaction.
