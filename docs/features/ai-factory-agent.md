# Feature: AI Factory Agent (GPU)

**Pipeline:** /feature (score: -1, range -1 to +4)
**Sprint:** v1.0
**Depends on:** architect-agent, orchestrator

## User Story

As an ML engineer or data scientist, I want GPU infrastructure recommendations for ML/AI workloads on Cloud.ru, so that I can select optimal configurations for training and inference.

### Acceptance Criteria (Gherkin)

```gherkin
Scenario: GPU recommendation for training
  Given an ML engineer asks "Нужны GPU для обучения модели на 7B параметров"
  When the AI Factory Agent processes the request
  Then it identifies the workload as training (medium model, 1-10B params)
  And recommends NVIDIA A100 (40/80GB VRAM), 4-8 GPUs
  And suggests PyTorch + DeepSpeed/FSDP for distributed training
  And provides cost estimate (on-demand vs reserved)
  And includes source references

Scenario: GPU recommendation for inference
  Given a CTO asks about "запуск LLM для обслуживания клиентов в реальном времени"
  When the AI Factory Agent processes the request
  Then it identifies the workload as real-time LLM inference
  And recommends NVIDIA H100 with vLLM or TensorRT-LLM
  And provides latency and throughput estimates

Scenario: Intent routing to AI Factory
  Given any user message containing GPU/ML/AI keywords
  When intent detection runs
  Then intent is classified as "gpu_ai"
  And routed to "ai_factory" agent
```

## Architecture References

### Agent Configuration (Architecture.md L150-157)
```
| Agent | Tools (MCP) | RAG Collections |
| AI Factory | gpu_catalog, ml_sizing, benchmark_lookup | ai_factory_docs, gpu_specs |
```

### RAG Collections (Architecture.md L322-336)
- `{tenant}_ai_factory` — AI/GPU documentation

## Complexity Scoring

| Signal | Score | Notes |
|--------|-------|-------|
| Touches ≤3 files | -2 | Only prompts/ai_factory.md (routing already correct) |
| System prompt > 30 lines | +1 | 53-line prompt with GPU tiers |
| Estimated < 30 min | -2 | Config-only, routing pre-existing |
| No routing change needed | +0 | gpu_ai → ai_factory was already correct |
| **Total** | **-3** | **Actually /plan boundary, but /feature for consistency** |

## Implementation Plan

### Files to Create
1. `prompts/ai_factory.md` — NEW: System prompt (53 lines)

### Tests Required
1. `test_gpu_routes_to_ai_factory` — already existed and passing
2. `test_gpu_ai_intent` — already existed and passing

### Edge Cases
- User asks about on-premise GPUs → flag as non-Cloud.ru offering
- Workload too large for Cloud.ru (10K+ GPUs) → recommend professional services
- Framework-specific questions (JAX, TensorFlow, PyTorch) → framework comparison

## Phase Tracking

- [x] Phase 1: PLAN — this document
- [x] Phase 2: VALIDATE — requirements score 95/100
- [x] Phase 3: IMPLEMENT — 2 tests passing, routing correct, prompt complete
- [x] Phase 4: REVIEW — lint clean, no security issues
