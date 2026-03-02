"""Conversation model."""

from datetime import datetime

from sqlalchemy import ForeignKey, Index, String, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Conversation(Base):
    __tablename__ = "conversations"
    __table_args__ = (
        Index("idx_conversations_tenant", "tenant_id"),
        Index("idx_conversations_status", "status"),
        Index("idx_conversations_channel_user", "channel", "channel_user_id"),
    )

    id: Mapped[str] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    tenant_id: Mapped[str] = mapped_column(UUID, ForeignKey("tenants.id"), nullable=False)
    channel: Mapped[str] = mapped_column(String(20), nullable=False)
    channel_user_id: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(20), server_default="active")
    context: Mapped[dict] = mapped_column(JSONB, server_default=text("'{}'::jsonb"))
    created_at: Mapped[datetime] = mapped_column(server_default=text("NOW()"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("NOW()"), onupdate=text("NOW()"))

    tenant: Mapped["Tenant"] = relationship(back_populates="conversations")
    messages: Mapped[list["Message"]] = relationship(back_populates="conversation", order_by="Message.created_at")
    lead: Mapped["Lead | None"] = relationship(back_populates="conversation", uselist=False)


from src.models.lead import Lead  # noqa: E402, F401
from src.models.message import Message  # noqa: E402, F401
from src.models.tenant import Tenant  # noqa: E402, F401
