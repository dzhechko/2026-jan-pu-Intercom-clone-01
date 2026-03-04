"""Pydantic schemas for dashboard metrics API."""

import datetime as dt

from pydantic import BaseModel


class IntentCountSchema(BaseModel):
    intent: str
    count: int
    percentage: float


class DailyTrendSchema(BaseModel):
    date: dt.date
    consultations: int
    leads: int


class MetricsResponseSchema(BaseModel):
    total_consultations: int
    leads_generated: int
    avg_response_time_ms: int | None
    escalation_rate: float
    satisfaction_score: float | None
    conversion_rate: float
    top_intents: list[IntentCountSchema]
    daily_trend: list[DailyTrendSchema]


class LeadBreakdownSchema(BaseModel):
    qualification: str
    count: int
    total_value: float


class ChannelStatsSchema(BaseModel):
    channel: str
    consultations: int
    leads: int
    conversion_rate: float


class ConversationItemSchema(BaseModel):
    id: str
    channel: str
    status: str
    intent: str | None = None
    created_at: dt.datetime | None = None


class PaginatedConversationsSchema(BaseModel):
    items: list[ConversationItemSchema]
    total: int


class LeadItemSchema(BaseModel):
    id: str
    conversation_id: str
    contact: dict = {}
    qualification: str
    intent: str | None = None
    estimated_deal_value: float | None = None
    created_at: dt.datetime | None = None


class PaginatedLeadsSchema(BaseModel):
    items: list[LeadItemSchema]
    total: int


class RoiMetricsSchema(BaseModel):
    # Core ROI
    total_consultations: int
    total_leads: int
    qualified_leads: int
    pipeline_value: float
    avg_deal_value: float | None
    conversion_rate: float

    # SA time savings
    ai_handled: int
    escalated_to_sa: int
    sa_hours_saved: float
    sa_cost_saved: float

    # Lead breakdown
    lead_breakdown: list[LeadBreakdownSchema]

    # Channel performance
    channel_stats: list[ChannelStatsSchema]

    # Daily ROI trend
    daily_trend: list[DailyTrendSchema]
