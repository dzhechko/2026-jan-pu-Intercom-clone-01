"""Pydantic schemas for authentication."""

from pydantic import BaseModel, Field


class LoginSchema(BaseModel):
    email: str
    password: str = Field(min_length=8)


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class AgentConfigUpdateSchema(BaseModel):
    system_prompt: str | None = None
    confidence_threshold: float | None = Field(default=None, ge=0.0, le=1.0)
    max_turns: int | None = Field(default=None, ge=1, le=100)
    rag_collections: list[str] | None = None
    tools: list[str] | None = None
