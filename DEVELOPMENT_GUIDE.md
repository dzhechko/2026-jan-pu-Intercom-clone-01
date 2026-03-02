# Development Guide — AI-Консультант Cloud.ru

## Quick Start

```bash
# 1. Clone and setup
git clone <repo-url>
cd ai-consultant-cloudru

# 2. Copy environment config
cp .env.example .env
# Edit .env with your API keys

# 3. Start services
docker compose up -d

# 4. Run migrations
docker compose exec api alembic upgrade head

# 5. Seed initial data
docker compose exec api python scripts/seed_data.py

# 6. Index RAG documents
docker compose exec api python scripts/index_documents.py

# 7. Verify
curl http://localhost:8000/health/ready
```

## Development Workflow

### Feature Lifecycle

```
1. /plan [feature]     → Create implementation plan
2. /feature [feature]  → Full lifecycle: plan → implement → test → review → commit
3. /test               → Run tests
4. /deploy staging     → Deploy to staging
```

### Daily Workflow

```bash
# Start services
docker compose up -d

# Run in watch mode (auto-reload)
docker compose up api --watch

# Run tests
pytest tests/unit/ -v

# Lint
ruff check . && ruff format .

# Security scan
bandit -r src/ -ll
```

## Project Structure

```
├── src/                    # Backend application
│   ├── api/                # FastAPI routes + schemas
│   ├── orchestrator/       # Intent detection + agent routing
│   ├── agents/             # Agent execution engine
│   ├── rag/                # RAG pipeline (search, embed, index)
│   ├── models/             # SQLAlchemy models
│   ├── services/           # Business logic
│   ├── mcp/                # MCP server implementations
│   └── core/               # Config, auth, logging
├── admin/                  # React admin dashboard
├── prompts/                # Agent config files (*.md)
├── scripts/                # Seed data, indexing, utilities
├── tests/                  # Test suite
│   ├── unit/               # Fast, isolated tests
│   ├── integration/        # Requires Docker services
│   └── e2e/                # Full user journeys
├── docs/                   # SPARC documentation
│   ├── PRD.md              # Product Requirements
│   ├── Specification.md    # Acceptance criteria
│   ├── Pseudocode.md       # Algorithms + API contracts
│   ├── Architecture.md     # System design
│   ├── Refinement.md       # Edge cases + testing
│   └── features/           # Feature implementation plans
├── docker-compose.yml      # Service orchestration
├── Dockerfile              # Multi-stage build
└── CLAUDE.md               # AI assistant context
```

## Key Patterns

### 1. Multi-Tenant Isolation

Every database query MUST filter by `tenant_id`:

```python
# CORRECT
result = await db.execute(
    select(Conversation)
    .where(Conversation.tenant_id == tenant.id)
    .where(Conversation.id == conversation_id)
)

# WRONG — data leak risk
result = await db.execute(
    select(Conversation).where(Conversation.id == conversation_id)
)
```

### 2. Agent Configuration

Agents are defined as Markdown config files, not code:

```
prompts/
├── architect.md           # Architecture recommendations
├── cost_calculator.md     # TCO calculations
├── compliance.md          # Regulatory guidance
├── migration.md           # Migration planning
├── ai_factory.md          # GPU/ML workloads
└── human_escalation.md    # Handoff to human SA
```

### 3. RAG Pipeline

```
User Query → Embed → Vector Search (Qdrant) ─┐
                   → BM25 Search (PostgreSQL) ─┼── RRF Merge → Rerank → Top-K → Agent
                                                └── Metadata Filter (tenant, freshness)
```

### 4. Error Handling

Use error codes from `docs/Pseudocode.md`:
- `AGENT_*` — Agent processing errors
- `RAG_*` — Search/retrieval errors
- `AUTH_*` — Authentication/authorization errors
- `RATE_*` — Rate limiting errors
- `VALIDATION_*` — Input validation errors

## Testing

```bash
# Unit tests (fast, no Docker needed)
pytest tests/unit/ -v

# Integration tests (requires docker compose up)
pytest tests/integration/ -v

# Full suite with coverage
pytest tests/ -v --cov=src --cov-report=term-missing --cov-fail-under=80

# Specific test
pytest tests/unit/test_orchestrator.py::test_intent_detection -v
```

## Deployment

```bash
# Staging
/deploy staging

# Production (with backup)
/deploy production

# Rollback
/deploy rollback
```

## Available Claude Code Commands

| Command | Description |
|---------|-------------|
| `/start` | Bootstrap project from documentation |
| `/feature [name]` | Full feature lifecycle |
| `/plan [feature]` | Create implementation plan |
| `/test [scope]` | Run/generate tests |
| `/deploy [env]` | Deploy to environment |
| `/myinsights` | Capture development insights |

## Recommended Implementation Order

Based on PRD MVP priorities:

1. **Database models + migrations** — Foundation for all features
2. **RAG Pipeline** — Core search infrastructure
3. **Orchestrator + Architect Agent** — Primary consultation flow
4. **Telegram Bot** — First channel delivery
5. **Cost Calculator Agent** — TCO comparisons
6. **Compliance Agent** — Regulatory guidance
7. **Human Escalation** — SA handoff flow
8. **Admin Dashboard** — Metrics and management
9. **Lead Qualification** — CRM integration
10. **Web Chat Widget** — Second channel
