# Stage 8 — Base Model Selection

## Decision

Use **Qwen3.5 4B through Ollama as the initial benchmark candidate**, not as an irrevocable choice. Use Qwen3.5 2B as the low-resource fallback and Qwen3.5 9B as a quality candidate when hardware allows.

The [Ollama model library](https://ollama.com/library/qwen3.5) currently lists 0.8B, 2B, 4B, 9B, and larger variants. The [Qwen3.5-4B model card](https://huggingface.co/Qwen/Qwen3.5-4B) lists the model under the Apache-2.0 license. Confirm the precise model/tag license and distribution terms again before redistributing model files or packaging them with a release.

## Why begin with 4B?

- It is a reasonable middle point between resource use and conversational capability.
- The package is small enough to be a plausible local baseline on a 16 GB RAM system, subject to actual benchmarking.
- It permits an apples-to-apples comparison against a smaller 2B and stronger 9B option.
- The local runtime and model choice can be separated from the persona, relationship, memory, and UI layers.

This is a hypothesis to test, not a claim that 4B is the best model for every machine or that Persian companion quality has already been validated.

## Candidate matrix

| Candidate | Role | When to choose it |
|---|---|---|
| `qwen3.5:2b` | Low-resource fallback | 4B is too slow or exceeds available memory |
| `qwen3.5:4b` | Primary starting point | Balanced first test on the recommended baseline tier |
| `qwen3.5:9b` | Higher-quality comparison | Machine has enough RAM/VRAM and 4B quality is insufficient |
| `qwen3.5:0.8b` | Bring-up/debug fallback | Verify that the complete application path works on constrained hardware |

Use explicit model tags, not an unpinned `latest` alias, in reproducible tests. Record the actual tag/digest reported by the runtime because tags and packaged weights can change.

## Inference runtime

**Initial runtime: Ollama.** Reasons:

- simple model acquisition and startup for development;
- a documented local HTTP chat interface;
- the ability to inspect loaded-model placement and resource behavior;
- keeps model execution outside the main `agent.py` while the application maintains a minimal source tree.

The app should call a localhost endpoint and use an adapter class so a future version can switch to another runtime without rewriting the conversation system.

Official references:
- [Ollama Qwen3.5 library](https://ollama.com/library/qwen3.5)
- [Ollama API overview](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Qwen3.5-4B model card](https://huggingface.co/Qwen/Qwen3.5-4B)

## Selection benchmark

Compare candidates using the same prompt set and approximately comparable generation/context settings. Score each response for:

1. Persian naturalness and comprehension;
2. conversational coherence over multiple turns;
3. stable persona adherence;
4. honesty about missing or uncertain information;
5. response latency and sustainable speed;
6. RAM/VRAM use and stability;
7. successful operation with external network access disabled.

Do not choose by model parameter count or benchmark headlines alone. A slower 9B model may not provide a better real experience on the target computer than a responsive 4B model.

## Training from scratch

Training a foundation model from zero is explicitly out of scope for Version 0. It would require a large curated dataset, substantial compute, and an evaluation pipeline. The project will first build the companion software around a pre-trained local model. Fine-tuning can be reconsidered later only if there is a specific, measured quality gap that prompt/persona/context improvements cannot solve.

## Acceptance criteria

The initial model decision is complete when 4B is recorded as the first candidate, 2B and 9B are documented alternatives, the runtime is behind an adapter, and an actual target-device benchmark is required before promoting any candidate to the default release model.
