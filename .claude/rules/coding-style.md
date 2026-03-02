# Coding Style Rules — AI-Консультант Cloud.ru

## Python (Backend)

### General
- Python 3.12+ (use modern syntax: `match/case`, `type` statements, `|` for unions)
- Async/await for all I/O operations (DB, HTTP, Redis, Qdrant)
- Type hints on all function signatures
- Google-style docstrings for public functions

### Framework Patterns
- **FastAPI** routes in `src/api/routes/` — thin handlers, delegate to services
- **Pydantic v2** models for all API schemas (request/response)
- **SQLAlchemy 2.0** async style — mapped_column, async_session
- **Alembic** for all schema migrations — never modify DB manually

### Project Conventions
- Agents are config files (`prompts/*.md`), NOT Python code
- Multi-tenant: every DB query must filter by `tenant_id`
- Error codes follow the strategy in `docs/Pseudocode.md`
- Environment config via `pydantic-settings` (BaseSettings class)

### Naming
- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Pydantic schemas: `{Entity}{Action}Schema` (e.g., `MessageCreateSchema`)
- SQLAlchemy models: singular noun (e.g., `Conversation`, `Message`)

### Linting
- `ruff` for linting and formatting (replaces black + isort + flake8)
- Line length: 120 characters
- Import sorting: isort-compatible via ruff

## TypeScript/React (Admin Dashboard)

### General
- TypeScript strict mode
- Functional components with hooks
- Tailwind CSS for styling (no CSS modules)

### Naming
- Files: `PascalCase.tsx` for components, `camelCase.ts` for utilities
- Components: `PascalCase`
- Hooks: `use{Name}`
- Types/interfaces: `PascalCase` with `I` prefix for interfaces

### Patterns
- React Query for server state
- Zustand for client state (minimal)
- Chart.js or Recharts for dashboard visualizations

## Testing

- `pytest` with `pytest-asyncio` for async tests
- Fixtures in `conftest.py` (shared across test modules)
- Factory pattern for test data (not raw dicts)
- Mock external services (LLM, Telegram API, Cloud.ru API)
- Coverage target: 80% overall, 90% for orchestrator/RAG

## Docker

- Multi-stage builds (builder + runtime)
- Python 3.12-slim as base image
- Non-root user in container
- Health check endpoints in every service
