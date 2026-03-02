# Architecture — AI-Консультант Cloud.ru

## Architecture Overview

### Architecture Style

**Distributed Monolith (Monorepo)** — a single deployable unit with clearly separated internal modules, containerized with Docker Compose on VPS. This balances simplicity (no microservice overhead) with modularity (each agent/service is an isolated module).

### Rationale

- MVP timeline (3 months) favors monolith simplicity
- Team size (3 people) cannot sustain microservice complexity
- Docker Compose provides sufficient isolation between components
- Clear module boundaries allow future extraction to microservices if needed
- MCP-based agent architecture naturally decouples business logic

---

## High-Level Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          CLIENTS                                     │
│                                                                      │
│  ┌──────────┐   ┌──────────────┐   ┌──────────┐   ┌──────────────┐ │
│  │ Telegram  │   │ Web Widget   │   │ Bitrix24 │   │ Admin Panel  │ │
│  │   Bot     │   │ (cloud.ru)   │   │   CRM    │   │ (Dashboard)  │ │
│  └─────┬─────┘   └──────┬───────┘   └────┬─────┘   └──────┬───────┘ │
└────────┼────────────────┼────────────────┼────────────────┼─────────┘
         │                │                │                │
         ▼                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       NGINX (Reverse Proxy + TLS)                    │
│                       Port 443 / Rate Limiting                       │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
┌─────────────────────────────────┼───────────────────────────────────┐
│                          API GATEWAY                                 │
│                                                                      │
│  ┌──────────────────────────────┴──────────────────────────────────┐ │
│  │                    FastAPI Application                           │ │
│  │                                                                  │ │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────────────┐ │ │
│  │  │ Auth Module  │  │ Rate Limiter │  │ Webhook Router         │ │ │
│  │  │ (JWT+APIKey) │  │ (Redis)      │  │ (Telegram/Web/CRM)    │ │ │
│  │  └─────────────┘  └──────────────┘  └────────────────────────┘ │ │
│  └─────────────────────────────┬───────────────────────────────────┘ │
└────────────────────────────────┼────────────────────────────────────┘
                                 │
┌────────────────────────────────┼────────────────────────────────────┐
│                         CORE ENGINE                                  │
│                                                                      │
│  ┌─────────────────────────────┴──────────────────────────────────┐ │
│  │                     ORCHESTRATOR                                │ │
│  │   Intent Detection → Agent Selection → Response Assembly        │ │
│  └───────────┬──────────┬──────────┬──────────┬──────────┬────────┘ │
│              │          │          │          │          │           │
│  ┌───────────▼──┐ ┌─────▼────┐ ┌──▼──────┐ ┌▼────────┐ ┌▼───────┐ │
│  │  Architect   │ │   Cost   │ │Compliance│ │Migration│ │  Human │ │
│  │   Agent     │ │Calculator│ │  Agent   │ │  Agent  │ │Escalate│ │
│  │             │ │  Agent   │ │          │ │         │ │  Agent │ │
│  └──────┬──────┘ └────┬─────┘ └────┬─────┘ └────┬────┘ └───┬────┘ │
│         │             │            │             │          │       │
│  ┌──────▼─────────────▼────────────▼─────────────▼──────────▼────┐ │
│  │                    MCP Tool Layer                              │ │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────────────┐ │ │
│  │  │ Pricing API │  │ Config API   │  │ Compliance Checker   │ │ │
│  │  │ (Cloud.ru)  │  │ (Cloud.ru)   │  │ (152-ФЗ rules)      │ │ │
│  │  └─────────────┘  └──────────────┘  └──────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                     RAG PIPELINE                                │ │
│  │                                                                  │ │
│  │  Query → Embedding → Vector Search → BM25 → RRF Merge → Rerank│ │
│  │                                                                  │ │
│  └──────────────┬──────────────────────────────┬──────────────────┘ │
└─────────────────┼──────────────────────────────┼────────────────────┘
                  │                              │
