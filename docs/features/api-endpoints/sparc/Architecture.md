# Architecture: API Endpoints

## Layer Diagram

```
Client (Telegram / Web Widget / Admin Dashboard)
  -> Nginx (TLS, rate limiting, security headers)
  -> FastAPI (src/api/main.py)
       +-- Routes    (src/api/routes/)       -- thin HTTP handlers
       +-- Schemas   (src/api/schemas/)      -- Pydantic v2 request/response
       +-- Security  (src/core/security.py)  -- JWT + API-key auth
       +-- Orchestrator (src/orchestrator/)   -- intent -> agent -> RAG -> LLM
       +-- Models    (src/models/)           -- Conversation, Message, Tenant, Lead
       +-- Database  (src/core/database.py)  -- AsyncSession -> PostgreSQL 16
```

## Key Architectural Decisions

**ADR-1: Two Auth Mechanisms.** Conversations use `X-API-Key` (machine-to-machine,
long-lived, tenant-scoped). Dashboard uses Bearer JWT (human admin, short-lived,
user-scoped). Keeps bot/widget auth separate from admin auth.

**ADR-2: Tenant Isolation at Query Level.** Every DB query filters by `tenant_id`,
injected via `get_current_tenant` / `get_current_user` dependencies. No cross-tenant
data leakage is possible.

**ADR-3: Thin Routes, Fat Orchestrator.** Route handlers validate input (Pydantic)
and delegate to `Orchestrator.process_message()`. Routes never call LLM APIs directly.

**ADR-4: Pydantic v2 as Contract.** All bodies are typed via Pydantic v2 with
`from_attributes=True` for ORM compatibility, giving automatic OpenAPI docs and
input validation.

## Data Flow: Send Message

```
POST /conversations/{id}/messages
  -> Pydantic validates MessageCreateSchema
  -> get_current_tenant resolves Tenant from X-API-Key
  -> Load Conversation (tenant-scoped), check status in (active, escalated)
  -> Orchestrator.process_message() -> intent -> agent -> RAG -> LLM -> save
  -> Read last 2 Messages, build SendMessageResponseSchema
  -> Return JSON: user_message + assistant_response + response_time_ms
```

## Dependencies

| Component | Technology | Purpose |
|-----------|------------|---------|
| Web framework | FastAPI | Async HTTP, OpenAPI docs |
| ORM | SQLAlchemy 2.0 (async) | DB access, tenant filtering |
| Validation | Pydantic v2 | Request/response schemas |
| Auth | python-jose + bcrypt | JWT signing, password hashing |
| Database | PostgreSQL 16 + asyncpg | Persistent storage |
| Reverse proxy | Nginx | TLS, rate limiting, headers |
