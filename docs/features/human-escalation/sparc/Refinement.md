# Refinement — Human Escalation

## Edge Cases

### EC-1: No SA Available

**Scenario**: Escalation triggers but no SA is online or assigned to the tenant.

**Behavior**:
- Queue ticket with status `pending`; retry every 60s, max 10 retries
- Outside business hours: offer callback scheduling
- After retries exhausted: notify tenant admin, keep ticket in queue
- User sees: "Все специалисты заняты. Хотите продолжить с AI пока ждёте?"

**Test**: mock `find_available_sa` returning None; assert ticket pending, retry enqueued.

### EC-2: Repeated Escalation in Same Conversation

**Scenario**: User triggers escalation, continues with AI, then escalates again.

**Behavior**:
- Do not create duplicate ticket; update existing ticket's context snapshot
- Bump priority to `high` on second escalation
- Log repeat escalation for analytics

**Test**: escalate twice on same conversation; assert 1 ticket, priority `high`.

### EC-3: User Cancels Escalation

**Scenario**: User says "отмена" or "не надо" after requesting escalation.

**Behavior**:
- Detect cancellation phrases: "отмена", "не надо", "продолжим с AI", "cancel"
- Set ticket status to `cancelled`, revert conversation status to `active`
- Resume routing to previously active agent

**Test**: escalate then send "отмена"; assert status `active`, ticket `cancelled`.

### EC-4: Escalation During LLM Outage

**Scenario**: LLM down, confidence = 0.0, should_escalate = True.

**Behavior**:
- Escalation service does not depend on LLM availability
- Use pre-defined template from `prompts/human_escalation.md`
- Priority set to `critical`

**Test**: mock LLM exception; assert should_escalate True, priority `critical`.

### EC-5: SA Does Not Respond Within SLA

**Scenario**: Ticket assigned but SA silent for 5+ minutes.

**Behavior**:
- SLA: 5 minutes during business hours
- After timeout: reassign to next SA; after 3 failures notify tenant admin

### EC-6: Concurrent Escalations Exceed Capacity

**Scenario**: Multiple conversations escalate simultaneously.

**Behavior**:
- FIFO queue per tenant; max 3 active tickets per SA (configurable)
- Queue depth > 10: alert tenant admin
- AI continues answering while queue drains

## Metrics

| Metric | Target |
|--------|--------|
| `escalation_rate` | < 15% of conversations |
| `time_to_sa_response` | < 5 min during business hours |
| `repeat_escalation_rate` | < 5% (quality signal) |
| `cancellation_rate` | Track for UX improvement |
