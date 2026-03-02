# Specification: Orchestrator

## Data Model

### Intent (enum)

```
"migration" | "new_deployment" | "cost_optimization"
| "compliance_check" | "gpu_ai" | "general_inquiry" | "human_escalation"
```

### AgentType (enum)

```
"architect" | "cost_calculator" | "compliance"
| "migration" | "ai_factory" | "human_escalation"
```

### Intent-to-Agent Mapping

| Intent | Agent Type | Fallback |
|--------|-----------|----------|
| migration | migration | -- |
| new_deployment | architect | -- |
| cost_optimization | cost_calculator | -- |
| compliance_check | compliance | -- |
| gpu_ai | ai_factory | -- |
| human_escalation | human_escalation | -- |
| general_inquiry | architect | default |
| (unknown) | architect | default |

### AgentResponse

```python
class AgentResponse:
    content: str            # LLM-generated text
    agent_type: str         # which agent produced this
    confidence: float       # 0.0 - 1.0
    sources: list[str]      # RAG source references
    should_escalate: bool   # triggers human handoff
```

## API Contracts

### Internal: `Orchestrator.process_message()`

```
Input:
  conversation: Conversation  (SQLAlchemy model, loaded from DB)
  user_message: str

Output:
  AgentResponse

Side effects:
  - Saves user Message to DB
  - Saves assistant Message to DB (with metadata: confidence, sources, response_time_ms)
  - Updates conversation.context with detected_intent
  - Sets conversation.status = "escalated" if should_escalate is True
  - Triggers lead qualification check (non-blocking)
```

### External: `POST /api/v1/conversations/:id/messages`

```
Request:  { content: string, role: "user" }
Response: { user_message: {...}, assistant_response: { agent_type, confidence, sources } }
```

## Constraints

- Conversation history limited to last 20 messages for context window.
- RAG search defaults to `{tenant_id}_cloud_docs` if agent has no collections configured.
- RAG failures are caught and logged; processing continues without RAG context.
