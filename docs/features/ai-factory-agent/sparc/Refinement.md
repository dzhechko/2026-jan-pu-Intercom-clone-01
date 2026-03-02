# Refinement -- AI Factory Agent

## Edge Cases

### EC-01: Multi-GPU Distributed Training
**Trigger:** Model >10B params, VRAM exceeds single-node capacity (8x 80GB = 640GB).
- Warn about 15-30% communication overhead on multi-node InfiniBand setups.
- Recommend gradient accumulation and model parallelism (pipeline + tensor) for 70B+.
- Always require checkpointing every N steps for fault tolerance.

### EC-02: Spot Instance Interruption
**Trigger:** User selects spot instances for long training jobs.
- Warn: "Spot instances can be interrupted with 30s notice."
- Require checkpointing strategy for training >2 hours.
- Suggest hybrid approach: reserved base capacity + spot burst.
- Block spot for latency-sensitive or non-resumable workloads.

### EC-03: Custom/Unsupported Frameworks
**Trigger:** Niche frameworks (PaddlePaddle, MindSpore, custom CUDA kernels).
- Set confidence to 0.5 (triggers escalation).
- Still provide base GPU recommendation (hardware is framework-agnostic).
- Log unsupported framework for corpus expansion.

### EC-04: Data Pipeline Bottleneck
**Trigger:** Dataset >1TB may bottleneck GPU utilization via I/O.
- Warn about disk I/O bottleneck; recommend NVMe or high-throughput S3.
- Suggest prefetch, num_workers tuning, WebDataset format.
- Include storage cost in total estimate; recommend shared FS for multi-node.

### EC-05: Inference Autoscaling
**Trigger:** Variable-load serving (e.g., "100 req/s peak, 10 req/s off-peak").
- Recommend K8s GPU autoscaling with min/max replicas.
- Calculate cost for peak and average load; suggest T4/A10 for faster cold start.
- Warn about 2-5 min GPU node startup; recommend pre-warming min_replicas.

### EC-06: Budget Constraint Conflict
**Trigger:** Estimated cost exceeds stated budget.
- Present alternatives: (1) spot instances, (2) smaller GPU tier, (3) quantization 4/8-bit, (4) smaller model variant.
- Always show trade-off: "4x T4 instead of 1x A100 saves 60% but 3x slower."

### EC-07: Vague GPU Request
**Trigger:** "I need GPUs" without workload details.
- Ask up to 3 clarifying questions per turn (task type, framework, model size).
- If unclear after 2 rounds, escalate to human SA.

## Testing Strategy

| Edge Case | Test Type | Test File |
|-----------|-----------|-----------|
| EC-01 Multi-GPU | Unit | `tests/unit/test_ai_factory.py::test_multi_node_recommendation` |
| EC-02 Spot warning | Unit | `tests/unit/test_ai_factory.py::test_spot_checkpoint_warning` |
| EC-03 Custom framework | Integration | `tests/integration/test_ai_factory.py::test_unsupported_framework` |
| EC-04 Data pipeline | Unit | `tests/unit/test_ai_factory.py::test_storage_bottleneck_warning` |
| EC-05 Autoscaling | Unit | `tests/unit/test_ai_factory.py::test_inference_autoscale_config` |
| EC-06 Budget conflict | Unit | `tests/unit/test_ai_factory.py::test_budget_alternatives` |
| EC-07 Vague request | Integration | `tests/integration/test_ai_factory.py::test_clarifying_questions` |
