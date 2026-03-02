"""Agent configuration model — per-tenant agent settings."""

from decimal import Decimal

from sqlalchemy import ARRAY, Boolean, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class AgentConfig(Base):
    __tablename__ = "agent_configs"
    __table_args__ = (UniqueConstraint("tenant_id", "agent_type"),)

    id: Mapped[str] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    tenant_id: Mapped[str] = mapped_column(UUID, ForeignKey("tenants.id"), nullable=False)
    agent_type: Mapped[str] = mapped_column(String(30), nullable=False)
    system_prompt: Mapped[str | None] = mapped_column(Text)
    confidence_threshold: Mapped[Decimal] = mapped_column(Numeric(3, 2), server_default=text("0.6"))
    max_turns: Mapped[int] = mapped_column(Integer, server_default=text("20"))
    rag_collections: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    tools: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    enabled: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))

    tenant: Mapped["Tenant"] = relationship(back_populates="agent_configs")


from src.models.tenant import Tenant  # noqa: E402, F401
