# AI-Консультант Cloud.ru

Multi-agent AI platform for pre-sales cloud consulting. 6 specialized agents deliver instant architecture recommendations, TCO calculations, compliance guidance, migration planning, and GPU/AI advisory for Russian cloud providers — via Telegram, web widget, and Bitrix24 CRM.

**Status: v1.0.0** — all 15 features implemented, 138 tests passing.

## Features

### MVP (10 features)

- **Architect Agent** — Cloud architecture recommendations with RAG-grounded answers
- **Cost Calculator** — TCO comparison across Cloud.ru, Yandex Cloud, VK Cloud
- **Compliance Agent** — 152-ФЗ, ФСТЭК, КИИ regulatory guidance
- **Human Escalation** — Automatic handoff when confidence < 0.6
- **Orchestrator** — Intent detection, agent routing, confidence scoring
- **RAG Pipeline** — Hybrid search (vector + BM25 + RRF) over Cloud.ru docs
- **Telegram Bot** — Webhook integration with bot commands
- **API Endpoints** — FastAPI REST API for conversations, messages, dashboard
- **Admin Dashboard** — Conversation list, metrics overview, agent configs
- **Lead Qualification** — Automatic lead scoring from consultations

### v1.0 (5 features)

- **Migration Agent** — Step-by-step migration planning from on-premise/other clouds
- **AI Factory Agent** — GPU infrastructure recommendations for ML/AI workloads
- **Web Chat Widget** — Embeddable JavaScript widget for website integration
- **ROI Analytics** — Consultation metrics, conversion tracking, SA time savings
- **Bitrix24 CRM** — Automatic lead/deal creation from qualified consultations

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0 |
| Database | PostgreSQL 16 + Alembic migrations |
| Vector DB | Qdrant (hybrid search) |
| Cache | Redis 7 |
| LLM | Claude API (primary) + GigaChat (fallback) |
| Object Storage | MinIO (S3-compatible) |
| Admin UI | React 18, TypeScript, Tailwind CSS, Recharts |
| Web Widget | Vanilla TypeScript, embeddable |
| CRM | Bitrix24 REST API |
| Deploy | Docker Compose on VPS (Moscow DC) |

## Quick Start

```bash
# Clone
git clone <repo-url>
cd ai-consultant-cloudru

# Setup environment
cp .env.example .env
# Edit .env with your API keys (see .env.example for full list)

# Start all services
docker compose up -d

# Run migrations
docker compose exec api alembic upgrade head

# Seed data and index documents
docker compose exec api python scripts/seed_data.py
docker compose exec api python scripts/index_documents.py

# Verify
curl http://localhost:8000/health
```

## Development

See [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) for full development workflow.

```bash
# Run all tests (138 tests)
pytest tests/ -v --cov=src

# Unit tests only (fast, ~4s)
pytest tests/unit/ -v

# Integration tests (requires Docker services)
pytest tests/integration/ -v

# Lint + format
ruff check . && ruff format .

# Security scan
bandit -r src/ -ll
```

## Project Structure

```
src/
  api/routes/       — FastAPI endpoints (conversations, dashboard, telegram, auth, widget)
  orchestrator/     — Intent detection, agent routing, confidence scoring
  rag/              — RAG pipeline (embedder, hybrid search, indexer)
  models/           — SQLAlchemy models (conversations, messages, leads, tenants)
  services/         — Business logic (TCO, lead qualification, CRM, escalation)
admin/              — React admin dashboard (metrics, analytics, ROI)
widget/             — Embeddable web chat widget
prompts/            — Agent system prompts (architect, cost, compliance, migration, AI factory)
corpus/             — RAG document corpus
tests/              — 138 tests (unit + integration)
```

## Documentation

| Document | Description |
|----------|-------------|
| [PRD](docs/PRD.md) | Product requirements, user stories |
| [Specification](docs/Specification.md) | Acceptance criteria, NFRs |
| [Architecture](docs/Architecture.md) | System design, tech decisions |
| [Pseudocode](docs/Pseudocode.md) | Algorithms, API contracts |
| [Refinement](docs/Refinement.md) | Edge cases, testing strategy |
| [Completion](docs/Completion.md) | Deployment, CI/CD setup |

## Architecture

```
Telegram / Web Widget / CRM
            |
          Nginx (TLS, rate limiting)
            |
         FastAPI
            |
       Orchestrator (intent detection + confidence scoring)
            |
    +-------+-------+-------+-------+-------+
    |       |       |       |       |       |
Architect  Cost  Compliance Migration AI Factory  Human
  Agent   Calc    Agent     Agent     Agent    Escalation
    |       |       |         |         |
    +---+---+---+---+---------+---------+
        |       |
      RAG     MCP Tools
   (Qdrant)  (Pricing, CRM)
        |
   PostgreSQL + Redis + MinIO
```

## License

Proprietary — Cloud.ru
