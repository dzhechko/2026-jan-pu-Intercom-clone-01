# Pseudocode — Human Escalation

## should_escalate()

Implemented in `src/agents/executor.py`:

```python
# In AgentExecutor.execute():
should_escalate = confidence < agent.confidence_threshold  # default 0.6
```

Triggers: confidence < threshold, keyword match (router), LLM failure (0.0).

## prepare_escalation_context()

Planned for `src/services/escalation.py`:

```python
async def prepare_escalation_context(
    conversation: Conversation, response: AgentResponse, db: AsyncSession,
) -> dict:
    """Build context snapshot for SA handoff."""
    messages = await db.execute(
        select(Message).where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
    )
    transcript = [
        {"role": m.role, "content": m.content, "agent_type": m.agent_type}
        for m in messages.scalars()
    ]
    # Determine reason
    if response.confidence == 0.0:
        reason = "system_failure"
    elif conversation.context.get("detected_intent") == "human_escalation":
        reason = "user_request"
    else:
        reason = "low_confidence"

    return {
        "conversation_id": str(conversation.id),
        "channel": conversation.channel,
        "transcript": transcript,
        "detected_intent": conversation.context.get("detected_intent"),
        "confidence": response.confidence,
        "escalation_reason": reason,
        "created_at": datetime.now(tz=ZoneInfo("Europe/Moscow")).isoformat(),
    }
```

## notify_sa()

```python
async def notify_sa(ticket: EscalationTicket, context: dict, tenant_id: str) -> bool:
    """Notify available SA. Returns True if notified, False if none available."""
    now_msk = datetime.now(tz=ZoneInfo("Europe/Moscow"))
    is_business_hours = now_msk.weekday() < 5 and time(9, 0) <= now_msk.time() <= time(18, 0)

    sa = await find_available_sa(tenant_id)
    if not sa:
        ticket.status = "pending"
        if is_business_hours:
            await enqueue_escalation(ticket.id, retry_interval=60, max_retries=10)
        return False

    ticket.assigned_sa_id = sa.id
    ticket.status = "assigned"
    summary = (
        f"Эскалация ({context['escalation_reason']})\n"
        f"Тема: {context.get('detected_intent')} | Уверенность: {context['confidence']}\n"
        f"Сообщений: {len(context.get('transcript', []))}"
    )
    if sa.telegram_id:
        await send_telegram_notification(sa.telegram_id, summary)
    if sa.email:
        await send_email_notification(sa.email, summary)
    return True
```
