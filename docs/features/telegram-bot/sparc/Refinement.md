# Refinement -- Telegram Bot

## Edge Cases

### EC-1: Empty or missing message body

- **Trigger:** Telegram sends an update with no `message` key (e.g., edited_message, channel_post, callback_query).
- **Current behavior:** `parse_update` returns `chat_id=None, text=""`, handler returns `{}` with 200.
- **Risk:** Silent discard is correct for non-message updates but loses callback_query data.
- **Mitigation:** Log the update type for observability. Future: handle `callback_query` for inline buttons.

### EC-2: Whitespace-only message

- **Trigger:** User sends a message containing only spaces, tabs, or newlines.
- **Current behavior:** `text.strip()` produces `""`, which fails the `not text` guard and returns `{}`.
- **Risk:** User gets no feedback.
- **Mitigation:** After stripping, if text is empty but chat_id is present, reply with a prompt like "Please describe your task."

### EC-3: Rate limiting from Telegram API (HTTP 429)

- **Trigger:** Bot sends too many messages in a short window.
- **Current behavior:** Logs a warning and skips the chunk.
- **Risk:** User receives an incomplete response with missing chunks.
- **Mitigation:** Implement exponential backoff with 1-3 retries before giving up. Respect `Retry-After` header.

### EC-4: Network timeout on outbound send

- **Trigger:** Telegram API is unreachable or slow (>10s).
- **Current behavior:** Exception caught, logged, swallowed.
- **Risk:** User never receives the bot's response.
- **Mitigation:** Queue failed messages in Redis for retry via a background worker.

### EC-5: Duplicate webhook deliveries

- **Trigger:** Telegram retries an unacknowledged webhook (server returned non-2xx or timed out).
- **Current behavior:** No deduplication. The same message is processed again, potentially creating duplicate conversations or double-charging LLM calls.
- **Risk:** Duplicate agent responses sent to user; wasted LLM tokens.
- **Mitigation:** Track `update_id` in Redis with a short TTL (5 minutes). Skip processing if `update_id` was already seen.

### EC-6: Message exceeds 4000-character input limit

- **Trigger:** User sends a very long message (Telegram allows up to 4096 chars).
- **Current behavior:** Full text is passed to the orchestrator without truncation.
- **Risk:** LLM context window waste; potential prompt injection in long payloads.
- **Mitigation:** Truncate to 4000 chars with a notice appended: "[message truncated]".

### EC-7: No tenant in database

- **Trigger:** Fresh deployment with no seed data.
- **Current behavior:** Bot replies "Service temporarily unavailable."
- **Risk:** Acceptable for MVP but unclear to the user.
- **Mitigation:** Ensure seed script creates a default tenant. Add a health check that verifies at least one tenant exists.

### EC-8: Concurrent conversation creation race condition

- **Trigger:** Two rapid messages from the same user arrive before the first conversation is flushed.
- **Current behavior:** Both handlers run the find query, both get None, both create a new Conversation.
- **Risk:** Duplicate active conversations for the same user.
- **Mitigation:** Add a unique constraint on (tenant_id, channel, channel_user_id, status) or use SELECT ... FOR UPDATE.

## Testing Gaps

| Gap | Suggested Test |
|-----|----------------|
| callback_query updates (inline buttons) | Test that non-message updates return 200 without error |
| Long message chunking (>4096 chars) | Unit test `_send_telegram_message` with 10000-char input |
| 429 retry behavior | Mock httpx to return 429, verify log and skip |
| Duplicate update_id | Send same update_id twice, verify single processing |
| Missing bot token config | Call `_send_telegram_message` with no token, verify no HTTP call |
