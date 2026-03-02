# PRD: API Endpoints

## User Story

As an admin or integration client, I need a REST API to create conversations,
send messages (routed through the AI orchestrator), view dashboard metrics and
ROI analytics, and authenticate via JWT -- so that Telegram bots, web widgets,
CRM integrations, and the admin dashboard can all interact with the platform
through a single, tenant-isolated API layer.

## Scope

- **Conversations API** -- CRUD for conversations and messages (multi-tenant, API-key auth)
- **Dashboard API** -- aggregated metrics, ROI analytics (JWT auth)
- **Auth API** -- admin login, JWT token issuance
- **Telegram Webhook** -- inbound updates from Telegram Bot API (secret-token auth)

## Gherkin Acceptance Criteria

```gherkin
Feature: Conversations API

  Scenario: Create a conversation
    Given a valid X-API-Key header for tenant "acme"
    When I POST /api/v1/conversations with channel "telegram"
    Then I receive 201 with conversation id and status "active"

  Scenario: Send a message and receive AI response
    Given an active conversation exists
    When I POST /api/v1/conversations/{id}/messages with content "Hello"
    Then I receive user_message, assistant_response with agent_type, confidence, sources

  Scenario: Reject unauthenticated requests
    When I POST /api/v1/conversations without X-API-Key
    Then I receive 401 Unauthorized

Feature: Dashboard API

  Scenario: Retrieve metrics for a period
    Given a valid JWT token with admin role
    When I GET /api/v1/dashboard/metrics?period=7d
    Then I receive total_consultations, leads_generated, daily_trend

Feature: Auth API

  Scenario: Successful login
    When I POST /api/v1/auth/login with valid credentials
    Then I receive access_token with expires_in
```

## Files

| File | Purpose |
|------|---------|
| `src/api/routes/conversations.py` | Conversation + message endpoints |
| `src/api/routes/dashboard.py` | Metrics and ROI endpoints |
| `src/api/routes/auth.py` | Login endpoint |
| `src/api/schemas/conversation.py` | Conversation Pydantic schemas |
| `src/api/schemas/dashboard.py` | Dashboard Pydantic schemas |
| `src/api/schemas/auth.py` | Auth Pydantic schemas |
| `src/core/security.py` | JWT creation/decode, API key validation |
| `tests/integration/test_api.py` | Integration tests for all endpoints |

## Phase Tracking

- [x] Phase 1: PLAN -- SPARC docs created, 5+ files (routes, schemas, auth)
- [x] Phase 2: VALIDATE — code matches SPARC docs
- [x] Phase 3: IMPLEMENT — 138 tests passing, lint clean
- [x] Phase 4: REVIEW — 22 ruff issues fixed, all clean
