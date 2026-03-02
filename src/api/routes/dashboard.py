"""Dashboard metrics API endpoints."""

import datetime as dt

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.dashboard import DailyTrendSchema, IntentCountSchema, MetricsResponseSchema
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
