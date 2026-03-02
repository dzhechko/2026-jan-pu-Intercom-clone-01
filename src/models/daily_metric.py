"""Daily metrics model — aggregated consultation analytics."""

import datetime as dt
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Integer, Numeric, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class DailyMetric(Base):
    __tablename__ = "daily_metrics"
    __table_args__ = (UniqueConstraint("tenant_id", "date"),)

    id: Mapped[str] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    tenant_id: Mapped[str] = mapped_column(UUID, ForeignKey("tenants.id"), nullable=False)
    date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    total_consultations: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    avg_response_time_ms: Mapped[int | None] = mapped_column(Integer)
    leads_generated: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    escalations: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    satisfaction_avg: Mapped[Decimal | None] = mapped_column(Numeric(3, 2))
    top_intents: Mapped[dict | None] = mapped_column(JSONB)

    tenant: Mapped["Tenant"] = relationship(back_populates="daily_metrics")


from src.models.tenant import Tenant  # noqa: E402, F401
