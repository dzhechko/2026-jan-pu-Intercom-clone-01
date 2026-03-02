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
