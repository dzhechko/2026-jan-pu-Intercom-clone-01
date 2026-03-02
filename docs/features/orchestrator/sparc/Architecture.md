# Architecture: Orchestrator

## Component Diagram

```
User Message
     |
     v
+-----------------+
| Intent Detection|  (intent.py)
| - Regex scoring |  - ESCALATION_PATTERNS checked first
| - Multi-intent  |  - INTENT_PATTERNS scored per category
|   resolution    |  - Highest score wins
+-----------------+
     |
     v
+-----------------+
| Agent Selection |  (intent.py :: select_agent_type)
| - Intent-to-    |  - Static mapping dict
|   agent map     |  - Unknown -> architect (default)
+-----------------+
     |
     v
+-----------------+
| Orchestrator    |  (router.py :: Orchestrator.process_message)
| Pipeline:       |
| 1. Save msg     |  -> PostgreSQL (Message table)
| 2. Detect intent|  -> intent.py
| 3. Select agent |  -> agent definition (prompts/*.md)
| 4. RAG search   |  -> Qdrant (hybrid search)
| 5. Build history|  -> last N messages from DB
| 6. Execute agent|  -> AgentExecutor -> Claude API
| 7. Save response|  -> PostgreSQL (Message + metadata)
| 8. Escalation?  |  -> set status="escalated"
| 9. Lead qualify  |  -> async check
+-----------------+
     |
     v
AgentResponse (content, confidence, sources, should_escalate)
```

## Integration Points

| Component | Direction | Protocol |
|-----------|-----------|----------|
| PostgreSQL | read/write | SQLAlchemy async (asyncpg) |
| Qdrant | read | HTTP via RAGSearch client |
| Claude API | request | HTTP via AgentExecutor |
| Agent definitions | read | File system (prompts/*.md) |
| Lead qualification | write | Internal async service call |

## Key Decisions

1. **Intent detection is rule-based, not LLM-based.** Regex keyword scoring is fast
   (sub-millisecond), deterministic, and costs zero tokens. LLM-based classification
   can be added later as an upgrade path.

2. **RAG failure is non-fatal.** If Qdrant is down, the pipeline continues with an
   empty document list. The agent still responds using its system prompt and conversation
   history, just without retrieved context.

3. **Escalation is a conversation state change.** Setting `conversation.status = "escalated"`
   is the single mechanism; downstream handlers (notification, SA assignment) react to
   this state transition.

4. **Lead qualification is fire-and-forget.** Errors in lead scoring do not block the
   user response. Failures are logged but swallowed.