┌─────────────────┼──────────────────────────────┼────────────────────┐
│                 DATA LAYER                                           │
│                                                                      │
│  ┌──────────────▼───────┐  ┌───────────────────▼──────────────────┐ │
│  │    PostgreSQL 16      │  │         Qdrant (Vector DB)           │ │
│  │                       │  │                                      │ │
│  │  - Conversations      │  │  - Document embeddings (1536-dim)   │ │
│  │  - Messages           │  │  - Collections per tenant           │ │
│  │  - Leads              │  │  - BM25 index for hybrid search     │ │
│  │  - Users/Tenants      │  │                                      │ │
│  │  - Agent configs      │  │                                      │ │
│  │  - Metrics            │  │                                      │ │
│  └───────────────────────┘  └──────────────────────────────────────┘ │
│                                                                      │
│  ┌───────────────────────┐  ┌──────────────────────────────────────┐ │
│  │    Redis 7             │  │         MinIO (S3-compatible)       │ │
│  │                       │  │                                      │ │
│  │  - Session cache      │  │  - Document corpus (originals)      │ │
│  │  - Rate limiting      │  │  - Generated PDFs/reports           │ │
│  │  - Message queue      │  │  - Backup storage                   │ │
│  │  - Pub/Sub (events)   │  │                                      │ │
│  └───────────────────────┘  └──────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. API Gateway (FastAPI)

**Responsibility:** HTTP/WebSocket entry point, authentication, rate limiting, request routing.

| Subcomponent | Technology | Purpose |
|-------------|-----------|---------|
| HTTP Router | FastAPI | REST API endpoints |
| WebSocket | FastAPI WebSocket | Real-time chat for web widget |
| Auth | PyJWT + custom middleware | JWT validation, API key auth |
| Rate Limiter | Redis + sliding window | Per-user and global rate limits |
| Telegram Webhook | python-telegram-bot | Parse Telegram updates |
| CORS | FastAPI middleware | Web widget cross-origin support |

### 2. Orchestrator

**Responsibility:** Intent detection, agent selection, conversation management, response assembly.

| Subcomponent | Purpose |
|-------------|---------|
| Intent Detector | Classify user message into intent categories |
| Agent Router | Select appropriate agent based on intent + context |
| Context Manager | Maintain conversation state and context window |
| Response Assembler | Format agent output for specific channel (Telegram/Web/CRM) |
| Confidence Scorer | Calculate aggregate confidence from RAG + LLM + tools |

### 3. Agent Layer (6 Agents)

Each agent is a **configuration**, not separate code:

```python
# Agent is defined by config, not by writing new code
agent_config = {
    "type": "architect",
    "system_prompt": "prompts/architect.md",  # markdown prompt file
    "tools": ["pricing_lookup", "service_catalog", "architecture_templates"],
    "rag_collections": ["cloud_ru_docs", "reference_architectures"],
    "confidence_threshold": 0.6,
    "max_turns": 20
}
```

| Agent | Tools (MCP) | RAG Collections |
|-------|------------|----------------|
| Architect | service_catalog, architecture_templates, sizing_calculator | cloud_ru_docs, reference_architectures |
| Cost Calculator | pricing_lookup, discount_calculator, tco_templates | pricing_data, competitor_pricing |
| Compliance | compliance_checker, certification_lookup | compliance_docs, regulatory_updates |
| Migration | migration_assessor, timeline_generator | migration_playbooks, case_studies |
| AI Factory | gpu_catalog, ml_sizing, benchmark_lookup | ai_factory_docs, gpu_specs |
| Human Escalation | sa_availability, calendar_booking, notification_sender | — |

### 4. RAG Pipeline

**Responsibility:** Document indexing, hybrid search (vector + BM25), reranking.

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Embedder | text-embedding-3-small (OpenAI) or e5-large-v2 (local) | Generate 1536-dim embeddings |
| Vector Store | Qdrant | Vector similarity search |
| BM25 Index | Qdrant built-in or Elasticsearch | Keyword search |
| RRF Merger | Custom Python | Reciprocal Rank Fusion |
| Reranker | cross-encoder/ms-marco (optional) | Cross-encoder reranking |
| Doc Processor | LangChain / custom | PDF/HTML → chunks → embeddings |

### 5. MCP Tool Layer

**Responsibility:** External API access for agents via Model Context Protocol.

```
MCP Server architecture:
  - Each tool group is an MCP server (separate process)
  - Agents call tools via MCP protocol (stdio or HTTP)
  - Tools are stateless — easy to test and deploy

MCP Servers:
  1. cloud-ru-api-server     → pricing, service catalog, configuration
  2. compliance-server       → 152-ФЗ rules, ФСТЭК checks
  3. analytics-server        → consultation metrics, ROI calculations
  4. crm-server             → Bitrix24, amoCRM API calls
  5. notification-server     → Telegram notifications, email alerts
```

