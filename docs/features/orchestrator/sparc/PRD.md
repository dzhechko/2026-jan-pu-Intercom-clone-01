# PRD: Orchestrator

## Feature Description

The orchestrator is the central routing layer of the AI consultation platform. It receives
user messages, detects intent via keyword pattern matching (Russian + English), selects the
appropriate specialized agent, coordinates RAG retrieval, executes the agent via LLM, and
handles escalation when confidence is low or the user explicitly requests a human.

## User Stories

- **US-001** (Architecture): CTO describes infrastructure, orchestrator routes to Architect agent.
- **US-002** (TCO): CTO asks about costs, orchestrator routes to Cost Calculator agent.
- **US-003** (Compliance): CTO asks about 152-FZ, orchestrator routes to Compliance agent.
- **US-014** (Escalation): Confidence < 0.6 or explicit request triggers human handoff.

## Acceptance Criteria

```gherkin
Feature: Orchestrator Intent Routing

  Scenario: Route migration query to migration agent
    Given a user sends "Migrate 200 VMware servers to cloud"
    When the orchestrator detects intent
    Then intent is "migration" and agent_type is "migration"

  Scenario: Route cost query to cost calculator
    Given a user sends "Compare TCO for 50 VMs"
    When the orchestrator detects intent
    Then intent is "cost_optimization" and agent_type is "cost_calculator"

  Scenario: Escalate on explicit human request
    Given a user sends "I want to talk to a human"
    When the orchestrator detects intent
    Then intent is "human_escalation" and conversation.status becomes "escalated"

  Scenario: Empty message defaults to general inquiry
    Given a user sends ""
    When the orchestrator detects intent
    Then intent is "general_inquiry" and agent_type is "architect"
```

## Files

| File | Purpose |
|------|---------|
| `src/orchestrator/intent.py` | Intent detection via regex keyword scoring |
| `src/orchestrator/router.py` | Orchestrator class: message processing pipeline |
| `tests/unit/test_orchestrator.py` | 16 unit tests (intent + agent selection) |

## Phase Tracking

- [x] Phase 1: PLAN -- SPARC docs created, 2 files (intent, router)
- [x] Phase 2: VALIDATE — code matches SPARC docs
- [x] Phase 3: IMPLEMENT — 138 tests passing, lint clean
- [x] Phase 4: REVIEW — 22 ruff issues fixed, all clean
