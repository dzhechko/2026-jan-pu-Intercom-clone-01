# Command: /go

## Maturity: Alpha v1.0

## Used in: ai-consultant-cloud-ru

## Extracted: 2026-03-02

## Version: v1.0

---

## When to Use

- When starting work on a new feature and needing to determine the right development pipeline
- When triaging a backlog of features and deciding which pipeline each one requires
- When a team has multiple implementation pipelines of varying thoroughness and needs a consistent routing mechanism
- As the entry point for any feature implementation to ensure proportional process overhead

## When NOT to Use

- For bug fixes (use a dedicated fix workflow; bugs do not need complexity scoring)
- For documentation-only changes (no pipeline routing needed)
- When the project has only one implementation pipeline (routing is unnecessary)
- For tasks already assigned to a specific pipeline by a human decision-maker

## Prerequisites

- At least two implementation pipelines defined in the project (e.g., a lightweight plan-and-implement pipeline and a full lifecycle pipeline)
- A feature description or specification to score against
- Scoring signal definitions configured (or using defaults)

## Command Specification

### Purpose

Score the complexity of a proposed feature using weighted signals, then route it to the appropriate implementation pipeline. The command enforces that every feature goes through a consistent complexity assessment before work begins, preventing both over-engineering of simple features and under-engineering of complex ones.

### Invocation

```
/go [feature-name-or-description]
```

The command accepts a feature name, a description string, or a reference to a feature specification file.

### Complexity Scoring

The command evaluates the feature against N configurable signals, each producing a score from 0 to 10. The weighted sum determines the complexity tier.

#### Default Signals

| Signal | Weight | Evaluates | Score Range |
|--------|--------|-----------|-------------|
| Scope | 0.25 | Number of modules/files affected, new vs. modification | 0-10 |
| Integration | 0.20 | External dependencies, API contracts, cross-service calls | 0-10 |
| Data Model | 0.15 | Schema changes, migration complexity, data relationships | 0-10 |
| Risk | 0.20 | Security surface, data loss potential, backward compatibility | 0-10 |
| Ambiguity | 0.20 | Specification clarity, open questions, undefined edge cases | 0-10 |

Signals can be added, removed, or reweighted via configuration. Weights must sum to 1.0.

#### Scoring Process

1. Parse the feature description/specification
2. Evaluate each signal independently
3. Compute weighted sum: `complexity_score = sum(signal_score * signal_weight)`
4. Map score to tier

### Tier Routing

| Tier | Score Range | Pipeline | Description |
|------|-------------|----------|-------------|
| Lightweight | 0.0 - 3.5 | `/plan` | Simple changes: plan, implement, commit. Minimal ceremony. |
| Standard | 3.6 - 7.0 | `/feature` | Full lifecycle: plan, implement, test, review, commit. |
| Enterprise | 7.1 - 10.0 | `/feature-ent` | Extended lifecycle: ADR, plan, implement, test, review, security audit, deploy plan. |

Tier boundaries and pipeline mappings are configurable.

### Mandatory Scoring Block

The command MUST output a scoring block before executing the routed pipeline. This is non-negotiable -- it provides an audit trail of why a particular pipeline was chosen.

```markdown
## Complexity Score: [feature-name]

| Signal | Score | Rationale |
|--------|-------|-----------|
| Scope | X.X | [Brief justification] |
| Integration | X.X | [Brief justification] |
| Data Model | X.X | [Brief justification] |
| Risk | X.X | [Brief justification] |
| Ambiguity | X.X | [Brief justification] |

**Weighted Total: X.X / 10.0**
**Tier: [Lightweight | Standard | Enterprise]**
**Routed to: /[pipeline-command]**
```

This block is displayed to the developer and logged to the pipeline log before the routed pipeline begins execution.

### Override Mechanism

A developer can override the routing decision:

```
/go [feature] --force [pipeline]
```

When overridden, the scoring block is still produced, but a notice is appended:

```
OVERRIDE: Developer forced routing to /[pipeline] (scored tier was [original-tier])
```

Overrides are logged for retrospective analysis.

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `signals` | See table above | List of scoring signals with names, weights, and descriptions |
| `tiers` | See table above | Tier boundaries and pipeline mappings |
| `log_path` | `docs/pipeline_log.jsonl` | Path to the pipeline decision log |
| `require_confirmation` | `false` | Whether to prompt for confirmation before executing the routed pipeline |
| `allow_override` | `true` | Whether developers can force a different pipeline |

### Pipeline Log Entry

Each routing decision is appended to the pipeline log as a JSON line:

```json
{
  "timestamp": "2026-03-02T14:30:00Z",
  "feature": "feature-name",
  "scores": {"scope": 4.0, "integration": 6.0, "data_model": 2.0, "risk": 5.0, "ambiguity": 3.0},
  "weighted_total": 4.2,
  "tier": "standard",
  "routed_to": "/feature",
  "override": null
}
```

## Variants

| Variant | Description |
|---------|-------------|
| `/go [feature]` | Score and route to appropriate pipeline, then execute |
| `/go [feature] --score-only` | Output scoring block without executing the pipeline |
| `/go [feature] --force [pipeline]` | Override routing to a specific pipeline |
| `/go --calibrate` | Review recent pipeline log entries and suggest signal weight adjustments |
| `/go --explain [feature]` | Verbose mode: show detailed rationale for each signal score |

## Gotchas

- **Garbage in, garbage out**: The scoring quality depends entirely on the feature description quality. Vague one-liners will produce unreliable scores. Provide sufficient context for meaningful evaluation.
- **Signal weight drift**: Default weights are starting points. After 20+ features, review the pipeline log to see if routing decisions matched actual implementation complexity. Adjust weights based on retrospective data.
- **Tier boundary effects**: Features scoring near tier boundaries (e.g., 3.4 vs 3.6) may be routed to significantly different pipelines. If a feature scores within 0.5 of a boundary, consider reviewing the routing decision manually.
- **New signal integration**: When adding a new signal, all existing weights must be rebalanced to sum to 1.0. Do not simply append a new signal without reducing other weights.
- **Override abuse**: If a high percentage of features are overridden, the scoring model needs recalibration. Track override rate as a health metric.
- **Ambiguity bootstrapping**: The ambiguity signal scores high when specifications are unclear, which routes to heavier pipelines. This is intentional -- unclear requirements need more process, not less. Do not lower ambiguity scores to avoid heavier pipelines; instead, clarify the requirements.

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-03-02 | Initial extraction. Five-signal scoring, three-tier routing, mandatory scoring block. |
