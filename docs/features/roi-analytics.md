# Feature: ROI Analytics Dashboard

## User Story
As a sales manager, I want to see ROI metrics for the AI consultant (SA hours saved, pipeline value, conversion rates), so that I can demonstrate business impact to stakeholders.

## Complexity Score: +2 (via /feature)
- Touches 4-10 files: 0
- New API endpoint + new frontend page: +2
- Uses existing database models (Lead, Conversation, DailyMetric): 0
- No new database entities: 0
- Estimated 1-2 hours: +1
- **Pipeline: /feature**

## Files Created/Modified
1. `src/api/schemas/dashboard.py` — Added RoiMetricsSchema, LeadBreakdownSchema, ChannelStatsSchema
2. `src/api/routes/dashboard.py` — Added GET /api/v1/dashboard/roi endpoint
3. `admin/src/pages/RoiAnalyticsPage.tsx` — ROI analytics page with charts
4. `admin/src/App.tsx` — Added /roi route
5. `admin/src/components/Layout.tsx` — Added ROI Analytics nav item
6. `admin/src/api/client.ts` — Added getRoiMetrics API call
7. `admin/src/types/index.ts` — Added IRoiMetrics interface
8. `tests/unit/test_roi_analytics.py` — 12 tests (schemas, calculations)

## Architecture Decisions
- **SA cost model**: 5,000 ₽/hour, 45 min avg consultation → hours_saved = ai_handled × 45/60
- **Pipeline value**: sum of estimated_deal_value for hot + qualified leads
- **Channel breakdown**: group by conversation.channel with lead join
- **Period support**: 7d, 30d, 90d (aligned with sales reporting cycles)

## Implementation Steps
1. Define Pydantic schemas: RoiMetricsSchema (core ROI + SA savings + lead breakdown + channel stats)
2. Implement /api/v1/dashboard/roi endpoint:
   - Query conversations by tenant + date range
   - Count AI-handled vs escalated
   - Calculate SA hours saved and cost saved
   - Aggregate leads by qualification
   - Join leads to channels for channel stats
   - Query daily metrics for trend
3. Create RoiAnalyticsPage.tsx:
   - 4 KPI cards: SA Hours Saved, Pipeline Value, Conversion Rate, Avg Deal Value
   - AI vs SA pie chart (Recharts PieChart)
   - Lead funnel bar chart (color-coded by qualification)
   - Channel performance cards
   - Daily trend line chart
   - Cost savings summary banner
4. Add route, nav item, API client method

## Tests
1. `tests/unit/test_roi_analytics.py::TestRoiSchemas` — 4 tests (schema validation)
2. `tests/unit/test_roi_analytics.py::TestSaTimeSavingsCalculation` — 5 tests (formulas)
3. `tests/unit/test_roi_analytics.py::TestConversionCalculations` — 3 tests (rates, pipeline)

## Edge Cases
- Zero consultations: conversion_rate = 0, sa_hours_saved = 0
- No leads in period: pipeline_value = 0, avg_deal_value = None
- Missing deal values: avg ignores NULL values
- Channel without leads: conversion_rate = 0 for that channel

## Dependencies
- Depends on: admin-dashboard-basic, lead-qualification
- Uses: DailyMetric model, Lead model, Conversation model

## Status: DONE
Committed: `feat: ROI analytics dashboard with SA savings and pipeline tracking`
