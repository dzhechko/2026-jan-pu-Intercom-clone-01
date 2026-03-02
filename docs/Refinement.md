# Refinement — AI-Консультант Cloud.ru

## Edge Cases Matrix

| # | Scenario | Input | Expected Behavior | Handling |
|---|----------|-------|--------------------|----------|
| 1 | Empty message | User sends empty string or whitespace | Ignore, prompt for input | Validation middleware, return friendly prompt |
| 2 | Very long message | User sends 10K+ characters | Truncate to 4000 chars, process | Truncate with notice: "Я обработал первые 4000 символов" |
| 3 | Non-Russian language | User writes in English/Chinese | Respond in detected language, default Russian | Language detection, multilingual system prompts |
| 4 | Offensive content | User sends abusive messages | Politely decline, log | Content filter before agent processing |
| 5 | Competitor probing | Competitor asks about internals | Answer product capabilities only, not architecture | System prompt instruction to avoid revealing internals |
| 6 | Simultaneous sessions | Same user opens Telegram + web widget | Separate conversations per channel | channel + channel_user_id as unique key |
| 7 | Stale pricing data | RAG has outdated prices (>30 days) | Flag as potentially outdated | Metadata check: if doc.last_updated > 30 days, add disclaimer |
| 8 | LLM hallucination | AI generates non-existent service | RAG-grounded responses, source citation | Confidence < 0.6 triggers disclaimer or escalation |
| 9 | Network timeout to LLM | LLM API doesn't respond in 30s | Retry once, then apologize | 30s timeout, 1 retry, fallback message |
| 10 | Vector DB down | Qdrant container crashes | Serve from cache or acknowledge limitation | Health check, auto-restart, cached popular queries in Redis |
| 11 | Telegram rate limit | Bot exceeds Telegram API limits | Queue messages, retry with backoff | Rate-aware message queue, exponential backoff |
| 12 | Large TCO request | 500+ VMs with complex configurations | Process in chunks, stream results | Batch processing, progressive response delivery |
| 13 | Ambiguous workload | "I need cloud" with no details | Ask 2-3 clarifying questions | Orchestrator triggers clarification flow |
| 14 | Multi-provider comparison | "Compare ALL Russian cloud providers" | Compare top 3, mention data limitations | Limit to providers with pricing data in RAG |
| 15 | Compliance edge case | Workload spans CII and non-CII | Explain dual requirements | Compliance agent handles mixed workloads |
| 16 | Conversation timeout | User inactive for 24 hours | Auto-close, send summary | Background job closes stale conversations |
| 17 | Token limit exceeded | Conversation context exceeds LLM window | Summarize older messages | Sliding window with summarization |
| 18 | Concurrent writes | Multiple messages from same user quickly | Process sequentially per conversation | Per-conversation lock (Redis) |

---

## Testing Strategy

### Unit Tests

**Coverage target:** 80% for core modules, 90% for agent orchestration.

| Module | Critical Paths | Coverage Target |
|--------|---------------|:---:|
| Orchestrator | Intent detection, agent routing, confidence scoring | 90% |
| RAG Pipeline | Embedding, search, RRF merge, reranking | 85% |
| TCO Calculator | Price lookup, calculation, comparison | 90% |
| Lead Qualification | Scoring, classification, contact extraction | 85% |
| Auth Module | JWT validation, API key verification, RBAC | 90% |
| Telegram Handler | Message parsing, formatting, webhook processing | 80% |
| MCP Tools | Tool execution, error handling, response parsing | 85% |

### Integration Tests

| Test ID | Scenario | Components | Expected Result |
|---------|----------|------------|-----------------|
| IT-001 | Full consultation flow | API → Orchestrator → Agent → RAG → LLM → DB | Response with sources, saved to DB |
| IT-002 | Telegram webhook → response | Telegram webhook → API → Agent → Telegram API | Message delivered to user |
| IT-003 | Lead creation → CRM sync | Qualification → Lead → Bitrix24 API | Deal created in CRM |
| IT-004 | Human escalation flow | Low confidence → Escalation → SA notification | SA receives context, user notified |
| IT-005 | RAG index and query | Doc upload → Embedding → Qdrant → Query → Results | Relevant documents returned |
| IT-006 | Multi-tenant isolation | Tenant A query → Only tenant A data | No cross-tenant data leakage |
| IT-007 | Rate limiting | 31 requests in 1 minute | 31st request returns 429 |
| IT-008 | Auth flow | Login → JWT → Protected endpoint → Success | Valid JWT grants access |

