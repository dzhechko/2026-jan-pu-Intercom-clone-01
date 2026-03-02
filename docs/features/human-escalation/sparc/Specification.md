# Specification — Human Escalation

## Escalation Triggers

### 1. Confidence-Based (Automatic)

The `AgentExecutor._estimate_confidence()` method computes a score from RAG
relevance and source references. When `confidence < agent.confidence_threshold`
(default 0.6), `AgentResponse.should_escalate` is set to `True`.

Confidence formula:
```
confidence = min(1.0, avg_rag_score * 0.8 + reference_bonus + 0.2)
```
- No RAG documents: confidence = 0.4 (always escalates)
- LLM failure after retry: confidence = 0.0 (always escalates)

### 2. Explicit User Request (Keyword)

`ESCALATION_PATTERNS` in `src/orchestrator/intent.py` matches phrases in
Russian and English: "человек", "оператор", "специалист", "живой",
"менеджер", "connect human", "speak person", "talk someone".

When matched, `detect_intent()` returns `"human_escalation"` and the
orchestrator routes directly to the human escalation agent.

### 3. System Failure

When the LLM call raises an unrecoverable exception, the executor returns
`confidence=0.0, should_escalate=True` with a service-unavailable message.

## Data Model

### Conversation (existing)

| Field | Type | Escalation Behavior |
|-------|------|---------------------|
| `status` | `String(20)` | Set to `"escalated"` on trigger |
| `context` | `JSONB` | Stores `detected_intent`, escalation metadata |

### Message (existing)

| Field | Type | Escalation Behavior |
|-------|------|---------------------|
| `agent_type` | `String` | Set to `"human_escalation"` |
| `metadata_` | `JSONB` | Contains `confidence`, `sources`, `response_time_ms` |

### EscalationTicket (planned)

| Field | Type | Description |
|-------|------|-------------|
| `id` | `UUID` | Primary key |
| `conversation_id` | `FK → conversations.id` | Source conversation |
| `tenant_id` | `FK → tenants.id` | Tenant isolation |
| `reason` | `String(50)` | `low_confidence`, `user_request`, `system_failure` |
| `priority` | `String(10)` | `normal`, `high`, `critical` |
| `assigned_sa_id` | `UUID | None` | Assigned Solution Architect |
| `status` | `String(20)` | `pending`, `assigned`, `resolved`, `expired` |
| `context_snapshot` | `JSONB` | Transcript, intent, architecture, TCO data |
| `created_at` | `datetime` | Ticket creation time |
| `resolved_at` | `datetime | None` | Resolution time |

## Business Hours

Monday-Friday, 09:00-18:00 MSK. Outside this window, callback scheduling
replaces live handoff. Business hours are configurable per tenant.

## Response Templates

Defined in `prompts/human_escalation.md`:
- **Business hours**: "Подключаю специалиста..." (ETA 30 seconds)
- **Outside hours**: "Могу запланировать обратный звонок..."
- **SAs busy**: "Ожидаемое время ожидания — около 5 минут..."
