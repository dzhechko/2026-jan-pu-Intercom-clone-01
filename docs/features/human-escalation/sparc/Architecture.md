# Architecture — Human Escalation

## Component Diagram

```
User Message
     │
     ▼
┌──────────────────┐
│  Intent Detector  │── ESCALATION_PATTERNS match ──┐
│  (intent.py)      │                                │
└────────┬─────────┘                                 │
         │ other intent                              │
         ▼                                           │
┌──────────────────┐                                 │
│  Agent Executor   │── confidence < 0.6 ───────┐    │
│  (executor.py)    │                            │    │
└──────────────────┘                             ▼    ▼
                                   ┌─────────────────────┐
                                   │  Orchestrator        │
                                   │  status="escalated"  │
                                   └──────────┬──────────┘
                                              │
                                   ┌──────────▼──────────┐
                                   │ Escalation Service   │
                                   │ ticket → assign → SA │
                                   └──────────┬──────────┘
                                         ┌────┴────┐
                                         ▼         ▼
                                    Telegram    Email
```

## Flow: Low Confidence Escalation

1. User sends message; `AgentExecutor` calls LLM, runs `_estimate_confidence()`
2. If `confidence < 0.6`, sets `should_escalate = True` on `AgentResponse`
3. Orchestrator sets `conversation.status = "escalated"`, logs event
4. Escalation Service creates `EscalationTicket` with context snapshot
5. Checks business hours (Mon-Fri 09:00-18:00 MSK)
6. **During hours**: notifies SA via Telegram/email
7. **Outside hours**: schedules callback, informs user

## Flow: Explicit User Request

1. `detect_intent()` matches ESCALATION_PATTERNS, returns `"human_escalation"`
2. `select_agent_type()` routes to escalation agent prompt
3. Agent generates response template, then same service flow (steps 4-7 above)

## Context Handoff Payload

```json
{
  "conversation_id": "uuid",
  "channel": "telegram",
  "transcript": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}],
  "detected_intent": "migration",
  "confidence": 0.42,
  "recommendations": {"architect": "..."},
  "escalation_reason": "low_confidence",
  "created_at": "2026-03-02T14:30:00+03:00"
}
```

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Threshold 0.6 per-agent configurable | Different agents need different thresholds |
| Context snapshot as denormalized JSONB | SA gets self-contained ticket |
| Dual notification (Telegram + email) | SA may not monitor both channels |
| Conversation stays in same thread | User does not switch channels |
| Escalation is non-blocking | User gets AI response while escalating |
