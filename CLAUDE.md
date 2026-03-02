# AI-Консультант Cloud.ru

Multi-agent AI platform for automating pre-sales cloud consulting. 6 specialized agents (Architect, Cost Calculator, Compliance, Migration, AI Factory, Human Escalation) via RAG + MCP, delivered through Telegram, web widget, and CRM integrations.

## Architecture

- **Pattern:** Distributed Monolith (Monorepo)
- **Deploy:** Docker Compose on VPS (Moscow, 152-ФЗ compliant)
- **Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0 + Alembic
- **Frontend:** React 18 + TypeScript, Tailwind CSS, shadcn/ui, Recharts
- **AI:** Claude API (primary) + GigaChat (fallback), RAG (Qdrant + hybrid search), MCP tools
- **Data:** PostgreSQL 16, Qdrant (vector DB), Redis 7, MinIO (S3)
- **Infra:** Nginx (TLS), Docker 25+, Docker Compose 2.24+

## Project Structure

```
├── src/
│   ├── api/           # FastAPI routes, webhooks, middleware
│   ├── agents/        # Agent configs (system prompts, tools, RAG collections)
│   ├── orchestrator/  # Intent detection, agent routing, confidence scoring
│   ├── rag/           # RAG pipeline (embedding, search, reranking)
│   ├── mcp/           # MCP tool servers (pricing, compliance, CRM)
│   ├── models/        # SQLAlchemy models (conversations, messages, leads, tenants)
│   ├── services/      # Business logic (lead qualification, TCO calculation, escalation)
│   ├── utils/         # Shared utilities (logging, config, rate limiting)
│   └── config/        # Settings, environment
├── admin/             # React admin dashboard
├── corpus/            # RAG document corpus (Cloud.ru docs, pricing, compliance)
├── prompts/           # Agent system prompts (markdown files)
├── scripts/           # Utility scripts (seed, index, backup, health check)
├── tests/             # pytest tests (unit, integration, e2e)
├── docs/              # SPARC documentation (PRD, Architecture, etc.)
├── docker-compose.yml
├── Dockerfile
└── .env.example
```

## Key Design Decisions

1. **Agents are config, not code** — each agent is defined by a system prompt + MCP tools + RAG collections. Adding a new agent = creating a config file, not writing code.
2. **RAG with hybrid search** — vector (Qdrant) + BM25 + Reciprocal Rank Fusion for best retrieval quality.
3. **MCP for tool access** — standardized protocol for agent-to-API communication. 5 MCP servers.
4. **Multi-tenant** — `tenant_id` on all data. Qdrant collections per tenant.
5. **Confidence scoring** — below 0.6 triggers human escalation automatically.

## Coding Standards

- Python: ruff for linting + formatting, type hints required, async/await for I/O
- SQL: SQLAlchemy ORM only (no raw SQL), Alembic for migrations
- API: Pydantic v2 models for all request/response schemas
- Tests: pytest + pytest-asyncio, 80%+ coverage for core modules
- Frontend: TypeScript strict mode, React functional components, Tailwind utility classes

## Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Bootstrap project from SPARC docs |
| `/feature [name]` | Full feature lifecycle (plan → implement → test → review) |
| `/plan [feature]` | Plan implementation with auto-commit |
| `/test [scope]` | Generate and run tests |
| `/deploy [env]` | Deploy to environment |
| `/myinsights` | Capture development insights |

## Parallel Execution Strategy

- Use `Task` tool for independent subtasks (e.g., parallel test runs)
- Run tests, linting, type-checking in parallel
- For complex features: spawn specialized agents (planner, code-reviewer, architect)

## Documentation

Read before implementing:
1. `docs/Specification.md` — User stories and acceptance criteria
2. `docs/Pseudocode.md` — Algorithms and API contracts
3. `docs/Architecture.md` — System design and ADRs
4. `docs/Refinement.md` — Edge cases and testing strategy
5. `docs/Completion.md` — Deployment and CI/CD
