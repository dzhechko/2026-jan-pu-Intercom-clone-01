"""Unit tests for ROI analytics schemas and calculations."""


from src.api.routes.dashboard import SA_AVG_CONSULTATION_MINUTES, SA_HOURLY_RATE
from src.api.schemas.dashboard import (
    ChannelStatsSchema,
    LeadBreakdownSchema,
    RoiMetricsSchema,
)


class TestRoiSchemas:
    """Test ROI analytics Pydantic schemas."""

    def test_lead_breakdown_schema(self):
        schema = LeadBreakdownSchema(qualification="hot", count=10, total_value=500000.0)
        assert schema.qualification == "hot"
        assert schema.count == 10
        assert schema.total_value == 500000.0

    def test_channel_stats_schema(self):
        schema = ChannelStatsSchema(
            channel="telegram", consultations=100, leads=15, conversion_rate=0.15
        )
        assert schema.channel == "telegram"
        assert schema.conversion_rate == 0.15

    def test_roi_metrics_full_schema(self):
        schema = RoiMetricsSchema(
            total_consultations=200,
            total_leads=40,
            qualified_leads=12,
            pipeline_value=2400000.0,
            avg_deal_value=200000.0,
            conversion_rate=0.2,
            ai_handled=170,
            escalated_to_sa=30,
            sa_hours_saved=127.5,
            sa_cost_saved=637500.0,
            lead_breakdown=[
                LeadBreakdownSchema(qualification="cold", count=10, total_value=0),
                LeadBreakdownSchema(qualification="warm", count=18, total_value=0),
                LeadBreakdownSchema(qualification="hot", count=8, total_value=1600000),
                LeadBreakdownSchema(qualification="qualified", count=4, total_value=800000),
            ],
            channel_stats=[
                ChannelStatsSchema(channel="telegram", consultations=120, leads=25, conversion_rate=0.208),
                ChannelStatsSchema(channel="web_widget", consultations=80, leads=15, conversion_rate=0.188),
            ],
            daily_trend=[],
        )
        assert schema.total_consultations == 200
        assert schema.pipeline_value == 2400000.0
        assert len(schema.lead_breakdown) == 4
        assert len(schema.channel_stats) == 2

    def test_roi_metrics_empty(self):
        schema = RoiMetricsSchema(
            total_consultations=0,
            total_leads=0,
            qualified_leads=0,
            pipeline_value=0.0,
            avg_deal_value=None,
            conversion_rate=0.0,
            ai_handled=0,
            escalated_to_sa=0,
            sa_hours_saved=0.0,
            sa_cost_saved=0.0,
            lead_breakdown=[],
            channel_stats=[],
            daily_trend=[],
        )
        assert schema.total_consultations == 0
        assert schema.avg_deal_value is None


class TestSaTimeSavingsCalculation:
    """Test SA time savings formulas."""

    def test_sa_constants_reasonable(self):
        assert SA_AVG_CONSULTATION_MINUTES == 45
        assert SA_HOURLY_RATE == 5000

    def test_hours_saved_formula(self):
        ai_handled = 100
        hours_saved = ai_handled * SA_AVG_CONSULTATION_MINUTES / 60
        assert hours_saved == 75.0

    def test_cost_saved_formula(self):
        ai_handled = 100
        hours_saved = ai_handled * SA_AVG_CONSULTATION_MINUTES / 60
        cost_saved = hours_saved * SA_HOURLY_RATE
        assert cost_saved == 375000.0

    def test_zero_handled_zero_savings(self):
        ai_handled = 0
        hours_saved = ai_handled * SA_AVG_CONSULTATION_MINUTES / 60
        cost_saved = hours_saved * SA_HOURLY_RATE
        assert hours_saved == 0.0
        assert cost_saved == 0.0

    def test_large_volume_savings(self):
        ai_handled = 1000
        hours_saved = ai_handled * SA_AVG_CONSULTATION_MINUTES / 60
        cost_saved = hours_saved * SA_HOURLY_RATE
        assert hours_saved == 750.0
        assert cost_saved == 3750000.0


class TestConversionCalculations:
    """Test conversion rate calculations."""

    def test_conversion_rate(self):
        total_consultations = 200
        total_leads = 40
        rate = total_leads / total_consultations
        assert rate == 0.2

    def test_conversion_rate_zero_consultations(self):
        total_consultations = 0
        rate = 0 / 1 if total_consultations == 0 else 0 / total_consultations
        assert rate == 0.0

    def test_pipeline_from_qualified(self):
        lead_values = [
            ("cold", 10, 0),
            ("warm", 18, 0),
            ("hot", 8, 1600000),
            ("qualified", 4, 800000),
        ]
        pipeline = sum(v for q, c, v in lead_values if q in ("hot", "qualified"))
        qualified_count = sum(c for q, c, v in lead_values if q in ("hot", "qualified"))
        assert pipeline == 2400000
        assert qualified_count == 12
