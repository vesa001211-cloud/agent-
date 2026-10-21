# Offline AI Companion — Phase 1

## 1. Project goal

Build a fully local AI companion that can communicate naturally with the user, maintain a consistent character, remember useful information across conversations, and later operate as an agent over files and code.

The project is intentionally designed to grow large. Hundreds of thousands of lines of implementation are acceptable if the architecture remains understandable, testable, and modular.

## 2. Core experience

The first-class experience is conversation, not code generation.

The companion should:

- talk naturally rather than behave like a command-only chatbot;
- have a persistent, configurable personality;
- behave consistently across conversations;
- remember selected facts and experiences when appropriate;
- retrieve relevant memories instead of dumping the entire history into every prompt;
- support long conversations without unbounded context growth;
- run locally after the required model files and dependencies are installed;
- avoid requiring a cloud API for normal operation.

## 3. Agent direction

The long-term system will also be able to work with local files and code. The agent layer is intentionally separated conceptually from the language model so the model can be replaced without rewriting personality, memory, conversation, or tools.

Planned capabilities include:

- reading and searching local files;
- understanding large repositories;
- creating and editing code;
- running tests in a controlled environment;
- inspecting tool results and deciding on follow-up actions;
- maintaining useful project context.

These capabilities are future phases, not requirements for the first runnable prototype.

## 4. Offline requirement

Normal inference and companion functionality must work without an internet connection.

Internet access may be used during setup to obtain dependencies or model weights, but the runtime architecture must not depend on a remote API.

Models, credentials, and private user memories must not be committed to GitHub.

## 5. Model strategy

The language model is the neural component responsible for language generation and reasoning. We will initially target a local instruction/chat model and keep the inference interface abstract enough to permit changing models later.

Initial candidate: Qwen3.5-class local model, with a smaller model used first if hardware requires it. Final model selection must be validated by an actual local benchmark rather than assumed from model specifications.

The application should not be coupled to a single model vendor or hosted API.

## 6. Runtime architecture

Conceptual pipeline:

User → Conversation Engine → Context Builder → Local Model → Response
                         ↘ Memory
                         ↘ Persona
                         ↘ Tools (later)

Responsibilities:

### Conversation Engine
Owns turns, sessions, conversation state, and response flow.

### Persona
Defines stable character traits, tone, behavioral rules, preferences, and configurable identity.

### Memory
Stores durable information separately from the active context. It will later support importance, retrieval, correction, deletion, and summarization.

### Context Builder
Chooses what information is relevant for the current model call. It prevents the entire lifetime conversation from being inserted into every prompt.

### Local Model Adapter
Provides one stable application interface for loading the model and generating responses. The implementation can later switch between supported local inference engines.

### Tools
A controlled interface for future file/code/system capabilities. Tools must be explicitly defined and validated rather than allowing unrestricted model-generated shell commands.

## 7. Storage strategy

The application will favor a simple local storage design.

Initial target:

- SQLite for structured persistent state and memory metadata;
- plain/local files where they are more appropriate;
- no mandatory external database server.

The exact memory schema will be designed in the memory phase rather than prematurely fixed here.

## 8. Repository philosophy

The user prefers very few files and does not want a large directory tree.

Initial implementation target:

- `agent.py` — main application and core implementation;
- `README.md` — public project documentation;
- `PHASE_01.md` — this architecture/requirements document.

Additional files should only be introduced when they solve a real maintenance, testing, packaging, or security problem.

A single Python file is acceptable even if it becomes very large. Inside that file, major subsystems must still be separated with clear sections/classes/functions.

## 9. Character design requirements

The character system must eventually support:

- name and identity;
- personality traits;
- communication style;
- humor level;
- likes/dislikes;
- conversational habits;
- behavioral boundaries;
- configurable user-facing personality settings;
- stable behavior across sessions.

The character should feel coherent without pretending that the software is a human being.

## 10. Memory requirements

Memory is a first-class subsystem, not simply an ever-growing transcript.

Planned memory layers:

1. active conversation context;
2. recent conversation history;
3. durable memories;
4. user preferences/profile information;
5. summarized older conversations.

The system must eventually allow the user to inspect, correct, and delete stored memories.

## 11. Hardware and performance

The project must be designed around real local resource constraints.

Before selecting the production model, benchmark:

- RAM usage;
- VRAM usage when applicable;
- model load time;
- tokens/second;
- first-token latency;
- context length behavior;
- CPU-only fallback behavior;
- stability during long conversations.

A smaller model that runs reliably is preferable to a larger model that cannot run comfortably.

## 12. Security principles

Future agent tools must follow least privilege.

The model must not automatically receive unrestricted operating-system access. File operations, command execution, and code execution will be explicit tools with validation, clear boundaries, and user-visible results.

Secrets, local paths containing private data, model weights, databases, and runtime logs containing sensitive information must be excluded from version control.

## 13. Version 0 success criteria

Phase 1 is considered complete when the project has an agreed architecture and measurable requirements for the first prototype.

The first prototype will eventually be considered successful if it can:

- run a local neural language model;
- maintain a multi-turn conversation;
- preserve a defined personality;
- store and retrieve selected memories locally;
- operate without a cloud API during normal use;
- recover cleanly from common runtime/model errors;
- keep the codebase understandable despite being intentionally extensible.

## 14. Phase boundaries

Phase 1 does not yet implement the full companion, long-term memory, tools, code intelligence, or autonomous behavior.

Those are implemented incrementally through the remaining phases of the 100-step roadmap.

## 15. 100-phase roadmap reference

1–10: project definition and architecture
11–20: project skeleton
21–30: local model integration
31–40: personality
41–50: memory
51–60: deeper context understanding
61–70: companion behavior
71–80: agent tools
81–90: code intelligence
91–100: optimization, security, persistence, documentation, testing, and release

## Decision log

- Offline-first: accepted.
- Python as primary implementation language: accepted.
- Neural local model rather than a hand-built language engine: accepted.
- Character/companion as the primary product experience: accepted.
- Future code-agent capabilities: accepted.
- Minimal repository structure: accepted.
- Model choice remains benchmark-dependent; Qwen3.5-class local models are the initial candidates.
