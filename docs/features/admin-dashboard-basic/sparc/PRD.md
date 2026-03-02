# PRD: Admin Dashboard (Basic)

## User Story

As a **Cloud Sales Director**, I need a web-based admin dashboard to monitor
real-time consultation metrics, browse conversation history, review generated
leads, and view ROI analytics so I can track pipeline health and AI performance.

Ref: US-010 (Consultation Metrics) in `docs/Specification.md`.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: Admin Dashboard Basic

  Scenario: Login and view dashboard
    Given a Sales Director opens the admin URL
    When they enter valid email and password
    Then they are redirected to the Dashboard page
    And they see metric cards: consultations, leads, avg response time, escalation rate
    And a 7-day daily trend line chart (consultations + leads)
    And a top intents bar chart

  Scenario: Switch metric period
    Given the user is on the Dashboard page
    When they click "Today", "7 days", or "30 days"
    Then the metric cards and charts refresh for that period

  Scenario: Browse conversations
    Given the user navigates to the Conversations page
    Then they see a paginated table with ID, channel, status, intent, created date
    And they can page through results (20 per page)

  Scenario: View leads
    Given the user navigates to the Leads page
    Then they see a table with contact, company, qualification, intent, est. value, date
    And qualification badges are color-coded (cold/warm/hot/qualified)

  Scenario: ROI analytics
    Given the user navigates to the ROI Analytics page
    Then they see SA hours saved, pipeline value, conversion rate, avg deal value
    And AI vs SA handling pie chart, lead funnel bar chart, channel stats, daily trend

  Scenario: Unauthorized access
    Given the user has no valid JWT token
    When they attempt to access any dashboard route
    Then they are redirected to the Login page

  Scenario: API failure
    Given the backend API is unreachable
    When the dashboard attempts to load metrics
    Then a red error banner is displayed with the error message
```

## File Inventory (13 TSX/TS files)

| File | Purpose |
|------|---------|
| `admin/src/main.tsx` | React root, BrowserRouter |
| `admin/src/App.tsx` | Route definitions, auth gate |
| `admin/src/pages/LoginPage.tsx` | Email/password login form |
| `admin/src/pages/DashboardPage.tsx` | Metric cards + Recharts |
| `admin/src/pages/ConversationsPage.tsx` | Paginated conversation table |
| `admin/src/pages/LeadsPage.tsx` | Paginated leads table |
| `admin/src/pages/RoiAnalyticsPage.tsx` | ROI metrics + charts |
| `admin/src/components/Layout.tsx` | Sidebar nav + main content |
| `admin/src/components/MetricCard.tsx` | Reusable metric card |
| `admin/src/hooks/useAuth.ts` | JWT auth state + login/logout |
| `admin/src/hooks/useDashboard.ts` | Dashboard metrics fetcher |
| `admin/src/api/client.ts` | API client (fetch + token) |
| `admin/src/types/index.ts` | TypeScript interfaces |

## Phase Tracking

- [x] Phase 1: PLAN -- SPARC docs created, 13 TSX/TS files
- [x] Phase 2: VALIDATE — code matches SPARC docs
- [x] Phase 3: IMPLEMENT — 138 tests passing, lint clean
- [x] Phase 4: REVIEW — 22 ruff issues fixed, all clean