### 6. Data Layer

| Store | Technology | Data | Scaling Strategy |
|-------|-----------|------|-----------------|
| Primary DB | PostgreSQL 16 | Conversations, leads, users, configs, metrics | Vertical (single node MVP, read replicas later) |
| Vector DB | Qdrant | Document embeddings, RAG index | Horizontal (collection-per-tenant) |
| Cache | Redis 7 | Sessions, rate limits, message queue | Single node (cluster later) |
| Object Store | MinIO | Document corpus, PDFs, backups | Single node |

---

## Technology Stack

| Layer | Technology | Version | Rationale |
|-------|-----------|---------|-----------|
| **Language** | Python | 3.12+ | LLM ecosystem, FastAPI, rapid development |
| **Web Framework** | FastAPI | 0.110+ | Async, type-safe, WebSocket support, OpenAPI docs |
| **LLM Client** | anthropic / gigachat SDK | latest | Model-agnostic, primary Claude, fallback GigaChat |
| **RAG Framework** | LangChain or custom | latest | Document processing, embedding, retrieval |
| **Vector DB** | Qdrant | 1.9+ | Hybrid search (vector + BM25), filtering, multi-tenant |
| **Primary DB** | PostgreSQL | 16 | ACID, JSONB for flexible schemas, proven reliability |
| **ORM** | SQLAlchemy + Alembic | 2.0+ | Async support, migrations |
| **Cache/Queue** | Redis | 7+ | Rate limiting, session cache, Pub/Sub for events |
| **Object Storage** | MinIO | latest | S3-compatible, self-hosted |
| **Reverse Proxy** | Nginx | 1.25+ | TLS termination, rate limiting, static files |
| **Containerization** | Docker + Docker Compose | 25+ / 2.24+ | Required by architecture constraints |
| **Frontend (Admin)** | React + TypeScript | 18+ | Dashboard SPA, reusable components |
| **UI Framework** | Tailwind CSS + shadcn/ui | latest | Rapid UI development |
| **Charting** | Recharts | latest | Dashboard analytics charts |
| **Telegram SDK** | python-telegram-bot | 21+ | Async, webhook support |
| **Testing** | pytest + pytest-asyncio | latest | Async test support |
| **Linting** | ruff | latest | Fast Python linter + formatter |
| **MCP SDK** | mcp (Python) | latest | Model Context Protocol implementation |

---

## Data Architecture

### Database Schema (PostgreSQL)

```sql
-- Multi-tenant support
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    config JSONB DEFAULT '{}',    -- agent configs, branding, etc.
    api_key_hash VARCHAR(255) NOT NULL,
    plan VARCHAR(50) DEFAULT 'pilot',  -- pilot, production, enterprise
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Conversations
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    channel VARCHAR(20) NOT NULL,  -- telegram, web_widget, crm
    channel_user_id VARCHAR(255),
    status VARCHAR(20) DEFAULT 'active',
    context JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_conversations_tenant ON conversations(tenant_id);
CREATE INDEX idx_conversations_status ON conversations(status);
CREATE INDEX idx_conversations_channel_user ON conversations(channel, channel_user_id);

-- Messages
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id),
    role VARCHAR(20) NOT NULL,     -- user, assistant, system, agent
    agent_type VARCHAR(30),
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',   -- confidence, sources, tool_calls
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_created ON messages(created_at);

-- Leads
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    conversation_id UUID REFERENCES conversations(id),
    contact JSONB DEFAULT '{}',
    qualification VARCHAR(20) DEFAULT 'cold',
    intent VARCHAR(30),
    estimated_deal_value DECIMAL(15,2),
    architecture_summary TEXT,
    tco_data JSONB,
    compliance_requirements TEXT[],
    crm_external_id VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_leads_tenant ON leads(tenant_id);
CREATE INDEX idx_leads_qualification ON leads(qualification);

-- Agent configurations (per tenant)
CREATE TABLE agent_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    agent_type VARCHAR(30) NOT NULL,
    system_prompt TEXT,
    confidence_threshold DECIMAL(3,2) DEFAULT 0.6,
    max_turns INT DEFAULT 20,
    rag_collections TEXT[],
    tools TEXT[],
    enabled BOOLEAN DEFAULT true,
    UNIQUE(tenant_id, agent_type)
);

-- Metrics (daily aggregation)
CREATE TABLE daily_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    date DATE NOT NULL,
    total_consultations INT DEFAULT 0,
    avg_response_time_ms INT,
    leads_generated INT DEFAULT 0,
    escalations INT DEFAULT 0,
    satisfaction_avg DECIMAL(3,2),
    top_intents JSONB,
    UNIQUE(tenant_id, date)
);
```

