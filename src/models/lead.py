"""Lead model — qualified leads from conversations."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import ARRAY, ForeignKey, Index, Numeric, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Lead(Base):
    __tablename__ = "leads"
    __table_args__ = (
        Index("idx_leads_tenant", "tenant_id"),
        Index("idx_leads_qualification", "qualification"),
    )

    id: Mapped[str] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    tenant_id: Mapped[str] = mapped_column(UUID, ForeignKey("tenants.id"), nullable=False)
    conversation_id: Mapped[str] = mapped_column(UUID, ForeignKey("conversations.id"), nullable=False)
    contact: Mapped[dict] = mapped_column(JSONB, server_default=text("'{}'::jsonb"))
    qualification: Mapped[str] = mapped_column(String(20), server_default="cold")
    intent: Mapped[str | None] = mapped_column(String(30))
    estimated_deal_value: Mapped[Decimal | None] = mapped_column(Numeric(15, 2))
    architecture_summary: Mapped[str | None] = mapped_column(Text)
    tco_data: Mapped[dict | None] = mapped_column(JSONB)
    compliance_requirements: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    crm_external_id: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=text("NOW()"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("NOW()"), onupdate=text("NOW()"))

    tenant: Mapped["Tenant"] = relationship(back_populates="leads")
    conversation: Mapped["Conversation"] = relationship(back_populates="lead")


from src.models.tenant import Tenant  # noqa: E402, F401
from src.models.conversation import Conversation  # noqa: E402, F401
