# Pseudocode: API Endpoints

## login()

```
FUNCTION login(payload: LoginSchema) -> TokenResponseSchema:
    IF payload.email != settings.admin_email: RAISE 401
    IF settings.admin_password_hash:
        IF NOT bcrypt_verify(payload.password, hash): RAISE 401
    ELSE:  # dev mode
        IF payload.password != DEV_DEFAULT: RAISE 401
    token = jwt_encode(sub=email, role="admin", tenant_id=DEFAULT, exp=now()+TTL)
    RETURN { access_token: token, token_type: "bearer", expires_in: seconds }
```

## create_conversation()

```
FUNCTION create_conversation(payload, tenant, db) -> ConversationResponseSchema:
    conv = Conversation(tenant_id=tenant.id, channel=payload.channel,
                        channel_user_id=payload.channel_user_id)
    db.add(conv); db.flush()
    IF payload.initial_message:
        Orchestrator(db, tenant.id).process_message(conv, payload.initial_message)
        db.flush()
    RETURN conv
```

## send_message()

```
FUNCTION send_message(conversation_id, payload, tenant, db):
    conv = SELECT Conversation WHERE id=conversation_id AND tenant_id=tenant.id
    IF conv is None: RAISE 404
    IF conv.status NOT IN ("active","escalated"): RAISE 409
    response = Orchestrator(db, tenant.id).process_message(conv, payload.content)
    recent = SELECT Message WHERE conversation_id ORDER BY created_at DESC LIMIT 2
    recent.reverse()  # [user_msg, assistant_msg]
    RETURN { user_message: recent[0], assistant_response: {
        content, agent_type, confidence, sources }, response_time_ms }
```

## get_metrics()

```
FUNCTION get_metrics(period, start_date, end_date, user, db):
    (date_from, date_to) = resolve_date_range(period, start_date, end_date)
    rows = SELECT DailyMetric WHERE tenant_id AND date BETWEEN range ORDER BY date
    total = SUM(consultations); leads = SUM(leads_generated)
    avg_rt = AVG(avg_response_time_ms); satisfaction = AVG(satisfaction_avg)
    escalation_rate = SUM(escalations) / total
    top_intents = aggregate JSON arrays, sort desc, take 5
    RETURN MetricsResponseSchema(...)
```

## get_current_tenant()

```
FUNCTION get_current_tenant(api_key, db) -> Tenant:
    IF api_key is None: RAISE 401 "API key required"
    FOR EACH tenant IN all Tenants:
        IF bcrypt_verify(api_key, tenant.api_key_hash): RETURN tenant
    RAISE 401 "Invalid API key"
```

## get_current_user()

```
FUNCTION get_current_user(credentials) -> dict:
    IF credentials is None: RAISE 401
    RETURN jwt_decode(credentials.token, secret, HS256)  # raises 401 if invalid
```