### E2E Tests

| Test ID | User Journey | Steps | Success Criteria |
|---------|-------------|-------|-----------------|
| E2E-001 | VMware migration consultation | 1. Start Telegram bot 2. Ask about migration 3. Provide workload details 4. Get architecture 5. Get TCO 6. Get migration plan | All 4 agents respond, lead created |
| E2E-002 | Compliance check | 1. Ask about 152-ФЗ 2. Describe workload 3. Get compliance assessment | Compliance agent responds with specific requirements |
| E2E-003 | Human escalation | 1. Ask complex question 2. AI confidence < 0.6 3. Escalation triggered 4. SA receives context | Seamless handoff with full context |
| E2E-004 | Admin dashboard | 1. Login 2. View metrics 3. Check consultation list 4. Review lead | All pages load, data accurate |
| E2E-005 | Web widget | 1. Load cloud.ru page 2. Click widget 3. Start consultation 4. Get response | Widget loads, conversation works |

### Performance Tests

| Test ID | Scenario | Load | Target | Tool |
|---------|----------|------|--------|------|
| PT-001 | Concurrent consultations | 20 parallel sessions | All respond < 30s | Locust |
| PT-002 | RAG search under load | 100 queries/sec | p99 < 2s | Locust |
| PT-003 | Dashboard API | 50 concurrent users | Page load < 3s | Locust |
| PT-004 | Telegram webhook throughput | 100 messages/sec | No dropped messages | Custom script |
| PT-005 | Database write throughput | 1000 inserts/sec | No degradation | pgbench |

---

## Test Cases (Gherkin)

### Feature: AI Consultation

```gherkin
Feature: AI Cloud Consultation

  Background:
    Given the AI-Консультант system is running
    And the Telegram bot is connected
    And RAG corpus contains Cloud.ru documentation

  Scenario: Happy path - architecture consultation
    Given a user sends "Мне нужно мигрировать 200 серверов VMware в облако"
    When the Architect Agent processes the request
    Then the response contains a target architecture
    And the response includes Cloud.ru service names
    And the response has confidence >= 0.7
    And the response includes source references
    And the response time is under 30 seconds

  Scenario: TCO calculation with comparison
    Given a user sends "Сравни стоимость 50 ВМ: 8 vCPU, 32GB RAM у трёх провайдеров"
    When the Cost Calculator Agent processes the request
    Then the response contains a comparison table
    And the table includes Cloud.ru, Yandex Cloud, and VK Cloud
    And each provider has monthly, annual, and 3-year costs
    And the cheapest option is highlighted

  Scenario: Compliance advisory
    Given a user sends "Мы обрабатываем персональные данные. Соответствует ли Cloud.ru 152-ФЗ?"
    When the Compliance Agent processes the request
    Then the response confirms compliance status
    And lists specific certifications
    And recommends security level (УЗ)
    And cites regulatory documents

  Scenario: Low confidence triggers escalation
    Given a user asks about a highly specialized FPGA workload
    When the AI's confidence drops below 0.6
    Then the system offers to connect with a human SA
    And creates an escalation ticket
    And passes full conversation context

  Scenario: User requests human explicitly
    Given a user sends "Хочу поговорить с человеком"
    When the escalation is triggered
    Then the system acknowledges the request
    And notifies an available SA
    And preserves the full conversation for the SA
```

### Feature: Multi-Channel Delivery

```gherkin
Feature: Multi-Channel Support

  Scenario: Telegram bot interaction
    Given a user opens the Telegram bot
    When they send /start
    Then the bot responds with a greeting in Russian
    And lists available capabilities
    And offers to start a consultation

  Scenario: Web widget initialization
    Given a visitor loads the cloud.ru website
    When the page fully loads
    Then a chat widget appears in the bottom-right corner
    And clicking it opens the chat panel
    And the greeting appears within 1 second

  Scenario: Session continuity
    Given a user had a consultation yesterday via Telegram
    When they message the bot today saying "Что насчёт плана миграции?"
    Then the bot restores previous conversation context
    And responds in context of the previous discussion
```

### Feature: Admin Dashboard

```gherkin
Feature: Admin Dashboard

  Scenario: View daily metrics
    Given an admin is logged into the dashboard
    When they view the main page
    Then they see today's consultation count
    And average response time
    And leads generated count
    And escalation rate
    And a 7-day trend chart

  Scenario: ROI calculation
    Given 30 days of data exists
    When the admin views the ROI page
    Then they see total SA hours saved
    And total leads generated
    And estimated pipeline value in rubles
    And cost comparison: AI vs equivalent SA headcount
```

