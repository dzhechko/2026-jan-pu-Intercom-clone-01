"""Pydantic schemas for conversations API."""

from datetime import datetime

from pydantic import BaseModel, Field


class ConversationCreateSchema(BaseModel):
    channel: str = Field(pattern="^(telegram|web_widget|crm)$")
    channel_user_id: str
    initial_message: str | None = None


class ConversationResponseSchema(BaseModel):
    id: str
    status: str
    channel: str
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageCreateSchema(BaseModel):
    content: str = Field(max_length=10000)
    role: str = Field(default="user", pattern="^user$")


class SourceSchema(BaseModel):
    title: str
    url: str = ""


class MessageResponseSchema(BaseModel):
    id: str
    content: str
    role: str
    agent_type: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class AssistantResponseSchema(BaseModel):
    id: str
    content: str
    agent_type: str | None = None
    confidence: float = 0.0
    sources: list[SourceSchema] = []
    created_at: datetime


class SendMessageResponseSchema(BaseModel):
    user_message: MessageResponseSchema
    assistant_response: AssistantResponseSchema
    response_time_ms: int
