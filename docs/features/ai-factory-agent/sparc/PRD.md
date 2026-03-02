# PRD -- AI Factory Agent

## User Story (US-004)

```
As an ML Engineer,
I want to describe my training workload and get GPU infrastructure recommendations,
So that I can provision optimal Cloud.ru GPU resources without manual SA involvement.
```

## Acceptance Criteria

```gherkin
Feature: AI Factory GPU Consultation

  Scenario: Training workload recommendation
    Given an ML Engineer connects via Telegram or web widget
    And sends "I need to fine-tune a 7B LLM on 500GB of Russian text"
    When the AI Factory Agent processes the request
    Then it classifies the workload (framework, model size, task type)
    And recommends a GPU configuration (e.g., 4x A100 80GB with NVLink)
    And provides cost estimates (on-demand, reserved, spot)
    And suggests distributed training strategy (DeepSpeed/FSDP)
    And response time is under 30 seconds

  Scenario: Inference workload recommendation
    Given an ML Engineer asks "I need to serve a 13B model at 200 req/s"
    When the AI Factory Agent processes the request
    Then it recommends inference-optimized GPUs (H100 + vLLM/TensorRT-LLM)
    And estimates throughput and latency per configuration
    And compares serving frameworks

  Scenario: Low confidence escalation
    Given the workload involves custom ASIC or unsupported hardware
    When the AI Factory Agent confidence drops below 0.6
    Then it acknowledges limitations transparently
    And offers to connect with a human GPU infrastructure specialist
    And passes full context to the SA

  Scenario: Multi-GPU distributed training
    Given an ML Engineer needs 16+ GPUs across nodes
    When the AI Factory Agent processes the request
    Then it recommends cluster topology and interconnect (NVLink, InfiniBand)
    And warns about communication overhead and scaling efficiency
```

## Key Files

| File | Purpose |
|------|---------|
| `prompts/ai_factory.md` | Agent system prompt and behavior rules |
| `src/orchestrator/intent.py` | `gpu_ai` intent detection patterns |
| `src/orchestrator/router.py` | Routes `gpu_ai` intent to `ai_factory` agent |
| `src/agents/base.py` | Agent definition loader |
| `src/rag/search.py` | RAG search over GPU/ML documentation |
| `corpus/gpu/` | Cloud.ru GPU docs, pricing, quotas |

## Phase Tracking

| Phase | Status | Milestone |
|-------|--------|-----------|
| Intent detection (`gpu_ai`) | Done | M1 |
| Agent prompt (`prompts/ai_factory.md`) | Done | M1 |
| RAG corpus (GPU docs) | Planned | M4 |
| MCP tools (pricing_api, config_api) | Planned | M4 |
| GPU recommendation logic | Planned | M4-5 |
| Cost estimation integration | Planned | M5 |
| Integration tests | Planned | M5 |
| E2E flow (Telegram + web) | Planned | M6 |
