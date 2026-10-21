# Stage 10 — Success Criteria and Phase 1 Exit Gate

## Purpose

Turn the project vision into observable criteria. “It feels smart” or “the code is big” are not acceptance tests.

## Phase 1 completion versus software completion

There are two distinct gates:

- **Planning gate:** the requirements and architecture for the first release are written, consistent, and testable.
- **Prototype gate:** the implementation runs on the intended computer and passes the measurable tests below.

The planning gate can be completed in GitHub. The prototype gate cannot be claimed until code and target-device tests exist.

## Planning gate

Phase 1 documentation is ready when:

- the project goal and long-term direction are documented;
- persona and relationship behavior are specified;
- MVP scope and exclusions are explicit;
- offline behavior and network boundaries are documented;
- single-file logical architecture and storage direction are defined;
- hardware tiers and model candidates are recorded;
- a reproducible local feasibility test exists;
- success metrics and pass/fail thresholds are explicit;
- unresolved empirical decisions are clearly marked pending rather than guessed.

## Prototype gate — initial release

The first usable prototype will be accepted only when all critical items pass:

### Product behavior
- A user can start a terminal conversation without an account.
- The system uses a local neural model and supports multi-turn text conversation.
- The configured character affects responses consistently across a fixed test set.
- The model does not invent stored memories when none are available.
- Context use is bounded and handles a long session without uncontrolled prompt growth.
- Basic commands (help, exit, reset, model status) behave predictably.

### Offline and privacy
- After setup, a chat succeeds with external network access disabled.
- No automatic cloud inference fallback exists.
- Conversation data and settings are stored locally.
- No model weights, private databases, secrets, or private transcripts are accidentally committed to GitHub.

### Reliability
- Missing runtime, missing model, invalid settings, storage failure, and timeout have understandable error paths.
- Core context construction, command parsing, and storage logic have tests that do not require a live model.
- A separate local smoke test verifies integration with the chosen model.
- A 20-turn test completes without a crash or unrecoverable error.

### Usability target
- For the first candidate benchmark, target at least 5 generated tokens/second and average at least 3.5/5 across Persian naturalness, coherence, persona consistency, and uncertainty handling. These are initial project thresholds and must be measured, not assumed.
- Track cold load time, first-token latency, and peak memory even when a machine misses the target; a failure should lead to a documented model/hardware adjustment, not hidden numbers.

## Repository acceptance
- The repository remains minimal and its README links to the relevant design documents.
- Main application logic stays in `agent.py` unless a later documented maintenance, test, or security need justifies another source file.
- Large model binaries and personal runtime data remain out of version control.
- Each implementation milestone includes a focused test and a commit with a clear message.

## Long-term success

The long-term project may grow into a sophisticated companion and code agent, but size alone is not success. Each new subsystem must produce a demonstrable capability, have a defined interface, be testable, and preserve offline/privacy boundaries.

Future milestones can add durable memory, semantic retrieval, voice, safe tools, large-repository understanding, bug finding, and controlled code editing. These do not block the first conversational prototype.

## Current status

- Planning gate: covered by the Phase 1 and Stage 2–10 documents; review for contradictions before implementation.
- Prototype gate: not yet run; requires implementation and testing on the target machine.
- Stage 9 device validation: pending target hardware and real measurements.
