# Specification: Compliance Agent

## Compliance Categories

| Category | Regulation | Scope | Key Articles |
|----------|-----------|-------|-------------|
| Personal Data | 152-FZ | Any system processing PII of Russian citizens | Art. 18.1, 19 |
| Security Certification | FSTEC | Government and regulated workloads | Orders 17, 21, 239 |
| Critical Infrastructure | KII (187-FZ) | Banking, telecom, energy, transport, healthcare | Art. 7, 9, 10 |

## Security Levels (152-FZ)

| Level | Description | Data Volume | Data Category |
|-------|-------------|-------------|---------------|
| UZ-1 | Maximum protection | Any | Special (biometric, health, political) |
| UZ-2 | High protection | >100K subjects | General PII |
| UZ-3 | Standard protection | <100K subjects | General PII |
| UZ-4 | Basic protection | Any | Public PII only |

## FSTEC Certification Classes

| Class | Application | Cloud.ru Coverage |
|-------|-------------|-------------------|
| K1 | Government secret data | Partial (requires dedicated infra) |
| K2 | Confidential government data | Supported with configuration |
| K3 | Internal government data | Fully supported |

## Data Model

The Compliance Agent does not introduce new DB tables. It operates through the existing pipeline:

- **Intent**: `compliance_check` (detected in `src/orchestrator/intent.py`)
- **Agent type**: `compliance` (mapped in `select_agent_type()`)
- **RAG collections**: tenant-scoped regulatory document collections
- **Response metadata**: `confidence`, `sources` (regulation citations), `response_time_ms`

Stored in existing `Message` model with `agent_type="compliance"` and `metadata_` containing cited regulation articles.

## Agent Configuration (Config-as-Code)

Defined entirely in `prompts/compliance.md`:
- Behavior rules (identify regulations, cite articles, map services)
- Response format (6-step structured output)
- Constraints (no legal claims, cite 2+ sources, acknowledge limitations)
- Confidence threshold: 0.6 (inherited from `AgentDefinition` default)
