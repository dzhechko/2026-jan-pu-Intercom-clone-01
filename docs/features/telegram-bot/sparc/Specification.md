# Specification -- Telegram Bot

## Webhook Endpoint

- **URL:** `POST /api/v1/webhooks/telegram`
- **Content-Type:** `application/json`
- **Auth:** `X-Telegram-Bot-Api-Secret-Token` header (validated against `TELEGRAM_WEBHOOK_SECRET`)

## Telegram Update Payload (inbound)

```json
{
  "update_id": 123456789,
  "message": {
    "message_id": 1,
    "from": { "id": 12345, "first_name": "Ivan", "is_bot": false },
    "chat": { "id": 12345, "type": "private" },
    "date": 1700000000,
    "text": "/start"
  }
}
```

Key fields extracted by the handler: `message.text`, `message.chat.id`, `message.from.id`.

## Bot Commands

| Command | Behavior |
|---------|----------|
| `/start` | Returns `START_GREETING` with capabilities list in Russian |

All other text is forwarded to the Orchestrator for agent routing.

## Message Flow

1. Telegram servers POST an Update to the webhook URL.
2. Handler validates `X-Telegram-Bot-Api-Secret-Token`.
3. Handler extracts `chat_id`, `user_id`, and `text`.
4. If text is `/start`, respond with greeting and return.
5. If text or chat_id is missing, return empty `{}`.
6. Look up tenant (first active tenant).
7. Find or create a `Conversation` (filtered by tenant, channel=telegram, channel_user_id, status=active).
8. Pass conversation + text to `Orchestrator.process_message()`.
9. Send orchestrator response back via `sendMessage` API.

## Outbound Telegram API Call

```
POST https://api.telegram.org/bot{TOKEN}/sendMessage
{
  "chat_id": 12345,
  "text": "Response text",
  "parse_mode": "Markdown"
}
```

- Messages over 4096 characters are split into chunks.
- HTTP 429 from Telegram is logged and the chunk is skipped.
- Network errors are caught, logged, and swallowed (no retry currently).

## Security

- **Secret validation:** If `TELEGRAM_WEBHOOK_SECRET` is set, every request must include a matching `X-Telegram-Bot-Api-Secret-Token` header. Mismatch returns 401.
- **IP logging:** Failed secret validation logs the client IP.
- **No raw SQL:** All DB access through SQLAlchemy ORM.
- **Multi-tenant isolation:** Conversations are scoped by `tenant_id`.
