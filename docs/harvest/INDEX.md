# Toolkit Index

Last harvest: 2026-03-02
Source: ai-consultant-cloud-ru
Total artifacts: 34

## Patterns

| Pattern | Maturity | Version | Description |
|---------|----------|---------|-------------|
| [Hybrid RAG Search with RRF](patterns/hybrid-rag-search-rrf.md) | 🔴 Alpha | v1.0 | Vector + keyword search merged via Reciprocal Rank Fusion |
| [Multi-Agent Orchestrator](patterns/multi-agent-orchestrator.md) | 🔴 Alpha | v1.0 | Intent → route → enrich → execute → escalate pipeline |
| [Confidence-Triggered Escalation](patterns/confidence-triggered-escalation.md) | 🔴 Alpha | v1.0 | Auto-handoff to human when AI confidence < threshold |
| [Multi-Tenant Data Isolation](patterns/multi-tenant-data-isolation.md) | 🔴 Alpha | v1.0 | tenant_id on all tables, enforced via middleware |
| [Agent-as-Config](patterns/agent-as-config.md) | 🔴 Alpha | v1.0 | Agents defined by prompt files, not code |
| [LLM Fallback & Retry](patterns/llm-fallback-retry.md) | 🔴 Alpha | v1.0 | Primary model → fallback model → graceful degradation |
| [Non-Blocking Side Effects](patterns/non-blocking-side-effects.md) | 🔴 Alpha | v1.0 | Try-catch wrapped side effects that don't block user flow |

## Commands

| Command | Maturity | Version | Description |
|---------|----------|---------|-------------|
| [/myinsights](commands/myinsights.md) | 🔴 Alpha | v1.0 | Capture development learnings with error signature matching |
| [/review](commands/review.md) | 🔴 Alpha | v1.0 | Multi-agent code review with automated checks |
| [/deploy](commands/deploy.md) | 🔴 Alpha | v1.0 | Docker Compose deployment with rollback |
| [/go](commands/go-pipeline-router.md) | 🔴 Alpha | v1.0 | Complexity scoring → pipeline selection |
| [/run](commands/run-autonomous-loop.md) | 🔴 Alpha | v1.0 | Autonomous feature build loop with error recovery |

## Rules

| Rule | Maturity | Version | Description |
|------|----------|---------|-------------|
| [Checklists > Prose](rules/checklists-over-prose.md) | 🔴 Alpha | v1.0 | LLMs follow checklists more reliably than narrative instructions |
| [Mandatory Phase Artifacts](rules/mandatory-phase-artifacts.md) | 🔴 Alpha | v1.0 | Every workflow phase must produce verifiable outputs |
| [Judge-Generator Separation](rules/judge-generator-separation.md) | 🔴 Alpha | v1.0 | Never use same model for both generation and evaluation |
| [Layer-Based Model Escalation](rules/layer-based-model-escalation.md) | 🔴 Alpha | v1.0 | Cheapest model first, escalate only when insufficient |
| [Optimization Convergence Gate](rules/optimization-convergence-gate.md) | 🔴 Alpha | v1.0 | Stop when improvement delta < 0.5 for 3 iterations |
| [Scoring Boundary Examples](rules/scoring-boundary-examples.md) | 🔴 Alpha | v1.0 | Always include concrete examples at decision boundaries |
| [Mandatory Review Phase](rules/mandatory-review-phase.md) | 🔴 Alpha | v1.0 | Optional review = skipped review; make it mandatory |
| [Pipeline Decisions Logging](rules/pipeline-decisions-must-be-logged.md) | 🔴 Alpha | v1.0 | Log all routing decisions before execution |
| [Retroactive Docs via Agents](rules/retroactive-docs-via-parallel-agents.md) | 🔴 Alpha | v1.0 | Parallel agents can generate docs from existing code |

## Templates

| Template | Maturity | Version | Description |
|----------|----------|---------|-------------|
| [Docker Compose Multi-Service](templates/docker-compose-multi-service.md) | 🔴 Alpha | v1.0 | 7-service stack: API, frontend, DB, cache, vector, storage, proxy |
| [Python Dockerfile Multi-Stage](templates/python-dockerfile-multistage.md) | 🔴 Alpha | v1.0 | Builder + runtime with non-root user and health check |
| [Nginx Reverse Proxy](templates/nginx-reverse-proxy.md) | 🔴 Alpha | v1.0 | Rate limiting, security headers, upstream routing, SSL-ready |
| [.env.example](templates/env-example-multi-service.md) | 🔴 Alpha | v1.0 | Environment vars organized by service domain |
| [pyproject.toml](templates/pyproject-toml-python.md) | 🔴 Alpha | v1.0 | ruff + pytest + coverage config for Python projects |
| [CLAUDE.md](templates/claude-md-project-context.md) | 🔴 Alpha | v1.0 | AI project context template with all standard sections |

## Snippets

| Snippet | Maturity | Version | Language | Dependencies |
|---------|----------|---------|----------|-------------|
| [RRF Merge](snippets/rrf-merge-python.md) | 🔴 Alpha | v1.0 | Python | None |
| [Text Chunking](snippets/text-chunking-overlap-python.md) | 🔴 Alpha | v1.0 | Python | None |
| [Structlog Setup](snippets/structlog-json-setup-python.md) | 🔴 Alpha | v1.0 | Python | structlog |
| [Async SQLAlchemy Session](snippets/async-sqlalchemy-session-python.md) | 🔴 Alpha | v1.0 | Python | sqlalchemy[asyncpg] |
| [JWT Token](snippets/jwt-token-python.md) | 🔴 Alpha | v1.0 | Python | python-jose |
| [Confidence Estimation](snippets/confidence-estimation-rag-python.md) | 🔴 Alpha | v1.0 | Python | None |
| [Pseudo-Embedding](snippets/pseudo-embedding-python.md) | 🔴 Alpha | v1.0 | Python | None |

## Hooks

_No hooks extracted in this harvest._

## Skills

_No new skills extracted in this harvest (existing skills like BTO already standalone)._
