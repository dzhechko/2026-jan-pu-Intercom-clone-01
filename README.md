# AI-Консультант Cloud.ru

Multi-agent AI platform for pre-sales cloud consulting. Provides instant architecture recommendations, TCO calculations, and compliance guidance for Russian cloud providers.

## Features

- **Architect Agent** — Cloud architecture recommendations with RAG-grounded answers
- **Cost Calculator** — TCO comparison across Russian cloud providers
- **Compliance Agent** — 152-ФЗ, ФСТЭК, КИИ regulatory guidance
- **Multi-Channel** — Telegram bot, web widget, CRM integration
- **Human Escalation** — Automatic handoff to Solution Architects
- **Admin Dashboard** — Metrics, analytics, agent configuration

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, FastAPI |
| Database | PostgreSQL 16 |
| Vector DB | Qdrant |
| Cache | Redis 7 |
| LLM | Claude API (Anthropic) |
| Object Storage | MinIO |
| Admin UI | React, TypeScript, Tailwind CSS |
| Deploy | Docker Compose on VPS |

## Quick Start

```bash
# Clone
git clone <repo-url>
cd ai-consultant-cloudru

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Start all services
docker compose up -d

# Run migrations
docker compose exec api alembic upgrade head

# Verify
curl http://localhost:8000/health
```

## Development

See [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) for full development workflow.

```bash
# Run tests
pytest tests/ -v --cov=src

# Lint
ruff check . && ruff format .

# Security scan
bandit -r src/ -ll
```

## Documentation

| Document | Description |
|----------|-------------|
| [PRD](docs/PRD.md) | Product requirements, user stories |
| [Specification](docs/Specification.md) | Acceptance criteria, NFRs |
| [Architecture](docs/Architecture.md) | System design, tech decisions |
| [Pseudocode](docs/Pseudocode.md) | Algorithms, API contracts |
| [Refinement](docs/Refinement.md) | Edge cases, testing strategy |

## Architecture

```
Telegram/Web/CRM → Nginx → FastAPI → Orchestrator → Agents → RAG + MCP Tools
                                                         ↓
                                              PostgreSQL / Qdrant / Redis
```

## License

Proprietary — Cloud.ru
