# PRD — Human Escalation

## User Story (US-014)

As an Enterprise CTO,
I want to be transferred to a human expert when the AI cannot help,
so that I always get the answer I need regardless of complexity.

## Escalation Triggers

1. **Auto-handoff**: Agent confidence score drops below 0.6
2. **Explicit request**: User asks for a human (keyword match)
3. **System failure**: LLM call fails after retry (confidence = 0.0)

## Acceptance Criteria (Gherkin)

```gherkin
Feature: Human Escalation

  Scenario: Low confidence auto-escalation
    Given the AI agent's confidence score is below 0.6
    When the orchestrator evaluates should_escalate
    Then conversation.status is set to "escalated"
    And an escalation ticket is created with full transcript
    And the SA is notified via Telegram/email

  Scenario: User-requested escalation
    Given a user sends "хочу поговорить с человеком"
    When intent detection matches ESCALATION_PATTERNS
    Then the human_escalation agent is selected
    And the handoff message is sent within 30 seconds (business hours)
    And outside business hours a callback is scheduled

  Scenario: SA context preservation
    Given an escalation is triggered
    When the SA receives the ticket
    Then they see: transcript, detected intent, architecture, TCO data
    And can continue in the same Telegram thread

  Scenario: All SAs busy
    Given no SA is available within 60 seconds
    When the timeout expires
    Then the user is offered to continue with AI while waiting
    And the escalation remains in the queue
```

## Files

| File | Role |
|------|------|
| `prompts/human_escalation.md` | Agent system prompt (RU/EN templates) |
| `src/orchestrator/intent.py` | ESCALATION_PATTERNS + detect_intent() |
| `src/orchestrator/router.py` | Orchestrator.process_message() escalation handling |
| `src/agents/executor.py` | AgentResponse.should_escalate, confidence estimation |
| `src/agents/base.py` | AgentDefinition.confidence_threshold = 0.6 |
| `src/models/conversation.py` | Conversation.status = "escalated" |

## Phase Tracking

- [x] Phase 1: PLAN — SPARC docs created, 2 files (prompt, routing)
- [x] Phase 2: VALIDATE — code matches SPARC docs
- [x] Phase 3: IMPLEMENT — 138 tests passing, lint clean
- [x] Phase 4: REVIEW — 22 ruff issues fixed, all clean
