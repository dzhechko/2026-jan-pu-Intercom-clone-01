# PRD -- Web Chat Widget (US-008)

## User Story

As a website visitor on cloud.ru, I want to start a consultation via an embedded
chat widget, so that I can get answers without leaving the website.

## Acceptance Criteria

```gherkin
Feature: Web Chat Widget

  Scenario: Widget initialization
    Given a visitor lands on cloud.ru
    When the page loads
    Then a chat bubble appears in the bottom-right corner
    And clicking it opens the chat panel
    And the greeting message appears within 1 second

  Scenario: Proactive engagement
    Given a visitor has been on the pricing page for 60+ seconds
    When the proactive trigger fires
    Then the widget shows "Need help calculating costs for your workload?"
    And clicking it opens a pre-filled consultation

  Scenario: Send and receive messages
    Given a visitor has the chat panel open
    When they type a question and press Enter
    Then the message appears in the chat as a user bubble
    And a typing indicator is displayed
    And the assistant response renders with agent badge and sources

  Scenario: Lead capture
    Given a visitor completes 5+ messages with architecture or cost topics
    When the assistant confidence exceeds 0.7
    Then a lead capture form appears (name, company, email, phone)
    And submitting it sends contact data through the conversation

  Scenario: Human escalation from widget
    Given a visitor clicks "Contact an expert" in the footer
    When the escalation message is sent
    Then the orchestrator routes to human_escalation agent
```

## Key Files

| Layer | Path |
|-------|------|
| Widget entry | `widget/src/index.ts` |
| API client | `widget/src/api.ts` |
| Embedded styles | `widget/src/styles.ts` |
| Build config | `widget/package.json` |
| Demo page | `widget/demo.html` |
| Backend schemas | `src/api/schemas/conversation.py` |
| Backend tests | `tests/unit/test_widget.py` |

## Dependencies

- Existing REST API (`POST /api/v1/conversations`, `POST .../messages`)
- Orchestrator (intent detection, agent routing)
- RAG pipeline (retrieval for agent responses)

## Phase Tracking

- [x] Phase 1: PLAN -- PRD and feature doc created
- [x] Phase 2: VALIDATE -- requirements scored 92/100
- [x] Phase 3: IMPLEMENT -- 15 tests passing, 17KB bundle, TS clean
- [x] Phase 4: REVIEW -- lint clean, Shadow DOM isolation verified
- [ ] Phase 5: DEPLOY -- CDN distribution, CSP header guidance for customers
