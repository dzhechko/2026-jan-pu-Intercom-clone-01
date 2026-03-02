# Specification — Migration Agent

## Migration Phases

### Phase 1: Assess
- Collect infrastructure details (VM count, OS, CPU/RAM, storage)
- Identify workload types (web apps, databases, file servers, legacy)
- Map dependencies between services
- Flag compliance requirements (152-FZ, FSTEC, CII)

### Phase 2: Plan
- Select strategy per workload: lift-and-shift, re-platform, re-architect
- Group workloads into migration waves (low-risk first)
- Define target Cloud.ru services for each workload
- Estimate timeline per wave (see `estimate_timeline()` in Pseudocode)

### Phase 3: Execute
- Provide step-by-step instructions per wave
- Reference Cloud.ru migration tools from RAG corpus
- Include rollback procedure for each step
- Track progress checkpoints

### Phase 4: Validate
- Post-migration verification checklist
- Performance baseline comparison
- Data integrity validation steps
- DNS/network cutover confirmation

## Data Model

```python
class MigrationAssessment(BaseModel):
    workloads: list[Workload]
    total_vms: int
    total_storage_tb: float
    compliance_flags: list[str]       # ["152-FZ", "FSTEC-K1"]
    complexity_score: float           # 0.0-1.0

class Workload(BaseModel):
    name: str
    type: str                         # vm | database | container | legacy
    count: int
    specs: WorkloadSpecs
    dependencies: list[str]
    recommended_strategy: str         # lift-and-shift | re-platform | re-architect
    target_service: str               # Cloud.ru service name
    estimated_weeks: float

class WorkloadSpecs(BaseModel):
    vcpu: int
    ram_gb: int
    storage_gb: int
    os: str | None = None
    database_engine: str | None = None

class MigrationPlan(BaseModel):
    waves: list[MigrationWave]
    total_timeline_weeks: float
    risk_level: str                   # low | medium | high
    rollback_strategy: str

class MigrationWave(BaseModel):
    order: int
    name: str
    workloads: list[str]
    strategy: str
    duration_weeks: float
    rollback_steps: list[str]
    dependencies: list[int]           # wave order dependencies
```

## Agent Configuration

```yaml
agent_type: migration
prompt_file: prompts/migration.md
rag_collections: ["{tenant_id}_migration_docs", "{tenant_id}_cloud_docs"]
mcp_tools: [rag_search, pricing_api, config_api]
confidence_threshold: 0.6
```
