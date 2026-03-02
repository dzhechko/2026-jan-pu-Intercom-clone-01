# Coding Standards Skill — AI-Консультант Cloud.ru

## Tech Stack Patterns

### FastAPI Endpoint Pattern

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.message import MessageCreateSchema, MessageResponseSchema
from src.core.auth import get_current_tenant
from src.core.database import get_db
from src.models.tenant import Tenant
from src.services.conversation import ConversationService

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.post("/{conversation_id}/messages", response_model=MessageResponseSchema)
async def send_message(
    conversation_id: str,
    payload: MessageCreateSchema,
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    service = ConversationService(db, tenant)
    return await service.process_message(conversation_id, payload)
```

### SQLAlchemy Model Pattern

```python
from sqlalchemy import String, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    tenant_id: Mapped[str] = mapped_column(UUID, ForeignKey("tenants.id"), nullable=False, index=True)
    channel: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active")
    context: Mapped[dict] = mapped_column(JSONB, default=dict)

    messages: Mapped[list["Message"]] = relationship(back_populates="conversation")
    tenant: Mapped["Tenant"] = relationship(back_populates="conversations")
```

### Pydantic Schema Pattern

```python
from pydantic import BaseModel, Field
from datetime import datetime

class MessageCreateSchema(BaseModel):
    content: str = Field(max_length=4000, description="User message text")

class MessageResponseSchema(BaseModel):
    id: str
    role: str
    content: str
    agent_type: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    sources: list[dict] = []
    created_at: datetime

    model_config = {"from_attributes": True}
```

### Service Layer Pattern

```python
class ConversationService:
    def __init__(self, db: AsyncSession, tenant: Tenant):
        self.db = db
        self.tenant = tenant

    async def process_message(self, conversation_id: str, payload: MessageCreateSchema):
        # Always filter by tenant_id
        conversation = await self.db.execute(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .where(Conversation.tenant_id == self.tenant.id)
        )
        # ... business logic
```

### Test Pattern

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_llm():
    with patch("src.agents.base.AnthropicClient") as mock:
        mock.return_value.messages.create = AsyncMock(return_value=MockResponse())
        yield mock

@pytest.mark.asyncio
async def test_orchestrator_routes_to_architect(mock_llm, sample_conversation):
    orchestrator = Orchestrator()
    result = await orchestrator.process("Мне нужно мигрировать 200 VMware серверов")
    assert result.agent_type == "architect"
    assert result.confidence >= 0.7
```

### Agent Config Pattern (prompts/*.md)

```markdown
# Agent: Architect

## System Prompt
You are a cloud architecture consultant for {tenant_name}.
You help CTOs design cloud migration strategies.

## Behavior
- Always ask 2-3 clarifying questions before recommending
- Cite specific service names from RAG corpus
- Include resource sizing estimates
- Provide at least 2 source references

## Tools Available
- rag_search: Search documentation corpus
- pricing_api: Get current pricing
- config_api: Get service configurations

## Constraints
- Never hallucinate service names or pricing
- If confidence < 0.6, trigger escalation
- Response must be in user's detected language
```

## File Organization

```
src/
├── api/
│   ├── routes/          # One file per resource
│   ├── schemas/         # Pydantic models
│   ├── middleware/       # Auth, rate limiting, logging
│   └── webhooks/        # Telegram, CRM webhooks
├── orchestrator/
│   ├── router.py        # Intent → Agent routing
│   ├── intent.py        # Intent detection
│   └── context.py       # Conversation context builder
├── agents/
│   ├── base.py          # BaseAgent class
│   ├── executor.py      # Agent execution + MCP tool calls
│   └── loader.py        # Load agent config from prompts/
├── rag/
│   ├── embedder.py      # Text → embeddings
│   ├── search.py        # Hybrid search (vector + BM25)
│   ├── indexer.py        # Document processing + indexing
│   └── reranker.py      # Cross-encoder reranking
├── models/              # SQLAlchemy + Alembic
├── services/            # Business logic layer
├── mcp/                 # MCP server implementations
└── core/                # Config, logging, security
```