### Vector DB Collections (Qdrant)

```
Collections per tenant:
  - {tenant_slug}_cloud_docs          → Cloud provider documentation
  - {tenant_slug}_pricing             → Pricing data and tables
  - {tenant_slug}_compliance          → Regulatory documents
  - {tenant_slug}_architectures       → Reference architectures
  - {tenant_slug}_migration           → Migration playbooks
  - {tenant_slug}_ai_factory          → AI/GPU documentation

Shared collections:
  - competitor_pricing                → Multi-provider price comparison
  - regulatory_updates                → 152-ФЗ, ФСТЭК updates
```

---

## Security Architecture

### Authentication Flow

```
Admin Dashboard:
  Browser → POST /auth/login (email+password) → JWT (access + refresh)
  All subsequent requests: Authorization: Bearer <access_token>
  Token refresh: POST /auth/refresh with refresh_token

API Clients (Telegram bot, web widget):
  Request → X-API-Key: <tenant_api_key> → Validate against tenants table
  API key hashed with bcrypt in DB

Telegram Users:
  Telegram Bot API handles user identity
  channel_user_id = Telegram user ID (trusted, verified by Telegram)
```

### Authorization Matrix

| Role | Dashboard | Agent Config | Conversations | Metrics | Tenant Mgmt |
|------|:---------:|:------------:|:-------------:|:-------:|:------------:|
| superadmin | ✅ | ✅ | ✅ | ✅ | ✅ |
| admin | ✅ | ✅ | ✅ | ✅ | ❌ |
| agent_manager | ❌ | ✅ | ✅ (read) | ✅ | ❌ |
| viewer | ✅ (read) | ❌ | ❌ | ✅ (read) | ❌ |

### Data Flow Security

```
External (TLS 1.3):
  User ←→ Nginx (TLS termination) ←→ FastAPI

Internal (Docker network):
  FastAPI ←→ PostgreSQL (Docker internal network, no external port)
  FastAPI ←→ Qdrant (Docker internal network)
  FastAPI ←→ Redis (Docker internal network, AUTH enabled)
  FastAPI ←→ MCP Servers (stdio or Docker internal HTTP)

Sensitive Data:
  - API keys: bcrypt hashed in PostgreSQL
  - JWT secrets: environment variables (Docker secrets in production)
  - LLM API keys: environment variables
  - Conversation logs: encrypted at rest (PostgreSQL TDE)
  - PII: anonymized after 90 days (background job)
```

---

## Scalability Considerations

### Vertical Scaling (MVP → v1.0)

| Component | MVP | v1.0 |
|-----------|-----|------|
| VPS | 4 vCPU, 16GB RAM, 200GB SSD | 8 vCPU, 32GB RAM, 500GB SSD |
| PostgreSQL | Shared on VPS | Dedicated container, connection pool |
| Qdrant | Shared on VPS | Dedicated container, 8GB RAM |
| Redis | Shared on VPS | Dedicated container |

### Horizontal Scaling Readiness (v2.0+)

| Component | Strategy | Trigger |
|-----------|----------|---------|
| FastAPI | Multiple replicas behind Nginx | >100 concurrent users |
| PostgreSQL | Read replicas, connection pooling (PgBouncer) | >1000 queries/sec |
| Qdrant | Cluster mode, sharding by tenant | >100K documents |
| Redis | Redis Cluster | >10K ops/sec |
| Background Jobs | Celery workers (separate containers) | >100 jobs/min |

### Bottleneck Analysis

| Component | Bottleneck | Mitigation |
|-----------|-----------|------------|
| LLM API | Latency (2-10s per call) | Streaming responses, caching common queries |
| RAG retrieval | Embedding generation | Pre-compute embeddings, batch indexing |
| PostgreSQL | Write-heavy message logging | Async writes via Redis queue |
| Qdrant | Large corpus search | Collection-per-tenant, filtered search |

---

## Infrastructure Architecture

### Docker Compose Services

