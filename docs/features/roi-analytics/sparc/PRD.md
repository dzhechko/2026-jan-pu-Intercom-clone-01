# PRD -- ROI Analytics

## User Story

```
As a Cloud Sales Director,
I want to see ROI metrics for the AI consultant investment,
So that I can justify the platform cost and track business impact.
```

## Gherkin Acceptance Criteria

```gherkin
Feature: ROI Analytics Dashboard

  Scenario: View SA time savings
    Given 30 days of consultation data exists
    When the Sales Director opens the ROI Analytics page
    Then they see SA hours saved (AI-handled * 45min / 60)
    And cost saved at 5,000 rub/hour rate
    And AI-handled vs escalated breakdown as a pie chart

  Scenario: View consultation-to-lead conversion
    Given consultations and leads exist for the selected period
    When the Sales Director views conversion metrics
    Then they see conversion rate as total_leads / total_consultations
    And qualified lead count and pipeline value
    And average deal value (or "N/A" if no deals)

  Scenario: View channel performance
    Given consultations arrived via Telegram, Web Widget, and CRM
    When the Sales Director views channel stats
    Then each channel shows consultations, leads, and conversion rate
    And an empty state displays when no channel data exists

  Scenario: Switch time period
    Given the page is loaded with 30d default
    When the Sales Director clicks "7 days" or "90 days"
    Then all metrics refresh for the selected period

  Scenario: Zero consultations
    Given no consultations exist for the selected period
    When the Sales Director opens ROI Analytics
    Then all numeric metrics display 0 and rates display 0.0%
    And no division-by-zero errors occur
```

## Files

| Layer    | Path                                       |
|----------|--------------------------------------------|
| API      | `src/api/routes/dashboard.py`              |
| Schemas  | `src/api/schemas/dashboard.py`             |
| Models   | `src/models/conversation.py`, `src/models/lead.py`, `src/models/daily_metric.py` |
| Frontend | `admin/src/pages/RoiAnalyticsPage.tsx`     |
| Tests    | `tests/unit/test_roi_analytics.py`         |

## Phase Tracking

| Phase       | Status   | Notes                                 |
|-------------|----------|---------------------------------------|
| API `/roi`  | Done     | GET `/api/v1/dashboard/roi`           |
| Schemas     | Done     | `RoiMetricsSchema` + sub-schemas      |
| Frontend    | Done     | Recharts page with period selector    |
| Unit tests  | Done     | Schema + formula coverage             |
| Integration | Pending  | DB-backed endpoint tests              |
| E2E         | Pending  | Full page render + period switching   |
