# Template: CLAUDE.md Project Context File

## Maturity: Alpha v1.0
## Extracted: 2026-03-02
## Version: v1.0

---

## Description

Template for a `CLAUDE.md` file that provides project context to AI coding assistants. Includes sections for project description, architecture overview, directory structure, key design decisions, coding standards, available commands, and documentation references. This file lives at the project root and is read automatically by Claude Code and similar tools.

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `{{PROJECT_NAME}}` | Human-readable project name | `My Platform` |
| `{{PROJECT_DESCRIPTION}}` | 1-2 sentence project summary | `SaaS platform for...` |
| `{{ARCHITECTURE_PATTERN}}` | High-level architecture pattern | `Distributed Monolith (Monorepo)` |
| `{{DEPLOY_TARGET}}` | Where the application is deployed | `Docker Compose on VPS` |
| `{{BACKEND_STACK}}` | Backend technology list | `Python 3.12, FastAPI, SQLAlchemy 2.0` |
| `{{FRONTEND_STACK}}` | Frontend technology list | `React 18, TypeScript, Tailwind CSS` |
| `{{DATA_STACK}}` | Data stores and caches | `PostgreSQL 16, Redis 7, Qdrant` |
| `{{INFRA_STACK}}` | Infrastructure components | `Nginx, Docker 25+, Docker Compose` |
| `{{COMMANDS_TABLE}}` | Markdown table of available slash commands | see template |
| `{{DESIGN_DECISIONS}}` | Numbered list of key ADRs | see template |
| `{{DIRECTORY_TREE}}` | ASCII directory structure | see template |

## Template

````markdown
# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

## Architecture

- **Pattern:** {{ARCHITECTURE_PATTERN}}
- **Deploy:** {{DEPLOY_TARGET}}
- **Backend:** {{BACKEND_STACK}}
- **Frontend:** {{FRONTEND_STACK}}
- **Data:** {{DATA_STACK}}
- **Infra:** {{INFRA_STACK}}

## Project Structure

```
{{DIRECTORY_TREE}}
```

## Key Design Decisions

{{DESIGN_DECISIONS}}

## Coding Standards

- Python: ruff for linting + formatting, type hints required, async/await for I/O
- SQL: SQLAlchemy ORM only (no raw SQL), Alembic for migrations
- API: Pydantic v2 models for all request/response schemas
- Tests: pytest + pytest-asyncio, 80%+ coverage for core modules
- Frontend: TypeScript strict mode, functional components, Tailwind utility classes

## Available Commands

{{COMMANDS_TABLE}}

## Parallel Execution Strategy

- Use `Task` tool for independent subtasks (e.g., parallel test runs)
- Run tests, linting, type-checking in parallel
- For complex features: spawn specialized agents (planner, code-reviewer, architect)

## Documentation

Read before implementing:
1. `docs/Specification.md` -- User stories and acceptance criteria
2. `docs/Pseudocode.md` -- Algorithms and API contracts
3. `docs/Architecture.md` -- System design and ADRs
4. `docs/Refinement.md` -- Edge cases and testing strategy
5. `docs/Completion.md` -- Deployment and CI/CD
````

## Usage

1. Copy the template content into a `CLAUDE.md` file at your project root.
2. Replace all `{{PLACEHOLDER}}` values with your project-specific information.
3. Customize the "Coding Standards" section to match your actual tooling choices.
4. Update the "Documentation" section to reference your actual documentation files.
5. Commit `CLAUDE.md` to version control so all team members and AI assistants share the same context.

## Example: Filled Parameters

For reference, here is how some parameters might look when filled in:

**`{{DESIGN_DECISIONS}}`:**
```
1. **Config-driven modules** -- each module is defined by a configuration file, not custom code. Adding a new module means creating a config file.
2. **Hybrid search** -- vector similarity + BM25 keyword search + Reciprocal Rank Fusion for best retrieval quality.
3. **Multi-tenant isolation** -- `tenant_id` column on all data tables. Queries always filter by tenant.
4. **Confidence scoring** -- below a configurable threshold, requests escalate to human review.
```

**`{{COMMANDS_TABLE}}`:**
```
| Command | Description |
|---------|-------------|
| `/start` | Bootstrap project from documentation |
| `/feature [name]` | Full feature lifecycle (plan, implement, test, review) |
| `/test [scope]` | Generate and run tests |
| `/deploy [env]` | Deploy to environment |
```

**`{{DIRECTORY_TREE}}`:**
```
+-- src/
|   +-- api/           # FastAPI routes, webhooks, middleware
|   +-- models/        # SQLAlchemy models
|   +-- services/      # Business logic
|   +-- utils/         # Shared utilities
|   +-- config/        # Settings, environment
+-- frontend/          # React frontend
+-- tests/             # pytest tests
+-- docs/              # Project documentation
+-- docker-compose.yml
+-- Dockerfile
+-- .env.example
```

## Notes

- The `CLAUDE.md` file is the single most important file for AI-assisted development. It is read at the start of every session and shapes how the AI understands your project.
- Keep it concise. Aim for 50-100 lines. AI assistants have limited context windows; a bloated CLAUDE.md wastes tokens on every interaction.
- The "Key Design Decisions" section is especially valuable. It prevents the AI from proposing architectures that contradict decisions already made.
- Update this file whenever the architecture or conventions change. Stale context leads to stale suggestions.
- The "Available Commands" table documents slash commands that the AI assistant can execute. Not all projects need this section.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |
