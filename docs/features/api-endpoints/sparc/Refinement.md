# Refinement: API Endpoints

## Edge Cases and Mitigations

### 1. Authentication Failures

| Case | Current Behavior | Risk | Mitigation |
|------|-----------------|------|------------|
| Missing X-API-Key header | 401 via `get_current_tenant` | None | Handled |
| Invalid API key (no match) | 401 after scanning all tenants | Timing attack (bcrypt is slow) | Acceptable: bcrypt is constant-time per hash |
| Expired JWT | 401 via `decode_token` JWTError | None | Handled |
| Malformed JWT | 401 via `decode_token` JWTError | None | Handled |
| Valid JWT but missing tenant_id claim | `user.get("tenant_id")` returns None | Queries return empty results silently | Add claim validation in `get_current_user` |

### 2. Rate Limiting

| Endpoint | Limit | Enforcement |
|----------|-------|-------------|
| POST .../messages | 30 req/60s per user | Nginx `limit_req` zone |
| POST /auth/login | 5 req/60s per IP | Nginx `limit_req` zone |
| GET /dashboard/* | 60 req/60s per user | Nginx `limit_req` zone |
| Global | 1000 req/60s | Nginx `limit_req` zone |

Edge: Rate limit exceeded returns 429 from Nginx before reaching FastAPI.
The client must implement exponential backoff.

### 3. Concurrent Writes

| Scenario | Risk | Mitigation |
|----------|------|------------|
| Two messages sent simultaneously to same conversation | Race condition in message ordering | SQLAlchemy `flush()` within the same async session serializes writes; `created_at` ordering is deterministic |
| Conversation status changed to "closed" mid-message | 409 returned to second request | Status check before orchestrator call; acceptable |
| Parallel dashboard queries | No write conflict | Read-only queries, no risk |

### 4. Missing or Invalid tenant_id

| Scenario | Impact | Mitigation |
|----------|--------|------------|
| API key resolves to tenant but tenant has no data | Empty result sets, zero metrics | Valid behavior; dashboard shows zeros |
| Tenant deleted while session active | Subsequent requests fail with 401 | API key lookup fails; acceptable |
| JWT tenant_id claim is None | Dashboard queries return no data | Should validate claim presence in `get_current_user` |

### 5. Input Validation Edge Cases

| Input | Schema Constraint | Behavior |
|-------|-------------------|----------|
| Empty string content | `MessageCreateSchema.content` has no `min_length` | Orchestrator receives empty string -- should add `min_length=1` |
| Content exceeds 10000 chars | `max_length=10000` on `content` field | 422 Unprocessable Entity (Pydantic) |
| Invalid channel value | `pattern="^(telegram\|web_widget\|crm)$"` | 422 Unprocessable Entity |
| Non-UUID conversation_id | Path parameter parsed as string | 404 from DB query (no match) |
| SQL injection in content | Parameterized queries via SQLAlchemy | Safe |

### 6. Orchestrator Failures

| Failure | Impact | Mitigation |
|---------|--------|------------|
| LLM API timeout | `send_message` hangs or times out | Add timeout to orchestrator (30s); return 504 |
| LLM returns empty response | assistant_response.content is empty | Orchestrator should return a fallback message |
| RAG search returns no results | Low confidence, possible escalation | Confidence < 0.6 triggers human escalation |
| Orchestrator raises unhandled exception | 500 Internal Server Error | Add try/except in route; return 502 with generic message |

### 7. Data Integrity

| Scenario | Risk | Mitigation |
|----------|------|------------|
| `daily_metrics` table empty for period | Division by zero in `get_metrics` | Guarded: `if total_consultations > 0` |
| `top_intents` JSON field is malformed | KeyError in aggregation loop | Defensive `.get()` calls with defaults |
| Lead with NULL `estimated_deal_value` | Sum includes None | `func.coalesce(..., 0)` in SQL |

## Recommended Improvements

1. Add `min_length=1` to `MessageCreateSchema.content`
2. Validate `tenant_id` claim presence in `get_current_user`
3. Add explicit timeout (30s) around `orchestrator.process_message()`
4. Return structured error responses (`{"error": "code", "detail": "..."}`)
5. Add pagination to `GET /conversations/{id}` message history
6. Cache `get_current_tenant` API key lookups in Redis (TTL 5 min)
