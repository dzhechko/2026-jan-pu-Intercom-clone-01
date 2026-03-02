# Feature: AI Factory Agent (GPU)

## User Story
As an ML engineer or data scientist, I want GPU infrastructure recommendations for ML/AI workloads on Cloud.ru, so that I can select optimal configurations for training and inference.

## Complexity Score: -1 (via /plan)
- Touches ≤3 files: -2
- Agent is config, not code: -3
- No new database entities: 0
- Routing already correct (gpu_ai → ai_factory): 0
- Estimated < 30 min: -2
- **Pipeline: /plan**

## Files Created/Modified
1. `prompts/ai_factory.md` — Agent system prompt (GPU recommendations, framework guidance)

## Implementation Steps
1. Create `prompts/ai_factory.md` with GPU/ML infrastructure specialist prompt:
   - Training workloads: T4 (<1B params), A100 (1-10B), H100 (10B+)
   - Inference workloads: T4/A10 (low latency), A100 (throughput), H100 (real-time LLM)
   - Framework recommendations: PyTorch, TensorFlow, vLLM, DeepSpeed/FSDP
   - Cost estimation (on-demand vs reserved vs spot)
2. Verify routing: `gpu_ai` → `ai_factory` already correct in `select_agent_type()`
3. Verify `AGENT_TYPES` includes "ai_factory" — confirmed

## Tests
- `tests/unit/test_orchestrator.py::test_gpu_routes_to_ai_factory` — already existed and passing

## Edge Cases
- GPU intent patterns already cover: gpu, видеокарт, ml, machine learning, нейросет, inference, ai factory

## Dependencies
- Depends on: architect-agent (for infrastructure architecture context)
- `load_agent_prompt()` loads from `prompts/ai_factory.md`

## Status: DONE
Committed: `feat: migration agent + AI factory agent with dedicated routing`
