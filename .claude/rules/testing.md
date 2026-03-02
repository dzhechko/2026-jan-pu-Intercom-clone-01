# Testing Rules — AI-Консультант Cloud.ru

## Test Structure

```
tests/
├── unit/                          # Fast, isolated, no external deps
│   ├── test_orchestrator.py       # Intent detection, agent routing
│   ├── test_rag.py                # RAG search, embedding, RRF
│   ├── test_tco.py                # TCO calculation algorithm
│   ├── test_lead_qualification.py # Lead scoring
│   └── test_auth.py               # JWT, API key validation
├── integration/                   # Requires Docker services
│   ├── test_api.py                # API endpoint tests
│   ├── test_telegram.py           # Telegram webhook handling
│   ├── test_crm.py                # CRM sync
│   └── test_rag_pipeline.py       # RAG index + query
├── e2e/                           # Full user journeys
│   ├── test_consultation_flow.py  # Full consultation E2E
│   ├── test_escalation.py         # Escalation flow E2E
│   └── test_dashboard.py          # Admin dashboard E2E
└── conftest.py                    # Shared fixtures
```

## Coverage Targets

| Module | Target |
|--------|--------|
| Orchestrator | 90% |
| RAG Pipeline | 85% |
| TCO Calculator | 90% |
| Lead Qualification | 85% |
| Auth Module | 90% |
| Telegram Handler | 80% |
| Overall | 80% |

## Testing Principles

1. **Test behavior, not implementation** — test what the function does, not how
2. **Mock external boundaries** — LLM API, Telegram API, Cloud.ru API
3. **Use fixtures** — shared test data in `conftest.py`
4. **Edge cases from Refinement.md** — every edge case needs a test
5. **BDD scenarios from test-scenarios.md** — map to integration/E2E tests
6. **Fast feedback** — unit tests should run in <10 seconds

## Test Data Patterns

```python
# Use factories, not raw dicts
@pytest.fixture
def sample_conversation(db_session, tenant):
    return ConversationFactory(tenant_id=tenant.id, channel="telegram")

# Use parametrize for edge cases
@pytest.mark.parametrize("input_msg,expected", [
    ("", "friendly_prompt"),           # Edge case #1: empty
    (" \n\t ", "friendly_prompt"),     # Edge case #1: whitespace
    ("x" * 10000, "truncated"),        # Edge case #2: long message
])
def test_message_handling(input_msg, expected): ...
```

## Running Tests

```bash
# All tests
pytest tests/ -v --cov=src --cov-report=term-missing

# Unit only (fast)
pytest tests/unit/ -v

# Integration (requires docker compose up)
pytest tests/integration/ -v

# With coverage threshold
pytest tests/ --cov=src --cov-fail-under=80

# Specific test file
pytest tests/unit/test_orchestrator.py -v

# Run with markers
pytest tests/ -m "not slow" -v
```

## CI Integration

Tests run automatically on every push via GitHub Actions:
1. Unit tests (always)
2. Integration tests (on PR to main)
3. Coverage report uploaded as artifact
4. Fail CI if coverage < 80%
