# Offline AI Companion

A Python-first, offline AI companion designed to communicate naturally, maintain a consistent character, remember useful information, and eventually work as a local code/file agent.

## Status

- **Planning:** Stages 1–10 documented.
- **Foundation implementation:** Stages 11–20 completed.
- **Current entry point:** `agent.py`.
- **Target-device model test:** still required for hardware-specific validation.

## Design documents

| Stage | Document | Purpose |
|---|---|---|
| 1 | [PHASE_01.md](PHASE_01.md) | Overall goal, requirements, long-term direction |
| 2 | [STAGE_02_PERSONALITY.md](STAGE_02_PERSONALITY.md) | Configurable identity and stable personality |
| 3 | [STAGE_03_RELATIONSHIP.md](STAGE_03_RELATIONSHIP.md) | Friend-like interaction, continuity, and boundaries |
| 4 | [STAGE_04_MVP.md](STAGE_04_MVP.md) | First-version scope and explicit exclusions |
| 5 | [STAGE_05_OFFLINE_REQUIREMENTS.md](STAGE_05_OFFLINE_REQUIREMENTS.md) | Offline guarantees, permitted network paths, privacy |
| 6 | [STAGE_06_ARCHITECTURE.md](STAGE_06_ARCHITECTURE.md) | Minimal single-file logical architecture |
| 7 | [STAGE_07_HARDWARE.md](STAGE_07_HARDWARE.md) | Hardware tiers and measurable performance data |
| 8 | [STAGE_08_MODEL_SELECTION.md](STAGE_08_MODEL_SELECTION.md) | Initial model candidate and alternatives |
| 9 | [STAGE_09_FEASIBILITY_TEST.md](STAGE_09_FEASIBILITY_TEST.md) | Repeatable local test protocol; device results pending |
| 10 | [STAGE_10_SUCCESS_CRITERIA.md](STAGE_10_SUCCESS_CRITERIA.md) | Planning/prototype exit gates and acceptance metrics |
| 11 | [STAGE_11_REPOSITORY_SETUP.md](STAGE_11_REPOSITORY_SETUP.md) | Repository and source-control baseline |
| 12 | `agent.py` | Single-file application scaffold and core entry point |
| 13 | [STAGE_13_CONFIGURATION.md](STAGE_13_CONFIGURATION.md) | Runtime configuration |
| 14 | [STAGE_14_INTERNAL_STRUCTURE.md](STAGE_14_INTERNAL_STRUCTURE.md) | Logical sections inside the single source file |
| 15 | [STAGE_15_RUNTIME.md](STAGE_15_RUNTIME.md) | Application initialization and lifecycle |
| 16 | [STAGE_16_CLI.md](STAGE_16_CLI.md) | Local terminal interface |
| 17 | [STAGE_17_ERROR_HANDLING.md](STAGE_17_ERROR_HANDLING.md) | Failure behavior and no-cloud fallback rule |
| 18 | [STAGE_18_LOGGING.md](STAGE_18_LOGGING.md) | Privacy-conscious diagnostics |
| 19 | [STAGE_19_STATE.md](STAGE_19_STATE.md) | Runtime and persistent state model |
| 20 | [STAGE_20_FIRST_RUN.md](STAGE_20_FIRST_RUN.md) | End-to-end first-run contract |

## Principles

- Offline-first after installation and model download.
- Local neural model rather than a cloud API.
- Persistent, configurable character.
- Local storage and user control of personal data.
- Minimal source tree; core application logic should remain in `agent.py` unless there is a documented reason to split it.
- Extensible model adapter so the inference engine can change without rewriting the companion logic.
- Explicit security boundaries for future file and code tools.
- Incremental development with testable milestones.

## Initial technical direction

- **Language:** Python 3.11+ is the proposed baseline, pending environment validation.
- **Runtime:** Ollama local API as the initial development target.
- **Model candidate:** `qwen3.5:4b`.
- **Fallback:** `qwen3.5:2b`.
- **Higher-capability comparison:** `qwen3.5:9b`, only where hardware allows.
- **Local storage:** SQLite for structured session data.
- **Application entry point:** `agent.py`.

These model choices are candidates, not benchmark results. The model must be validated on the target computer before it becomes the release default.

## Roadmap

The project is split into 100 incremental steps across 10 phases. Each step should produce an observable, testable result. A larger codebase is acceptable only when each subsystem remains understandable and useful.

Large model files, local databases, private logs, secrets, and personal configuration must not be committed to this repository.
