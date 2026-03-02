"""Tenant model — multi-tenant support."""

from datetime import datetime

from sqlalchemy import String, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[str] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    config: Mapped[dict] = mapped_column(JSONB, server_default=text("'{}'::jsonb"))
    api_key_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    plan: Mapped[str] = mapped_column(String(50), server_default="pilot")
    created_at: Mapped[datetime] = mapped_column(server_default=text("NOW()"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("NOW()"), onupdate=text("NOW()"))

    conversations: Mapped[list["Conversation"]] = relationship(back_populates="tenant")
    leads: Mapped[list["Lead"]] = relationship(back_populates="tenant")
    agent_configs: Mapped[list["AgentConfig"]] = relationship(back_populates="tenant")
    daily_metrics: Mapped[list["DailyMetric"]] = relationship(back_populates="tenant")


# Avoid circular imports — these are resolved at runtime
from src.models.conversation import Conversation  # noqa: E402, F401
from src.models.lead import Lead  # noqa: E402, F401
from src.models.agent_config import AgentConfig  # noqa: E402, F401
from src.models.daily_metric import DailyMetric  # noqa: E402, F401
