# PRD — Telegram Bot

## User Story (US-006)

As an Enterprise CTO, I want to consult with the AI via Telegram, so that I can get answers on my preferred communication platform.

## Gherkin Acceptance Criteria

```gherkin
Feature: Telegram Bot

  Scenario: Start consultation
    Given a user opens the Telegram bot
    When they send /start
    Then the bot greets them with available capabilities
    And asks what they need help with
    And supports Russian language by default

  Scenario: Rich message formatting
    Given the AI generates a TCO comparison table
    When sending to Telegram
    Then tables are formatted with monospace or as images
    And long responses are split into readable chunks (4096 char limit)
    And inline buttons offer "Get PDF" or "Continue"

  Scenario: Session continuity
    Given a user had a consultation yesterday
    When they return today and ask "What about the migration plan?"
    Then the bot restores previous conversation context
    And continues from where they left off

  Scenario: Webhook secret validation
    Given the webhook secret is configured
    When a request arrives without a valid X-Telegram-Bot-Api-Secret-Token
    Then the server responds with 401 Unauthorized

  Scenario: Empty or missing message
    Given a webhook update arrives with no text or no chat ID
    When the handler parses the update
    Then it returns an empty 200 response without processing
```

## Files

| File | Purpose |
|------|---------|
| `src/api/webhooks/telegram.py` | Webhook handler, message routing, Telegram API calls |
| `src/orchestrator/router.py` | Routes parsed messages to the appropriate agent |
| `src/models/conversation.py` | Conversation model (channel, channel_user_id, status) |
| `src/models/tenant.py` | Tenant lookup for multi-tenant isolation |
| `src/core/config.py` | `telegram_bot_token`, `telegram_webhook_secret` settings |
| `tests/integration/test_api.py` | Webhook integration tests |

## Phase Tracking

- [x] Phase 1: PLAN -- SPARC docs created, 1 file (telegram webhook)
- [x] Phase 2: VALIDATE — code matches SPARC docs
- [x] Phase 3: IMPLEMENT — 138 tests passing, lint clean
- [x] Phase 4: REVIEW — 22 ruff issues fixed, all clean
