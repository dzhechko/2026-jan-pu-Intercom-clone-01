"""Agent execution — call LLM with agent context and RAG results."""

from dataclasses import dataclass, field

import anthropic

from src.agents.base import AgentDefinition
from src.core.config import settings
from src.core.logging import get_logger
from src.rag.search import RAGDocument

logger = get_logger(__name__)

MAX_MESSAGE_LENGTH = 4000


@dataclass
class AgentResponse:
    content: str
    confidence: float
    agent_type: str
    sources: list[dict] = field(default_factory=list)
    should_escalate: bool = False


class AgentExecutor:
    """Execute an agent by calling the LLM with system prompt, RAG context, and conversation history."""

    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    async def execute(
        self,
        agent: AgentDefinition,
        user_message: str,
        conversation_history: list[dict],
        rag_documents: list[RAGDocument],
    ) -> AgentResponse:
        # Truncate long messages
        if len(user_message) > MAX_MESSAGE_LENGTH:
            user_message = user_message[:MAX_MESSAGE_LENGTH]
            truncation_notice = "\n\n[Сообщение было сокращено до 4000 символов]"
        else:
            truncation_notice = ""

        # Build system prompt with RAG context
        system_prompt = self._build_system_prompt(agent, rag_documents)

        # Build messages
        messages = self._build_messages(conversation_history, user_message + truncation_notice)

        try:
            response = await self.client.messages.create(
                model=settings.llm_model,
                max_tokens=4096,
                system=system_prompt,
                messages=messages,
            )

            content = response.content[0].text if response.content else ""
            confidence = self._estimate_confidence(rag_documents, content)

            sources = [
                {"title": doc.title, "url": doc.metadata.get("source_url", "")}
                for doc in rag_documents
                if doc.title
            ]

            should_escalate = confidence < agent.confidence_threshold

            return AgentResponse(
                content=content,
                confidence=confidence,
                agent_type=agent.agent_type,
                sources=sources,
                should_escalate=should_escalate,
            )

        except anthropic.APITimeoutError:
            logger.error("llm_timeout", agent_type=agent.agent_type)
            # Retry once
            try:
                response = await self.client.messages.create(
                    model=settings.llm_fallback_model or settings.llm_model,
                    max_tokens=4096,
                    system=system_prompt,
                    messages=messages,
                )
                content = response.content[0].text if response.content else ""
                return AgentResponse(
                    content=content,
                    confidence=0.5,
                    agent_type=agent.agent_type,
                    sources=[],
                    should_escalate=False,
                )
            except Exception:
                logger.exception("llm_retry_failed", agent_type=agent.agent_type)
                return AgentResponse(
                    content="Извините, сервис временно недоступен. Попробуйте через минуту.",
                    confidence=0.0,
                    agent_type=agent.agent_type,
                    should_escalate=True,
                )

        except Exception:
            logger.exception("llm_call_failed", agent_type=agent.agent_type)
            return AgentResponse(
                content="Произошла ошибка при обработке запроса. Пожалуйста, попробуйте ещё раз.",
                confidence=0.0,
                agent_type=agent.agent_type,
                should_escalate=True,
            )

    @staticmethod
    def _build_system_prompt(agent: AgentDefinition, rag_documents: list[RAGDocument]) -> str:
        prompt = agent.system_prompt

        if rag_documents:
            context_parts = []
            for i, doc in enumerate(rag_documents, 1):
                context_parts.append(f"[Источник {i}: {doc.title}]\n{doc.content}")

            rag_context = "\n\n---\n\n".join(context_parts)
            prompt += f"\n\n## Контекст из базы знаний\n\n{rag_context}"

        return prompt

    @staticmethod
    def _build_messages(conversation_history: list[dict], user_message: str) -> list[dict]:
        # Take last 20 messages from history
        recent_history = conversation_history[-20:] if len(conversation_history) > 20 else conversation_history

        messages = []
        for msg in recent_history:
            role = "user" if msg.get("role") == "user" else "assistant"
            messages.append({"role": role, "content": msg.get("content", "")})

        messages.append({"role": "user", "content": user_message})
        return messages

    @staticmethod
    def _estimate_confidence(rag_documents: list[RAGDocument], response: str) -> float:
        if not rag_documents:
            return 0.4

        avg_score = sum(d.score for d in rag_documents) / len(rag_documents)

        # Higher confidence if RAG scores are good and response references sources
        has_references = any(doc.title.lower() in response.lower() for doc in rag_documents if doc.title)
        reference_bonus = 0.1 if has_references else 0.0

        # Base confidence from RAG relevance
        confidence = min(1.0, avg_score * 0.8 + reference_bonus + 0.2)

        return round(confidence, 2)
