# Pseudocode -- Telegram Bot

## handle_webhook(request, secret_header, db)

```
function handle_webhook(request, secret_header, db):
    if not validate_secret(secret_header):
        raise HTTP 401

    body = await request.json()
    chat_id, user_id, text = parse_update(body)

    if not chat_id or not text: return {}
    if text == "/start":
        await send_response(chat_id, START_GREETING); return {}

    tenant = await db.query(Tenant).first()
    if not tenant:
        await send_response(chat_id, "Service unavailable"); return {}

    conversation = await db.query(Conversation).filter_by(
        tenant_id=tenant.id, channel="telegram",
        channel_user_id=str(user_id), status="active"
    ).first()
    if not conversation:
        conversation = Conversation(tenant_id=tenant.id,
            channel="telegram", channel_user_id=str(user_id))
        db.add(conversation); await db.flush()

    response = await Orchestrator(db, tenant.id).process_message(conversation, text)
    await send_response(chat_id, response.content)
    return {}
```

## parse_update(body)

```
function parse_update(body):
    message = body.get("message", {})
    text    = message.get("text", "").strip()
    chat_id = message.get("chat", {}).get("id")
    user_id = message.get("from", {}).get("id")
    return (chat_id, user_id, text)
```

## send_response(chat_id, text)

```
function send_response(chat_id, text):
    if BOT_TOKEN is not set:
        log_warning("bot_token_not_set")
        return

    url = "https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    # Telegram message limit is 4096 characters
    chunks = split_text(text, max_length=4096)

    for chunk in chunks:
        try:
            response = await http_post(url, json={
                "chat_id": chat_id,
                "text": chunk,
                "parse_mode": "Markdown"
            }, timeout=10s)

            if response.status == 429:
                log_warning("rate_limited", chat_id=chat_id)
        except NetworkError:
            log_exception("send_failed", chat_id=chat_id)
```

## validate_secret(header_value)

```
function validate_secret(header_value):
    if WEBHOOK_SECRET is not configured:
        return True   # skip validation when no secret is set
    return header_value == WEBHOOK_SECRET
```
