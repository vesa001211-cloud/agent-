# Stage 7 — Hardware Requirements and Performance Targets

## Purpose

Define practical starting tiers for running a quantized local language model. These are planning estimates, not guaranteed vendor minimums. Actual memory use depends on model quantization, context length, runtime, operating system, and whether layers run on CPU or GPU.

## Model file sizes currently listed by Ollama

The current Qwen3.5 tags listing shows approximate download sizes of:

- `qwen3.5:2b`: about 2.7–3.1 GB;
- `qwen3.5:4b`: about 3.3–4.0 GB;
- `qwen3.5:9b`: about 6.6–7.6 GB.

These are model-package sizes, not total RAM/VRAM requirements. See the [Ollama Qwen3.5 tags](https://ollama.com/library/qwen3.5/tags).

## Planning tiers

### Tier A — constrained / exploratory

- 8 GB system RAM;
- modern 64-bit CPU;
- 8 GB or more free disk space;
- no dedicated GPU required for a small CPU-only test;
- start with `qwen3.5:0.8b` or `qwen3.5:2b`.

This tier is for feasibility tests. Speed and response quality may be limited, especially with larger contexts and other applications open.

### Tier B — recommended baseline

- 16 GB system RAM;
- modern 64-bit CPU, preferably 6 or more reasonable-performance cores;
- 10–15 GB free disk space for the model, runtime, logs, and working room;
- optional discrete GPU; 6–8 GB VRAM may help with small/medium quantized models, but does not guarantee full GPU residency;
- benchmark `qwen3.5:4b` as the primary candidate and `qwen3.5:2b` as fallback.

This is the planning target for Version 0, not a claim that the app has already been tested on such a machine.

### Tier C — comfortable experimentation

- 32 GB system RAM;
- modern multi-core CPU;
- 20 GB or more free disk space;
- GPU with roughly 10–16 GB VRAM is useful for testing the 9B class, subject to quantization, context, and backend support;
- compare `qwen3.5:9b` against the 4B baseline.

CPU offload can allow a model to run when VRAM is insufficient, but usually affects speed. Larger context settings increase memory needs; do not set maximum advertised context by default.

## Operating system and runtime

Initial target platforms are 64-bit Windows, Linux, and macOS environments supported by the selected Ollama release. Runtime and GPU support must be verified for the exact OS/GPU combination. Python 3.11+ is the proposed application baseline; the selected environment will be tested before finalizing the minimum version.

## Required measurements

For each candidate model, capture:

- operating system and version;
- CPU model and core count;
- total system RAM;
- GPU model and dedicated VRAM, if present;
- free disk space;
- model tag and quantization/package variant;
- model load time;
- time to first token;
- steady-state generation speed (tokens/second);
- peak RAM and VRAM;
- behavior after at least 20 conversational turns;
- behavior while external networking is disabled.

Use `ollama ps` to inspect how the runtime placed the model (CPU/GPU split) and inspect system resource monitors during the test.

## Context-memory rule

Ollama's documented context defaults vary with available VRAM, and a larger context consumes additional memory. The model's advertised maximum must not be assumed to be a sensible default for this app. See the [Ollama context-length documentation](https://github.com/ollama/ollama/blob/main/docs/context-length.mdx).

Start with a conservative context window (for example, 8K tokens for initial benchmarking) and increase it only after checking memory and latency.

## Acceptance criteria

This stage is specified when target tiers, required disk space, fallback models, and benchmark metrics are clear. The user's actual hardware is not confirmed by these estimates and must be recorded during Stage 9.
