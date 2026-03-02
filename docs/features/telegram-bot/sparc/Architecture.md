# Architecture -- Telegram Bot

## System Context

```
Telegram User
    |
    | HTTPS (TLS 1.3)
    v
Telegram API Servers
    |
    | POST /api/v1/webhooks/telegram
    v
Nginx (reverse proxy, TLS termination, rate limiting)
    |
    v
FastAPI (telegram_webhook handler)
    |
    +---> Secret Validation (X-Telegram-Bot-Api-Secret-Token)
    |
    +---> Parse Update (extract chat_id, user_id, text)
    |
    +---> /start command? --> _send_telegram_message(greeting) --> return
    |
    +---> Tenant Lookup (PostgreSQL via SQLAlchemy)
    |
    +---> Conversation Find-or-Create (PostgreSQL)
    |
    +---> Orchestrator.process_message(conversation, text)
    |         |
    |         +---> Intent Detection
    |         +---> Agent Routing (Architect, Cost, Compliance, ...)
    |         +---> RAG Retrieval (Qdrant + BM25)
    |         +---> LLM Call (Claude / GigaChat fallback)
    |         +---> Confidence Scoring (<0.6 triggers escalation)
    |
    +---> _send_telegram_message(response)
              |
              | POST /bot{TOKEN}/sendMessage
              v
         Telegram API Servers
              |
              v
         Telegram User
```

## Component Responsibilities

| Component | Role |
|-----------|------|
| `telegram.py` (webhook handler) | HTTP entry point, secret validation, payload parsing, response dispatch |
| `Orchestrator` | Intent detection, agent routing, confidence scoring |
| `Conversation` model | Persistent session state per user per tenant |
| `Tenant` model | Multi-tenant isolation boundary |
| `_send_telegram_message` | Outbound Telegram API calls with chunking and error handling |

## Data Flow

- **Inbound:** Telegram Update JSON --> FastAPI request --> parsed (chat_id, user_id, text)
- **State:** Conversation row in PostgreSQL (keyed by tenant_id + channel + channel_user_id)
- **Processing:** Orchestrator delegates to the matched agent, which uses RAG + LLM
- **Outbound:** Response string --> chunked if >4096 chars --> Telegram sendMessage API

## Infrastructure

- **Webhook registration:** Done externally via `setWebhook` Telegram API call during deployment.
- **TLS:** Nginx terminates TLS; internal traffic is plaintext within Docker network.
- **Rate limiting:** Nginx limits `/api/v1/webhooks/telegram` to 100 req/60s globally.
- **Timeout:** `httpx.AsyncClient` uses 10-second timeout for outbound Telegram calls.

## Failure Modes

| Failure | Behavior |
|---------|----------|
| Invalid secret | 401 returned, logged with client IP |
| No tenant in DB | Bot replies "service temporarily unavailable" |
| Orchestrator error | Exception propagates, FastAPI returns 500 |
| Telegram API 429 | Logged, chunk skipped |
| Telegram API network error | Logged, swallowed |
