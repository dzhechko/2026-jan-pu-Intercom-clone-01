---
name: testing-patterns
description: >
  Testing patterns and strategies for AI-Consultant Cloud.ru.
  Extracted from Refinement.md edge cases and testing strategy.
  Use when writing tests, designing test architecture, or reviewing test coverage.
---

# Testing Patterns — AI-Consultant Cloud.ru

## Test Architecture

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

## Fixture Patterns

### Factory Pattern (preferred over raw dicts)
```python
@pytest.fixture
def sample_conversation(db_session, tenant):
    return ConversationFactory(tenant_id=tenant.id, channel="telegram")

@pytest.fixture
def sample_message(sample_conversation):
    return MessageFactory(conversation_id=sample_conversation.id, role="user", content="test")
```

### Parametrize for Edge Cases
```python
@pytest.mark.parametrize("input_msg,expected", [
    ("", "friendly_prompt"),           # Edge case: empty message
    (" \n\t ", "friendly_prompt"),     # Edge case: whitespace only
    ("x" * 10000, "truncated"),        # Edge case: exceeds 4000 char limit
    ("нормальный запрос", "response"), # Happy path: normal Russian text
])
def test_message_handling(input_msg, expected): ...
```

## Mock Patterns

### LLM API Mock
```python
@pytest.fixture
def mock_llm():
    with patch("src.services.llm_client.call_claude") as mock:
        mock.return_value = LLMResponse(content="test response", confidence=0.85)
        yield mock
```

### Telegram Webhook Mock
```python
@pytest.fixture
def telegram_update():
    return {
        "update_id": 123456,
        "message": {
            "message_id": 1,
            "chat": {"id": 12345, "type": "private"},
            "text": "/start",
            "from": {"id": 12345, "is_bot": False, "first_name": "Test"}
        }
    }
```

### RAG Search Mock
```python
@pytest.fixture
def mock_rag_search():
    with patch("src.rag.search.hybrid_search") as mock:
        mock.return_value = [
            SearchResult(content="Cloud.ru GPU pricing...", score=0.92),
            SearchResult(content="Cloud.ru compliance...", score=0.85),
        ]
        yield mock
```

## Edge Cases to Test

### Orchestrator
- Empty message → friendly re-prompt
- Message in wrong language → detect and respond appropriately
- Ambiguous intent → ask clarifying question
- Confidence < 0.6 → trigger human escalation
- Multiple intents in one message → handle primary, note secondary

### RAG Pipeline
- No relevant documents found → honest "I don't know"
- All documents below relevance threshold → escalate
- Duplicate documents in results → deduplicate via RRF
- Very long query → truncate before embedding

### TCO Calculator
- Missing pricing data → state limitation, don't hallucinate
- Negative values → reject with validation error
- Zero resources → return zero cost (valid edge case)
- Currency conversion not available → show in rubles only

### Multi-Tenant Isolation
- Query without tenant_id → reject at middleware
- Tenant A cannot access Tenant B data → enforce in all queries
- Deleted tenant data → soft delete, exclude from queries

## Running Tests

```bash
# All tests
pytest tests/ -v --cov=src --cov-report=term-missing

# Unit only (fast, <10s)
pytest tests/unit/ -v

# Integration (requires docker compose up)
pytest tests/integration/ -v

# With coverage threshold
pytest tests/ --cov=src --cov-fail-under=80

# Specific module
pytest tests/unit/test_orchestrator.py -v

# Skip slow tests
pytest tests/ -m "not slow" -v
```
