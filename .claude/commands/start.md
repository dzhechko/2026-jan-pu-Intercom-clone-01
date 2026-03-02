# /start — Bootstrap AI-Консультант Cloud.ru

## Phase 1: Project Scaffold

1. Create project directory structure (see CLAUDE.md)
2. Initialize Python project:
   - `pyproject.toml` with dependencies (fastapi, sqlalchemy, qdrant-client, anthropic, python-telegram-bot, redis, mcp, pydantic)
   - `requirements.txt` + `requirements-dev.txt` (pytest, ruff, bandit, locust)
3. Create `Dockerfile` (Python 3.12-slim, multi-stage build)
4. Create `docker-compose.yml` with services: api, admin, postgres, qdrant, redis, minio, nginx
5. Create `.env.example` with all required environment variables
6. Create `.gitignore` (Python + Node + Docker + .env)

## Phase 2: Core Implementation

Start with MVP features (Month 1-3 scope from PRD):

1. **Database models** — `src/models/` (conversations, messages, leads, tenants, agent_configs, daily_metrics)
   - Reference: `docs/Architecture.md` → Database Schema section
2. **RAG Pipeline** — `src/rag/` (document processor, embedder, hybrid search, RRF merge)
   - Reference: `docs/Pseudocode.md` → RAG Search algorithm
3. **Orchestrator** — `src/orchestrator/` (intent detection, agent routing, confidence scoring)
   - Reference: `docs/Pseudocode.md` → Orchestrator algorithm
4. **Agent configs** — `prompts/` (architect.md, cost_calculator.md, compliance.md, human_escalation.md)
5. **API endpoints** — `src/api/` (conversations, messages, dashboard, webhooks)
   - Reference: `docs/Pseudocode.md` → API Contracts
6. **Telegram bot** — `src/api/webhooks/telegram.py`

## Phase 3: Infrastructure

1. Set up Alembic migrations
2. Configure Nginx (TLS, rate limiting, reverse proxy)
3. Add health check endpoints (`/health`, `/health/ready`, `/metrics`)
4. Add structured logging (JSON format)
5. Create seed scripts (`scripts/seed_data.py`, `scripts/index_documents.py`)

## Phase 4: Testing

1. Unit tests for orchestrator, RAG, TCO calculator
2. Integration tests for API endpoints
3. E2E smoke test for Telegram bot flow

## Priority Order

Implement "Must" requirements first (see `docs/Specification.md` Feature Matrix):
1. Architect Agent + RAG Pipeline + Telegram Bot (core loop)
2. Cost Calculator Agent + TCO Algorithm
3. Compliance Agent
4. Human Escalation
5. Basic Admin Dashboard
