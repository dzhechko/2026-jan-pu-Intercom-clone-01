---
description: Bootstrap entire AI-Консультант Cloud.ru project from documentation.
  Generates monorepo skeleton, all packages, Docker configs, database schema,
  core modules, and basic tests.
  $ARGUMENTS: optional flags --skip-tests, --skip-seed, --dry-run
---

# /start $ARGUMENTS

## Purpose

One-command project generation from documentation → working monorepo with `docker compose up`.

## Prerequisites

- Documentation in `docs/` directory (SPARC output)
- CC toolkit in project root (CLAUDE.md, .claude/)
- Python 3.12+, Node.js 18+ (for admin dashboard)
- Docker + Docker Compose installed
- Git initialized

## Process

### Phase 1: Foundation (sequential — everything depends on this)

1. **Read all project docs** to build full context:
   - `docs/Architecture.md` → monorepo structure, Docker Compose, tech stack
   - `docs/Specification.md` → data model, API endpoints, NFRs
   - `docs/Pseudocode.md` → core algorithms, business logic
   - `docs/Completion.md` → env config, deployment setup
   - `docs/PRD.md` → features, user personas (for README)
   - `docs/Refinement.md` → edge cases, testing strategy

2. **Generate root configs:**
   - `pyproject.toml` with dependencies (fastapi, sqlalchemy, qdrant-client, anthropic, python-telegram-bot, redis, mcp, pydantic)
   - `requirements.txt` + `requirements-dev.txt` (pytest, ruff, bandit, locust)
   - `docker-compose.yml` with services: api, admin, postgres, qdrant, redis, minio, nginx
   - `Dockerfile` (Python 3.12-slim, multi-stage build)
   - `.env.example` with all required environment variables
   - `.gitignore` (Python + Node + Docker + .env)

3. **Git commit:** `chore: project root configuration`

### Phase 2: Packages (parallel via Task tool)

Launch 4 parallel tasks:

#### Task A: src/ — Backend core
Read and use as source:
- `docs/Architecture.md` → component structure, database schema
- `docs/Specification.md` → data model → SQLAlchemy models
- `docs/Pseudocode.md` → algorithms → service implementations

Generate:
- `src/models/` — SQLAlchemy models (conversations, messages, leads, tenants, agent_configs, daily_metrics)
- `src/api/routes/` — FastAPI endpoints (conversations, messages, dashboard, webhooks)
- `src/api/schemas/` — Pydantic request/response models
- `src/core/` — config, database, security, logging
- `src/orchestrator/` — intent detection, agent routing, confidence scoring
- `src/services/` — lead qualification, TCO calculation, escalation

**Commits:** `feat: SQLAlchemy models`, `feat: API endpoints`, `feat: orchestrator`

#### Task B: src/rag/ — RAG Pipeline
Read and use as source:
- `docs/Pseudocode.md` → RAG search algorithm, embedding, RRF merge
- `docs/Architecture.md` → Qdrant integration

Generate:
- `src/rag/embedder.py` — document embedding
- `src/rag/search.py` — hybrid search (vector + BM25 + RRF)
- `src/rag/indexer.py` — document indexing

**Commits:** `feat: RAG pipeline with hybrid search`

#### Task C: prompts/ + corpus/ — Agent configs
Read and use as source:
- `docs/Specification.md` → agent capabilities, user stories
- `docs/Architecture.md` → agent types and responsibilities

Generate:
- `prompts/architect.md`, `cost_calculator.md`, `compliance.md`, `human_escalation.md`
- `corpus/` directory structure with .gitkeep files

**Commits:** `feat: agent system prompts`

#### Task D: admin/ — React Dashboard
Read and use as source:
- `docs/Specification.md` → dashboard requirements
- `docs/Architecture.md` → frontend stack (React 18, TypeScript, Tailwind, Recharts)

Generate:
- `admin/package.json`, `admin/tsconfig.json`, `admin/vite.config.ts`
- `admin/src/App.tsx`, `admin/src/main.tsx`
- `admin/src/pages/`, `admin/src/components/`, `admin/src/api/`

**Commits:** `feat: admin dashboard scaffold`

### Phase 3: Integration (sequential)

1. **Verify cross-package imports** (shared modules used correctly)
2. **Docker build:** `docker compose build`
3. **Start services:** `docker compose up -d`
4. **Database setup:**
   - `alembic upgrade head` (run migrations)
   - `python scripts/seed_data.py` (seed initial data)
   - `python scripts/index_documents.py` (index RAG corpus)
5. **Health check:** `curl -f http://localhost:8000/health`
6. **Run tests:** `pytest tests/unit/ -v`
7. **Git commit:** `chore: verify docker integration`

### Phase 4: Finalize

1. Generate/update `README.md` with quick start instructions
2. Configure Nginx (TLS, rate limiting, reverse proxy)
3. Add structured logging (JSON format)
4. Final git tag: `git tag v0.1.0-scaffold`
5. Report summary: files generated, services running, what needs manual attention

## Flags

- `--skip-tests` — skip test file generation (faster, not recommended)
- `--skip-seed` — skip database seeding
- `--dry-run` — show plan without executing

## Error Recovery

If a task fails mid-generation:
- All completed phases are committed to git
- Re-run `/start` — it detects existing files and skips completed phases
- Or fix the issue manually and continue

## Swarm Agents Used

| Phase | Agents | Parallelism |
|-------|--------|-------------|
| Phase 1 | Main | Sequential |
| Phase 2 | 4 Task tools | Parallel |
| Phase 3 | Main | Sequential |
| Phase 4 | Main | Sequential |

## Priority Order

Implement "Must" requirements first (see `docs/Specification.md` Feature Matrix):
1. Architect Agent + RAG Pipeline + Telegram Bot (core loop)
2. Cost Calculator Agent + TCO Algorithm
3. Compliance Agent
4. Human Escalation
5. Basic Admin Dashboard

## CRITICAL: Read Docs, Don't Hallucinate

Each Phase 2 Task MUST read actual docs from `docs/` directory.
Never generate code from LLM memory — always reference specific
documents and sections.
