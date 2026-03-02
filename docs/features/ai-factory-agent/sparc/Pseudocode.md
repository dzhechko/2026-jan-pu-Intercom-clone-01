# Pseudocode -- AI Factory Agent

## classify_ml_workload()

```python
def classify_ml_workload(message: str, context: dict | None = None) -> MLWorkload:
    """Extract ML workload parameters from user message."""
    workload = MLWorkload()
    # Detect task type from keywords (RU + EN)
    if matches(message, [r"train", r"fine.?tun", r"обуч", r"дообуч"]):
        workload.task_type = "training"
    elif matches(message, [r"inference", r"serv", r"deploy", r"инференс"]):
        workload.task_type = "inference"
    else:
        workload.task_type = "unknown"  # agent asks clarifying question
    # Extract: model params (e.g. "7B"), framework, dataset size, RPS/latency
    workload.model_params_billions = normalize_param_count(extract_param_count(message))
    workload.framework = detect_framework(message)  # pytorch, tensorflow, jax, etc.
    workload.dataset_size_gb = normalize_to_gb(extract_data_size(message))
    if workload.task_type == "inference":
        workload.target_rps = extract_number(message, [r"(\d+)\s*req"])
        workload.max_latency_ms = extract_number(message, [r"(\d+)\s*ms"])
    return workload
```

## recommend_gpu_config()

```python
def recommend_gpu_config(workload: MLWorkload) -> GPURecommendation:
    """Recommend GPU type and count based on VRAM estimation."""
    if workload.task_type == "training":
        vram_gb = workload.model_params_billions * 18  # mixed-precision rule
        if vram_gb <= 16:
            config = GPUConfig(gpu="T4", count=1)
        elif vram_gb <= 80:
            config = GPUConfig(gpu="A100-80GB", count=1)
        elif vram_gb <= 320:
            config = GPUConfig(gpu="A100-80GB", count=ceil(vram_gb / 80), interconnect="NVLink")
        elif vram_gb <= 640:
            config = GPUConfig(gpu="H100", count=ceil(vram_gb / 80), interconnect="NVLink+InfiniBand")
        else:
            config = GPUConfig(gpu="H100", count=64, interconnect="InfiniBand NDR")
            config.requires_multi_node = True
        if config.count > 1:
            config.strategy = "FSDP" if workload.framework == "pytorch" else "DeepSpeed ZeRO-3"

    elif workload.task_type == "inference":
        if workload.model_params_billions <= 3:
            config = GPUConfig(gpu="T4", count=1)
        elif workload.model_params_billions <= 13:
            config = GPUConfig(gpu="A100-80GB", count=1)
        else:
            config = GPUConfig(gpu="H100", count=ceil(workload.model_params_billions / 40))
        config.serving_framework = "vLLM" if workload.model_params_billions > 7 else "TensorRT-LLM"
    return GPURecommendation(config=config, workload=workload)
```

## estimate_training_cost()

```python
def estimate_training_cost(config: GPUConfig, hours: float, pricing: dict) -> CostEstimate:
    """Calculate cost across billing tiers (on-demand, reserved, spot)."""
    base = pricing[config.gpu].hourly_rate * config.count
    estimate = CostEstimate(
        on_demand=CostTier(hourly=base, total=base * hours),
        reserved_1mo=CostTier(hourly=base * 0.80, total=base * 0.80 * hours),
        reserved_3mo=CostTier(hourly=base * 0.70, total=base * 0.70 * hours),
        spot=CostTier(hourly=base * 0.40, total=base * 0.40 * hours,
                      warning="Spot instances may be interrupted; use checkpointing"),
    )
    if config.dataset_size_gb:
        estimate.storage_cost = config.dataset_size_gb * STORAGE_PRICE_PER_GB
    # Recommend tier based on duration
    if hours > 720: estimate.recommended_tier = "reserved_3mo"
    elif hours > 168: estimate.recommended_tier = "reserved_1mo"
    else: estimate.recommended_tier = "spot" if config.count <= 4 else "on_demand"
    return estimate
```
