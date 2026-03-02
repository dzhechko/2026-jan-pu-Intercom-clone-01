# Refinement: Compliance Agent

## Edge Cases

### 1. Mixed KII / Non-KII Workloads

**Scenario**: CTO describes infrastructure where some services fall under KII (e.g., banking core) and others do not (e.g., internal HR portal).

**Risk**: Agent applies KII-level requirements to the entire deployment, inflating cost and complexity.

**Mitigation**:
- Detect "mixed" category in `classify_requirement()` when both KII and non-KII patterns match
- Ask clarifying questions to segment workloads before advising
- Present separate requirement checklists per workload segment
- Escalate if confidence < 0.6 on workload classification

### 2. Outdated Regulations in RAG Corpus

**Scenario**: RAG corpus contains a superseded version of a FSTEC order, and the agent cites obsolete requirements.

**Risk**: CTO receives incorrect compliance guidance, leading to audit failures.

**Mitigation**:
- Include `effective_date` and `superseded_by` metadata in RAG document indexing
- System prompt instructs agent to reference "latest known regulation versions"
- Add corpus freshness checks in document indexing pipeline
- Agent must cite specific article numbers so users can cross-verify

### 3. Cross-Border Data Transfer

**Scenario**: CTO needs to process data from EU citizens stored on Cloud.ru (Moscow DC), triggering both 152-FZ and GDPR.

**Risk**: Agent only addresses 152-FZ and misses GDPR adequacy requirements.

**Mitigation**:
- Add cross-border patterns to intent detection (e.g., `gdpr`, `трансграничн`, `ЕС`)
- System prompt should flag dual-jurisdiction scenarios explicitly
- Recommend legal counsel for cross-border cases (enforced by prompt constraint)
- Escalate to human when international regulation is detected

### 4. Ambiguous Workload Classification

**Scenario**: CTO describes a workload without specifying data categories (e.g., "we store customer data"), making UZ-level determination impossible.

**Risk**: Agent guesses a security level without sufficient information.

**Mitigation**:
- Agent behavior rule: "Ask clarifying questions if the regulatory context is ambiguous"
- Require data volume (number of subjects) and data category before recommending UZ level
- Present all possible UZ levels with criteria if user declines to specify

### 5. Compliance for Services Not Yet Certified

**Scenario**: CTO asks about compliance for a new Cloud.ru service that lacks FSTEC certification.

**Risk**: Agent hallucinates certification status or fails to mention the gap.

**Mitigation**:
- RAG corpus must include service-level certification matrices
- System prompt constraint: "If unsure about a specific regulation, acknowledge the limitation"
- Gap analysis step in response format explicitly identifies uncertified services
- Confidence score drops when RAG returns no certification documents for a service

## Testing Strategy

| Edge Case | Test Type | Location |
|-----------|-----------|----------|
| Mixed KII/non-KII | Unit | `tests/unit/test_orchestrator.py` |
| Outdated regulation | Integration | `tests/integration/test_rag_pipeline.py` |
| Cross-border data | Unit | `tests/unit/test_orchestrator.py` |
| Ambiguous classification | Unit + Integration | `tests/unit/test_orchestrator.py` |
| Uncertified service | Integration | `tests/integration/test_rag_pipeline.py` |

## Metrics to Monitor

- Compliance query escalation rate (target: < 15% at v1.0)
- Regulation citation accuracy (manual audit, monthly)
- Average confidence score for compliance responses
- Time from query to advisory (target: < 30s p99)
