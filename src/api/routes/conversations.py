"""Conversation API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.conversation import (
    AssistantResponseSchema,
    ConversationCreateSchema,
    ConversationResponseSchema,
    MessageCreateSchema,
    MessageResponseSchema,
    SendMessageResponseSchema,
    SourceSchema,
)
from src.core.database import get_db
from src.core.security import get_current_tenant
from src.models.conversation import Conversation
from src.models.message import Message
from src.models.tenant import Tenant
from src.orchestrator.router import Orchestrator

router = APIRouter(prefix="/api/v1/conversations", tags=["conversations"])


@router.post("", response_model=ConversationResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    payload: ConversationCreateSchema,
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    conversation = Conversation(
        tenant_id=tenant.id,
        channel=payload.channel,
        channel_user_id=payload.channel_user_id,
    )
    db.add(conversation)
    await db.flush()

    # If initial message provided, process it
    if payload.initial_message:
        orchestrator = Orchestrator(db, tenant.id)
        await orchestrator.process_message(conversation, payload.initial_message)

    await db.flush()
    return conversation


@router.post("/{conversation_id}/messages", response_model=SendMessageResponseSchema)
async def send_message(
    conversation_id: str,
    payload: MessageCreateSchema,
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    # Find conversation (tenant-scoped)
    result = await db.execute(
        select(Conversation)
        .where(Conversation.id == conversation_id)
        .where(Conversation.tenant_id == tenant.id)
    )
    conversation = result.scalar_one_or_none()

    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    if conversation.status not in ("active", "escalated"):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conversation is not active")

    # Process message through orchestrator
    orchestrator = Orchestrator(db, tenant.id)
    response = await orchestrator.process_message(conversation, payload.content)

    # Get the saved messages
    msgs = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(2)
    )
    recent = list(msgs.scalars().all())
    recent.reverse()

    user_msg = recent[0] if recent else None
    assistant_msg = recent[1] if len(recent) > 1 else None

    metadata = assistant_msg.metadata_ if assistant_msg else {}

    return SendMessageResponseSchema(
        user_message=MessageResponseSchema(
            id=user_msg.id if user_msg else "",
            content=payload.content,
            role="user",
            created_at=user_msg.created_at if user_msg else None,
        ),
        assistant_response=AssistantResponseSchema(
            id=assistant_msg.id if assistant_msg else "",
            content=response.content,
            agent_type=response.agent_type,
            confidence=response.confidence,
            sources=[SourceSchema(**s) for s in response.sources],
            created_at=assistant_msg.created_at if assistant_msg else None,
        ),
        response_time_ms=metadata.get("response_time_ms", 0),
    )


@router.get("/{conversation_id}", response_model=ConversationResponseSchema)
async def get_conversation(
    conversation_id: str,
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Conversation)
        .where(Conversation.id == conversation_id)
        .where(Conversation.tenant_id == tenant.id)
    )
    conversation = result.scalar_one_or_none()

    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    return conversation
