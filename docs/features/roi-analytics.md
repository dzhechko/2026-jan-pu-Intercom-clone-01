# Feature: ROI Analytics Dashboard

**Pipeline:** /feature (score: +2, range -1 to +4)
**Sprint:** v1.0
**Depends on:** admin-dashboard-basic, lead-qualification

## User Story

As a sales manager, I want to see ROI metrics for the AI consultant (SA hours saved, pipeline value, conversion rates), so that I can demonstrate business impact to stakeholders.

### Acceptance Criteria (Gherkin)

```gherkin
Scenario: View ROI metrics
  Given an admin is logged into the dashboard
  When they navigate to the ROI Analytics page
  Then they see SA hours saved and cost savings
  And pipeline value from qualified leads
  And conversion rate (leads/consultations)
  And average deal value

Scenario: AI vs SA comparison
  Given the ROI page is loaded
  Then a pie chart shows AI-handled vs escalated consultations
  And the percentage of AI-handled consultations is displayed

Scenario: Lead funnel visualization
  Given leads exist in the system
  Then a bar chart shows lead counts by qualification (cold/warm/hot/qualified)
  And each bar is color-coded

Scenario: Channel performance
  Given conversations exist across channels (telegram, web_widget)
  Then channel stats show consultations, leads, and conversion rate per channel

Scenario: Period filtering
  Given the admin selects a period (7d, 30d, 90d)
  Then all metrics refresh for the selected timeframe
```

## Architecture References

### Data Sources
- `Conversation` model — total consultations, escalation status, channel
- `Lead` model — qualification, estimated_deal_value, contact info
- `DailyMetric` model — aggregated daily metrics for trend charts

### Cost Model
- SA hourly rate: 5,000 ₽/h (Russian SA market benchmark)
- Average consultation: 45 minutes
- Formula: `sa_hours_saved = ai_handled × 45/60`
- Formula: `sa_cost_saved = sa_hours_saved × 5000`

## Complexity Scoring

| Signal | Score | Notes |
|--------|-------|-------|
| Touches 4-10 files | 0 | 8 files (backend schema, route, frontend page, types, etc.) |
| New API endpoint | +1 | GET /api/v1/dashboard/roi |
| New frontend page with charts | +1 | RoiAnalyticsPage with Recharts |
| Uses existing DB models | 0 | No new tables |
| Estimated 1-2 hours | +1 | Backend + frontend |
| **Total** | **+2** | **/feature pipeline** |

## Implementation Plan

### Files to Create/Modify
1. `src/api/schemas/dashboard.py` — MODIFY: Add RoiMetricsSchema, LeadBreakdownSchema, ChannelStatsSchema
2. `src/api/routes/dashboard.py` — MODIFY: Add GET /api/v1/dashboard/roi endpoint
3. `admin/src/pages/RoiAnalyticsPage.tsx` — NEW: ROI page with charts
4. `admin/src/App.tsx` — MODIFY: Add /roi route
5. `admin/src/components/Layout.tsx` — MODIFY: Add nav item
6. `admin/src/api/client.ts` — MODIFY: Add getRoiMetrics call
7. `admin/src/types/index.ts` — MODIFY: Add IRoiMetrics
8. `tests/unit/test_roi_analytics.py` — NEW: 12 tests

### Tests Required
1. Schema validation tests (RoiMetricsSchema, LeadBreakdownSchema, ChannelStatsSchema)
2. SA savings calculation tests (formulas, edge cases)
3. Conversion rate calculation tests

### Edge Cases
- Zero consultations → all rates = 0, hours = 0
- No leads in period → pipeline = 0, avg deal = None
- NULL deal values → avg ignores NULLs
- Channel with no leads → conversion = 0

## Phase Tracking

- [x] Phase 1: PLAN — this document
- [x] Phase 2: VALIDATE — requirements score 95/100 (fixed: IRoiMetrics type duplication removed)
- [x] Phase 3: IMPLEMENT — 12 tests passing, TypeScript clean
- [x] Phase 4: REVIEW — 2 fixes: unused Message import removed, duplicate type replaced with import
