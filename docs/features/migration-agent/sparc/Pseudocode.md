# Pseudocode — Migration Agent

## assess_infrastructure()

```python
async def assess_infrastructure(
    user_message: str, history: list[dict], rag_docs: list[Document],
) -> MigrationAssessment:
    """Parse user infra details, cross-reference Cloud.ru compatibility via RAG."""
    workloads = parse_workloads(user_message, history)
    for w in workloads:
        compat = search_compatibility(w, rag_docs)
        w.target_service = compat.recommended_service
        w.recommended_strategy = select_strategy(w, compat)
    compliance_flags = detect_compliance_requirements(history)
    return MigrationAssessment(
        workloads=workloads,
        total_vms=sum(w.count for w in workloads if w.type == "vm"),
        total_storage_tb=sum(w.specs.storage_gb for w in workloads) / 1024,
        compliance_flags=compliance_flags,
        complexity_score=calculate_complexity(workloads, compliance_flags),
    )

def select_strategy(workload: Workload, compat: Compatibility) -> str:
    if workload.type == "vm" and compat.direct_support: return "lift-and-shift"
    if workload.type == "database" and compat.managed_equivalent: return "re-platform"
    if workload.type == "legacy" or not compat.direct_support: return "re-architect"
    return "lift-and-shift"
```

## generate_migration_plan()

```python
async def generate_migration_plan(assessment: MigrationAssessment) -> MigrationPlan:
    """Group workloads into waves ordered by risk (lowest first)."""
    risk_order = {"lift-and-shift": 0, "re-platform": 1, "re-architect": 2}
    sorted_wl = sorted(assessment.workloads, key=lambda w: risk_order.get(w.recommended_strategy, 2))

    # Group into waves (max 50 VMs per wave)
    waves, current, count = [], [], 0
    for w in sorted_wl:
        if count + w.count > 50 and current:
            waves.append(current)
            current, count = [], 0
        current.append(w)
        count += w.count
    if current:
        waves.append(current)

    plan_waves = [
        MigrationWave(
            order=i + 1, name=f"Wave {i + 1}: {wl[0].recommended_strategy}",
            workloads=[w.name for w in wl], strategy=wl[0].recommended_strategy,
            duration_weeks=estimate_timeline(wl),
            rollback_steps=generate_rollback(wl),
            dependencies=[i] if i > 0 else [],
        ) for i, wl in enumerate(waves)
    ]
    return MigrationPlan(
        waves=plan_waves,
        total_timeline_weeks=sum(w.duration_weeks for w in plan_waves),
        risk_level=classify_risk(assessment.complexity_score),
        rollback_strategy="per-wave with DNS failback",
    )
```

## estimate_timeline()

```python
def estimate_timeline(workloads: list[Workload]) -> float:
    """Estimate weeks per batch. Baselines: lift-and-shift ~1w/50VMs,
    re-platform ~4w/service, re-architect ~12w/app. +20% per dependency."""
    BASE = {"lift-and-shift": 1.0, "re-platform": 4.0, "re-architect": 12.0}
    total = 0.0
    for w in workloads:
        base = BASE.get(w.recommended_strategy, 4.0)
        units = max(1, w.count / 50) if w.recommended_strategy == "lift-and-shift" else 1
        total += base * units * (1.0 + 0.2 * len(w.dependencies))
    return round(total, 1)
```
