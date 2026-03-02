"""Dashboard metrics API endpoints."""

import datetime as dt

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.dashboard import (
    ChannelStatsSchema,
    DailyTrendSchema,
    IntentCountSchema,
    LeadBreakdownSchema,
    MetricsResponseSchema,
    RoiMetricsSchema,
)
from src.core.database import get_db
from src.core.security import get_current_user
from src.models.conversation import Conversation
from src.models.daily_metric import DailyMetric
from src.models.lead import Lead
from src.models.message import Message

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


@router.get("/metrics", response_model=MetricsResponseSchema)
async def get_metrics(
    period: str = Query(default="7d", pattern="^(today|7d|30d|custom)$"),
    start_date: dt.date | None = None,
    end_date: dt.date | None = None,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    tenant_id = user.get("tenant_id")

    # Determine date range
    today = dt.date.today()
    if period == "today":
        date_from = today
        date_to = today
    elif period == "7d":
        date_from = today - dt.timedelta(days=7)
        date_to = today
    elif period == "30d":
        date_from = today - dt.timedelta(days=30)
        date_to = today
    else:
        date_from = start_date or today - dt.timedelta(days=7)
        date_to = end_date or today

    # Aggregate metrics from daily_metrics table
    metrics_result = await db.execute(
        select(DailyMetric)
        .where(DailyMetric.tenant_id == tenant_id)
        .where(DailyMetric.date.between(date_from, date_to))
        .order_by(DailyMetric.date)
    )
    daily_metrics = list(metrics_result.scalars().all())

    total_consultations = sum(m.total_consultations for m in daily_metrics)
    leads_generated = sum(m.leads_generated for m in daily_metrics)
    total_escalations = sum(m.escalations for m in daily_metrics)

    avg_times = [m.avg_response_time_ms for m in daily_metrics if m.avg_response_time_ms]
    avg_response_time = int(sum(avg_times) / len(avg_times)) if avg_times else None

    satisfaction_scores = [float(m.satisfaction_avg) for m in daily_metrics if m.satisfaction_avg]
    satisfaction = sum(satisfaction_scores) / len(satisfaction_scores) if satisfaction_scores else None

    escalation_rate = total_escalations / total_consultations if total_consultations > 0 else 0.0
    conversion_rate = leads_generated / total_consultations if total_consultations > 0 else 0.0

    # Daily trend
    daily_trend = [
        DailyTrendSchema(date=m.date, consultations=m.total_consultations, leads=m.leads_generated)
        for m in daily_metrics
    ]

    # Top intents (aggregate from daily metrics)
    intent_counts: dict[str, int] = {}
    for m in daily_metrics:
        if m.top_intents:
            for item in m.top_intents if isinstance(m.top_intents, list) else []:
                intent = item.get("intent", "unknown")
                intent_counts[intent] = intent_counts.get(intent, 0) + item.get("count", 0)

    total_intent_count = sum(intent_counts.values()) or 1
    top_intents = [
        IntentCountSchema(intent=k, count=v, percentage=round(v / total_intent_count * 100, 1))
        for k, v in sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    ]

    return MetricsResponseSchema(
        total_consultations=total_consultations,
        leads_generated=leads_generated,
        avg_response_time_ms=avg_response_time,
        escalation_rate=round(escalation_rate, 3),
        satisfaction_score=round(satisfaction, 2) if satisfaction else None,
        conversion_rate=round(conversion_rate, 3),
        top_intents=top_intents,
        daily_trend=daily_trend,
    )


# Average SA consultation time in minutes (industry benchmark)
SA_AVG_CONSULTATION_MINUTES = 45
# SA hourly rate in rubles
SA_HOURLY_RATE = 5000


@router.get("/roi", response_model=RoiMetricsSchema)
async def get_roi_metrics(
    period: str = Query(default="30d", pattern="^(7d|30d|90d)$"),
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """ROI analytics: SA hours saved, pipeline value, lead conversion."""
    tenant_id = user.get("tenant_id")

    today = dt.date.today()
    days = {"7d": 7, "30d": 30, "90d": 90}[period]
    date_from = today - dt.timedelta(days=days)

    # --- Conversations stats ---
    conv_result = await db.execute(
        select(
            func.count(Conversation.id).label("total"),
            Conversation.channel,
        )
        .where(Conversation.tenant_id == tenant_id)
        .where(func.date(Conversation.created_at) >= date_from)
        .group_by(Conversation.channel)
    )
    channel_rows = conv_result.all()
    total_consultations = sum(r.total for r in channel_rows)

    # Escalated conversations
    escalated_result = await db.execute(
        select(func.count(Conversation.id))
        .where(Conversation.tenant_id == tenant_id)
        .where(func.date(Conversation.created_at) >= date_from)
        .where(Conversation.status == "escalated")
    )
    escalated_count = escalated_result.scalar() or 0
    ai_handled = total_consultations - escalated_count

    # SA time savings
    sa_hours_saved = round(ai_handled * SA_AVG_CONSULTATION_MINUTES / 60, 1)
    sa_cost_saved = round(sa_hours_saved * SA_HOURLY_RATE, 2)

    # --- Lead stats ---
    lead_result = await db.execute(
        select(
            Lead.qualification,
            func.count(Lead.id).label("count"),
            func.coalesce(func.sum(Lead.estimated_deal_value), 0).label("total_value"),
        )
        .where(Lead.tenant_id == tenant_id)
        .where(func.date(Lead.created_at) >= date_from)
        .group_by(Lead.qualification)
    )
    lead_rows = lead_result.all()

    total_leads = sum(r.count for r in lead_rows)
    qualified_leads = sum(r.count for r in lead_rows if r.qualification in ("hot", "qualified"))
    pipeline_value = float(sum(r.total_value for r in lead_rows if r.qualification in ("hot", "qualified")))

    # Average deal value
    avg_deal_result = await db.execute(
        select(func.avg(Lead.estimated_deal_value))
        .where(Lead.tenant_id == tenant_id)
        .where(func.date(Lead.created_at) >= date_from)
        .where(Lead.estimated_deal_value.isnot(None))
    )
    avg_deal_value_raw = avg_deal_result.scalar()
    avg_deal_value = round(float(avg_deal_value_raw), 2) if avg_deal_value_raw else None

    conversion_rate = total_leads / total_consultations if total_consultations > 0 else 0.0

    # Lead breakdown
    lead_breakdown = [
        LeadBreakdownSchema(
            qualification=r.qualification, count=r.count, total_value=float(r.total_value)
        )
        for r in lead_rows
    ]

    # --- Channel stats ---
    # Get leads per channel via join
    channel_lead_result = await db.execute(
        select(
            Conversation.channel,
            func.count(Lead.id).label("leads"),
        )
        .outerjoin(Lead, Lead.conversation_id == Conversation.id)
        .where(Conversation.tenant_id == tenant_id)
        .where(func.date(Conversation.created_at) >= date_from)
        .group_by(Conversation.channel)
    )
    channel_lead_rows = {r.channel: r.leads for r in channel_lead_result.all()}

    channel_stats = []
    for r in channel_rows:
        leads = channel_lead_rows.get(r.channel, 0)
        channel_stats.append(
            ChannelStatsSchema(
                channel=r.channel,
                consultations=r.total,
                leads=leads,
                conversion_rate=round(leads / r.total, 3) if r.total > 0 else 0.0,
            )
        )

    # --- Daily trend ---
    daily_result = await db.execute(
        select(DailyMetric)
        .where(DailyMetric.tenant_id == tenant_id)
        .where(DailyMetric.date.between(date_from, today))
        .order_by(DailyMetric.date)
    )
    daily_metrics = list(daily_result.scalars().all())
    daily_trend = [
        DailyTrendSchema(date=m.date, consultations=m.total_consultations, leads=m.leads_generated)
        for m in daily_metrics
    ]

    return RoiMetricsSchema(
        total_consultations=total_consultations,
        total_leads=total_leads,
        qualified_leads=qualified_leads,
        pipeline_value=pipeline_value,
        avg_deal_value=avg_deal_value,
        conversion_rate=round(conversion_rate, 3),
        ai_handled=ai_handled,
        escalated_to_sa=escalated_count,
        sa_hours_saved=sa_hours_saved,
        sa_cost_saved=sa_cost_saved,
        lead_breakdown=lead_breakdown,
        channel_stats=channel_stats,
        daily_trend=daily_trend,
    )
