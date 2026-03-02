"""Message model."""

from datetime import datetime

from sqlalchemy import ForeignKey, Index, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (
        Index("idx_messages_conversation", "conversation_id"),
        Index("idx_messages_created", "created_at"),
    )

    id: Mapped[str] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    conversation_id: Mapped[str] = mapped_column(UUID, ForeignKey("conversations.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    agent_type: Mapped[str | None] = mapped_column(String(30))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, server_default=text("'{}'::jsonb"))
    created_at: Mapped[datetime] = mapped_column(server_default=text("NOW()"))

    conversation: Mapped["Conversation"] = relationship(back_populates="messages")


from src.models.conversation import Conversation  # noqa: E402, F401
