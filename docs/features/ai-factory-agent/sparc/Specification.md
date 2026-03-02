# Specification -- AI Factory Agent

## GPU Instance Types

| GPU | VRAM | Use Case | Cloud.ru SKU |
|-----|------|----------|--------------|
| NVIDIA T4 | 16 GB | Inference, small training | `gpu.t4.1`, `gpu.t4.4` |
| NVIDIA A10 | 24 GB | Inference, medium workloads | `gpu.a10.1`, `gpu.a10.2` |
| NVIDIA A100 40GB | 40 GB | Training up to 10B params | `gpu.a100-40.4`, `gpu.a100-40.8` |
| NVIDIA A100 80GB | 80 GB | Training 10B+ params | `gpu.a100-80.4`, `gpu.a100-80.8` |
| NVIDIA H100 | 80 GB | LLM training/inference, largest models | `gpu.h100.8` |

## Cluster Configurations

| Config | GPUs | Interconnect | Target Workload |
|--------|------|--------------|-----------------|
| Single GPU | 1x T4/A10 | N/A | Inference, prototyping |
| Multi-GPU node | 4x A100 | NVLink | Training models 1-10B |
| Multi-GPU node | 8x A100/H100 | NVLink + NVSwitch | Training models 10-70B |
| Multi-node cluster | 16-64x H100 | InfiniBand HDR/NDR | Training models 70B+ |

## Framework Support Matrix

| Framework | Training | Inference | Distributed | Managed |
|-----------|:--------:|:---------:|:-----------:|:-------:|
| PyTorch 2.x | Yes | Yes | FSDP, DDP | Yes |
| TensorFlow 2.x | Yes | Yes | MirroredStrategy | Yes |
| DeepSpeed (ZeRO 1-3) | Yes | -- | Yes | Yes |
| vLLM | -- | Yes | Tensor parallel | Yes |
| TensorRT-LLM | -- | Yes | Pipeline parallel | Yes |
| Hugging Face Transformers | Yes | Yes | via DeepSpeed/FSDP | Yes |

## Pricing Model

| Billing Type | Description | Discount |
|--------------|-------------|----------|
| On-demand | Pay per hour, no commitment | 0% |
| Reserved 1 month | Guaranteed capacity, monthly | 15-20% |
| Reserved 3 months | Guaranteed capacity, quarterly | 25-35% |
| Reserved 12 months | Annual commitment | 40-50% |
| Spot/Preemptible | Interruptible, best-effort | 50-70% |

## Agent Routing

Intent detection keywords (from `src/orchestrator/intent.py`):

```
gpu_ai: [gpu, видеокарт, ml, machine.?learning, нейросет,
         обуч.*модел, inference, ai.?factory, искусственн.*интеллект]
```

Maps to: `ai_factory` agent via `select_agent_type("gpu_ai")`.

## RAG Collections

- `{tenant_id}_gpu_docs` -- GPU instance specifications, quotas, limits
- `{tenant_id}_ml_pricing` -- Current GPU pricing tables
- `{tenant_id}_cloud_docs` -- General Cloud.ru documentation (fallback)

## MCP Tools

| Tool | Endpoint | Purpose |
|------|----------|---------|
| `pricing_api` | `/mcp/pricing/gpu` | Real-time GPU instance pricing |
| `config_api` | `/mcp/config/gpu-quota` | Check GPU availability and quotas |
| `rag_search` | Internal | Search GPU and ML documentation |
