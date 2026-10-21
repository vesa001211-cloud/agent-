# Stage 9 — Local Model Feasibility Test

## Status

**Test protocol defined; target-device execution is pending.** No claim is made that a model has been successfully run on the user's computer. That conclusion requires the computer's actual specifications and a test run on that device.

## Purpose

Verify that the selected local model can be installed, loaded, used for Persian and multi-turn conversation, and run without external networking on the intended machine.

## Record the target machine

Before testing, record:

- OS and version;
- CPU and core count;
- installed RAM;
- GPU and dedicated VRAM, if any;
- free disk space;
- Python version;
- Ollama version;
- whether the system is a laptop or desktop and whether other demanding applications are running.

Useful commands include:

```text
python --version
ollama --version
ollama list
ollama ps
```

For Windows, collect the CPU/RAM/GPU details from Task Manager or System Information; for Linux/macOS use the available system-information tools. Do not post serial numbers, account identifiers, or unrelated private details.

## Test sequence

### A. Runtime readiness

1. Install a supported Ollama release.
2. Pull the chosen candidate while online, for example `ollama pull qwen3.5:4b`.
3. Confirm that the model appears in `ollama list`.
4. Run `ollama run qwen3.5:4b` and ask for a short greeting in Persian.
5. Confirm that a model response is generated without a remote provider.

If the primary candidate fails because of memory or speed, repeat with `qwen3.5:2b`. Test 9B only when hardware has suitable headroom.

### B. Conversation quality smoke test

Use the same fixed tests for every candidate:

1. Persian greeting and natural reply.
2. Ask the model to explain that it is an AI, not a human.
3. Establish a simple persona instruction and check it after several turns.
4. Discuss a topic, briefly change topics, then refer back to the first one.
5. Ask a question where the correct answer is not known from the prompt and check whether it admits uncertainty.
6. Continue for at least 20 turns and watch for repetition, contradictions, or runtime errors.
7. Restart the chat application and check only the persistence features that have actually been implemented.
8. Repeat the core conversation test with external networking disabled after the model has been downloaded.

Do not grade quality based on one cherry-picked answer. Save a small fixed test set and score each response in the same way across models.

## Metrics and provisional pass thresholds

Capture actual measured values; leave a metric as “not measured” if the tool cannot provide it.

- **Runtime stability:** no crash or unrecoverable error during the fixed smoke test.
- **Offline behavior:** the model responds after external connectivity is disabled, with loopback/local inference still available.
- **Privacy behavior:** no request-content transmission to remote inference endpoints by the app.
- **Latency:** record cold model load, time to first token, and steady generation speed. Aim for at least 5 tokens/second for a minimally comfortable text-chat experience; treat this as a project target, not a hardware guarantee.
- **Quality:** rate Persian naturalness, coherence, persona consistency, and uncertainty handling from 1 to 5. An initial candidate should average at least 3.5/5 across the fixed set, with no category below 3/5. Adjust these thresholds only by documenting the reason.
- **Resource use:** record peak RAM/VRAM and confirm the machine remains responsive during the test.

## Failure paths

- **Not enough memory:** reduce context, use 2B/0.8B, close other applications, or use a supported GPU/CPU configuration.
- **Too slow:** compare a smaller model, reduce context, or check model offload using `ollama ps`.
- **Poor Persian quality:** compare 9B where feasible and re-evaluate prompting before changing the whole architecture.
- **No offline response:** check whether the model is fully downloaded and whether the app attempted to contact a remote service.
- **Runtime missing or stopped:** the application should explain the issue and must not silently fall back to cloud inference.

## Required result record

After device testing, add a short table to this file with:

| Item | Result |
|---|---|
| Test date and OS | Pending |
| CPU / RAM / GPU / VRAM | Pending |
| Runtime and exact model tag | Pending |
| Cold load / first token / tokens per second | Pending |
| Peak RAM / VRAM | Pending |
| Quality scores | Pending |
| Offline test | Pending |
| Decision | Pending |

Do not replace “Pending” values with estimates. Stage 9 is considered empirically complete only after the target-device results are filled in and reviewed.