```yaml
services:
  # Application
  api:          # FastAPI main application
  admin:        # React admin dashboard (Nginx static)
  worker:       # Background job processor

  # MCP Servers
  mcp-cloud:    # Cloud.ru API tools
  mcp-compliance: # Compliance checking tools
  mcp-crm:      # CRM integration tools

  # Data stores
  postgres:     # Primary database
  qdrant:       # Vector database
  redis:        # Cache and message queue
  minio:        # Object storage

  # Infrastructure
  nginx:        # Reverse proxy, TLS, rate limiting
```

### Network Architecture

```
External network (public):
  - nginx:443 (HTTPS)
  - nginx:80 (redirect to HTTPS)

Internal network (app_network):
  - api:8000
  - admin:3000
  - worker:8001
  - mcp-cloud:8010
  - mcp-compliance:8011
  - mcp-crm:8012

Data network (data_network):
  - postgres:5432
  - qdrant:6333
  - redis:6379
  - minio:9000
```

### Deployment Strategy

```
VPS (AdminVPS or HOSTKEY):
  - Location: Moscow (152-ФЗ compliance)
  - OS: Ubuntu 24.04 LTS
  - Docker Engine: 25+
  - Docker Compose: 2.24+

Deploy process:
  1. SSH to VPS
  2. git pull (or docker pull from registry)
  3. docker compose up -d --build
  4. docker compose exec api alembic upgrade head  (migrations)
  5. Health check: curl https://api.domain/health
  6. Rollback: docker compose down && git checkout prev-tag && docker compose up -d
```

---

## Monitoring Architecture

| Layer | Tool | Metrics |
|-------|------|---------|
| Application | Prometheus + custom metrics | Request latency, error rates, LLM call duration |
| Infrastructure | Docker stats + cAdvisor | CPU, memory, disk, network per container |
| Logs | Loki + Promtail (or simple file logs) | Structured JSON logs, searchable |
| Dashboards | Grafana | All metrics visualized |
| Alerts | Grafana Alerting → Telegram | Error rate >1%, response time >30s, disk >80% |
| Uptime | UptimeRobot (external) | HTTPS endpoint monitoring |

---

## ADR (Architecture Decision Records)

### ADR-001: Distributed Monolith over Microservices

**Status:** Accepted
**Context:** Team of 3, MVP in 3 months, need fast iteration.
**Decision:** Single deployable unit with internal module boundaries.
**Rationale:** Microservices add networking, observability, and deployment complexity that a 3-person team cannot sustain. Module boundaries via Python packages allow future extraction.
**Consequences:** Must maintain discipline in module boundaries. Shared database is acceptable for MVP.

### ADR-002: Qdrant over Pinecone/Weaviate

**Status:** Accepted
**Context:** Need vector DB with hybrid search, self-hosted (152-ФЗ), multi-tenant.
**Decision:** Qdrant (self-hosted Docker container).
**Rationale:** Open-source, built-in BM25 hybrid search, collection-level multi-tenancy, Rust performance, Docker-native. Pinecone is cloud-only (not 152-ФЗ compliant). Weaviate is heavier.
**Consequences:** Self-managed backups and upgrades. Limited to single-node initially.

### ADR-003: MCP for Agent Tool Access

**Status:** Accepted
**Context:** 6 agents need access to external APIs (pricing, compliance, CRM).
**Decision:** Model Context Protocol (MCP) servers for tool layer.
**Rationale:** Industry standard (97M+ SDK downloads), supported by Claude natively, clean separation between agent logic and tool implementation. Each tool group is an independent MCP server.
**Consequences:** Need to implement MCP servers for each tool group. Adds process management overhead.

### ADR-004: FastAPI over Django/Flask

**Status:** Accepted
**Context:** Need async HTTP + WebSocket + OpenAPI docs.
**Decision:** FastAPI with Pydantic v2.
**Rationale:** Native async (critical for LLM streaming), automatic OpenAPI docs, Pydantic validation, WebSocket for web widget. Django is too heavy for API-first product. Flask lacks async and type safety.
**Consequences:** Less built-in admin UI (compensated by custom React dashboard).

### ADR-005: PostgreSQL + Redis over MongoDB

**Status:** Accepted
**Context:** Need reliable storage for conversations, leads, metrics with complex queries.
**Decision:** PostgreSQL 16 + Redis 7.
**Rationale:** ACID compliance for lead data, JSONB for flexible schemas (conversation context), strong query capabilities for analytics. Redis for caching and rate limiting. MongoDB adds operational complexity without clear benefit.
**Consequences:** Schema migrations needed (Alembic). Must manage connection pooling for async.
