# Stage 5 — Offline Requirements and Boundaries

## Definition of offline

After installation and model acquisition, the companion's normal conversational runtime must function with external network access disabled. The app must not require a remote inference service, remote database, cloud memory, login, or hosted API.

Initial installation can require internet access to download the application runtime, Python dependencies if any, and model files. This setup-time requirement is distinct from runtime operation.

## Required runtime behavior

- Use a local model runtime and a loopback-only endpoint by default (for Ollama, normally `http://127.0.0.1:11434`).
- The app must not silently switch to a hosted model if the local model is unavailable.
- An unavailable local model must produce a clear local error and next-step guidance.
- Prompts, responses, character settings, and memories must remain on the user's device under normal operation.
- No analytics, telemetry, crash upload, cloud sync, or external content fetch is to be added by the companion without explicit, informed opt-in.
- Logs must not contain secrets and should avoid unnecessary copies of private conversation text.
- Model weights and personal data must remain outside the repository by default.

## Network policy

The application should call only the configured local inference endpoint. Bindings must be explicitly configurable only for advanced users; a remote host must never be accepted as the default.

For high-assurance offline checks, close external network access or use a firewall while leaving the local inference process available. A loopback API is local communication, not a cloud API, but the test must confirm no unexpected external connections are made by the complete runtime stack.

Ollama may be installed as a separate local service. Downloading a model is a setup action; using an already downloaded local model is the runtime action. The two must be tested separately.

## What offline does not automatically guarantee

- It does not mean a model is small or fast.
- It does not mean a local model is factually correct.
- It does not protect data if the computer is compromised or backups are exposed.
- It does not prevent all network activity by unrelated software on the computer.
- It does not mean every optional tool or future feature can work without external services. Any feature that needs the internet must be labeled optional and disabled in offline mode.

## Offline acceptance test

1. Download and verify the selected model while connected.
2. Start the local runtime and run one test conversation.
3. Disable external connectivity (keep localhost/loopback available).
4. Restart the application and run a multi-turn conversation.
5. Confirm responses are generated and saved locally.
6. Confirm the app shows an error rather than using a remote fallback if the local service is stopped.
7. Observe connections or apply firewall rules to confirm the app is not sending prompt content off-device.
8. Restore networking only after the test is complete.

## Data and repository exclusions

At minimum, repository hygiene must exclude:

- model weights and runtime caches;
- local database files (SQLite and backups);
- private logs and conversation exports;
- API keys, tokens, and personal configuration;
- temporary benchmarks containing private prompts.

The repository will include source code and documentation only, plus non-sensitive automated tests.

## Acceptance criteria

This stage is specified when the team can distinguish setup-time internet use from runtime behavior, list all permitted network paths, and run the offline acceptance test above. The actual test result must be recorded only after execution on the target device.