---

## Performance Optimizations

### Caching Strategy

| Cache Layer | What | TTL | Invalidation |
|-------------|------|-----|-------------|
| Redis: query cache | Common RAG queries → results | 1 hour | On RAG corpus update |
| Redis: pricing cache | Provider pricing lookups | 24 hours | On pricing data refresh |
| Redis: session cache | Conversation context | 24 hours | On conversation close |
| Application: LLM cache | Identical prompts → responses | 30 min | LRU eviction |
| CDN: admin assets | Static JS/CSS/images | 7 days | On deploy (cache bust) |

### Database Optimizations

| Optimization | Target | Implementation |
|-------------|--------|----------------|
| Connection pooling | Reduce connection overhead | SQLAlchemy async pool (pool_size=20, max_overflow=10) |
| Async writes | Reduce response latency | Queue message writes to Redis, batch insert |
| Partial indexes | Speed up active conversation queries | `CREATE INDEX ON conversations(status) WHERE status = 'active'` |
| JSONB indexing | Speed up context queries | GIN index on `conversations.context` |
| Materialized views | Dashboard metrics | Refresh daily_metrics table via background job |

### LLM Optimizations

| Optimization | Impact | Implementation |
|-------------|--------|----------------|
| Streaming responses | Perceived latency reduction 3-5x | SSE for web, chunked Telegram messages |
| Prompt caching | Cost reduction 30-50% | Anthropic prompt caching for system prompts |
| Smaller models for routing | Faster intent detection | Haiku for intent → Sonnet/Opus for response |
| Context window management | Prevent token overflow | Sliding window with summarization at 80% capacity |

---

## Security Hardening

### Input Validation

| Input | Validation | Action |
|-------|-----------|--------|
| User message | Max 4000 chars, UTF-8, strip HTML | Truncate, sanitize, log |
| API key | Exact format (32 hex chars) | Reject invalid format |
| JWT token | Valid signature, not expired, correct issuer | 401 response |
| Webhook payload | Valid Telegram signature | Reject, log IP |
| Admin form inputs | Parameterized queries, no SQL injection | SQLAlchemy ORM (no raw SQL) |
| File uploads (RAG) | Max 50MB, allowed types (PDF, HTML, MD, TXT) | Reject, return error |

### Rate Limiting

| Endpoint | Limit | Window | Burst |
|----------|-------|--------|-------|
| POST /messages (per user) | 30 | 1 minute | 5 |
| POST /messages (global) | 1000 | 1 minute | 100 |
| POST /auth/login | 5 | 5 minutes | 2 |
| GET /dashboard/* | 100 | 1 minute | 20 |
| POST /webhooks/telegram | 500 | 1 minute | 50 |

### Audit Logging

```
Every action logged as structured JSON:
{
  "timestamp": "2026-03-02T10:30:00Z",
  "level": "INFO",
  "event": "consultation_completed",
  "tenant_id": "uuid",
  "user_id": "telegram:12345",
  "conversation_id": "uuid",
  "agent_type": "architect",
  "confidence": 0.85,
  "response_time_ms": 4200,
  "tokens_used": 1500,
  "sources_count": 3
}

Retention: 90 days hot (PostgreSQL), 1 year cold (MinIO), then anonymized.
```

---

## Technical Debt Items

| # | Item | Severity | When to Address | Description |
|---|------|----------|----------------|-------------|
| 1 | Monolith module coupling | Medium | v1.0 | Extract agents into separate Python packages with clear interfaces |
| 2 | Single-node PostgreSQL | Medium | v2.0 | Add read replicas and PgBouncer when >5 clients |
| 3 | No distributed tracing | Low | v1.0 | Add OpenTelemetry for request tracing across components |
| 4 | Manual RAG corpus updates | Medium | v1.0 | Automate document crawling and re-indexing pipeline |
| 5 | No A/B testing framework | Low | v2.0 | Add prompt A/B testing for agent optimization |
| 6 | Hardcoded provider list | Low | v1.0 | Make provider comparison configurable per tenant |
| 7 | No graceful shutdown | Medium | MVP | Add SIGTERM handler for in-flight request completion |
| 8 | Missing request validation schemas | Medium | MVP | Add Pydantic models for all API endpoints |
