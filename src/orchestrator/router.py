"""Orchestrator — routes user messages to the appropriate agent."""

import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.base import get_agent_definition
from src.agents.executor import AgentExecutor, AgentResponse
from src.core.logging import get_logger
from src.models.conversation import Conversation
from src.models.message import Message
from src.orchestrator.intent import detect_intent, select_agent_type
from src.rag.search import RAGSearch

logger = get_logger(__name__)


class Orchestrator:
    """Main orchestrator — intent detection, agent selection, RAG search, LLM call."""

    def __init__(self, db: AsyncSession, tenant_id: str):
        self.db = db
        self.tenant_id = tenant_id
        self.rag = RAGSearch()
        self.executor = AgentExecutor()

    async def process_message(self, conversation: Conversation, user_message: str) -> AgentResponse:
        start_time = time.time()

        # 1. Save user message
        user_msg = Message(
            conversation_id=conversation.id,
            role="user",
            content=user_message,
        )
        self.db.add(user_msg)
        await self.db.flush()

        # 2. Detect intent
        intent = detect_intent(user_message, conversation.context)
        conversation.context = {**conversation.context, "detected_intent": intent}

        # 3. Select agent
        agent_type = select_agent_type(intent)
        agent = get_agent_definition(agent_type)

        # 4. RAG search
        rag_collections = agent.rag_collections or [f"{self.tenant_id}_cloud_docs"]
        try:
            rag_result = await self.rag.search(
                query=user_message,
                collections=rag_collections,
                tenant_id=self.tenant_id,
                top_k=5,
            )
        except Exception:
            logger.exception("rag_search_failed")
            rag_result = None

        # 5. Build conversation history
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at)
        )
        history_messages = result.scalars().all()
        conversation_history = [{"role": m.role, "content": m.content} for m in history_messages]

        # 6. Execute agent
        rag_docs = rag_result.documents if rag_result else []
        response = await self.executor.execute(
            agent=agent,
            user_message=user_message,
            conversation_history=conversation_history,
            rag_documents=rag_docs,
        )

        # 7. Save assistant response
        elapsed_ms = int((time.time() - start_time) * 1000)
        assistant_msg = Message(
            conversation_id=conversation.id,
            role="assistant",
            agent_type=response.agent_type,
            content=response.content,
            metadata_={
                "confidence": response.confidence,
                "sources": response.sources,
                "response_time_ms": elapsed_ms,
            },
        )
        self.db.add(assistant_msg)

        # 8. Handle escalation
        if response.should_escalate:
            conversation.status = "escalated"
            logger.info(
                "escalation_triggered",
                conversation_id=conversation.id,
                agent_type=agent_type,
                confidence=response.confidence,
            )

        await self.db.flush()

        logger.info(
            "message_processed",
            conversation_id=conversation.id,
            agent_type=agent_type,
            intent=intent,
            confidence=response.confidence,
            response_time_ms=elapsed_ms,
        )

        return response
