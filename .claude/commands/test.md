# /test $ARGUMENTS — Test Generation & Execution

## Usage

- `/test` — run all tests
- `/test unit` — run unit tests only
- `/test integration` — run integration tests
- `/test e2e` — run end-to-end tests
- `/test generate [feature]` — generate tests for a feature
- `/test coverage` — run with coverage report

## Test Generation

When generating tests for a feature:

1. Read acceptance criteria from `docs/Specification.md`
2. Read BDD scenarios from `docs/test-scenarios.md`
3. Read edge cases from `docs/Refinement.md`
4. Generate pytest test file in `tests/`

### Test Structure

```
tests/
├── unit/
│   ├── test_orchestrator.py      # Intent detection, agent routing
│   ├── test_rag.py               # RAG search, embedding, RRF
│   ├── test_tco.py               # TCO calculation algorithm
│   ├── test_lead_qualification.py # Lead scoring
│   └── test_auth.py              # JWT, API key validation
├── integration/
│   ├── test_api.py               # API endpoint tests
│   ├── test_telegram.py          # Telegram webhook handling
│   ├── test_crm.py               # CRM sync
│   └── test_rag_pipeline.py      # RAG index + query
├── e2e/
│   ├── test_consultation_flow.py # Full consultation E2E
│   ├── test_escalation.py        # Escalation flow E2E
│   └── test_dashboard.py         # Admin dashboard E2E
└── conftest.py                   # Shared fixtures
```

## Execution Commands

```bash
# All tests
pytest tests/ -v --cov=src --cov-report=term-missing

# Unit only
pytest tests/unit/ -v

# Integration (requires Docker services)
pytest tests/integration/ -v

# With coverage threshold
pytest tests/ --cov=src --cov-fail-under=80

# Specific file
pytest tests/unit/test_orchestrator.py -v
```
