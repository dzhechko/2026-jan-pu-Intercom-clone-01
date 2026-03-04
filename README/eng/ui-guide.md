# UI Guide -- Admin Dashboard

## Overview

The admin dashboard is a single-page application built with React 18, TypeScript, and Tailwind CSS. It provides real-time monitoring of AI consultations, lead management, and ROI analytics. Access it at `http://localhost:3000` (development) or via the configured production domain.

---

## Login Page

**URL:** `/login`

The login form requires:

| Field | Description |
|-------|-------------|
| Email | Admin email address (default: `admin@cloud.ru`) |
| Password | Admin password (default dev: `admin123admin`) |

On successful authentication, a JWT token is stored in the browser and all subsequent API requests include it as a Bearer token. The token expires after 60 minutes; the dashboard handles token refresh automatically.

If credentials are invalid, an error message is displayed below the form.

---

## Navigation Sidebar

The left sidebar provides navigation to all dashboard sections:

| Menu Item | Route | Description |
|-----------|-------|-------------|
| Dashboard | `/` | Main metrics overview |
| Conversations | `/conversations` | Conversation list and details |
| Leads | `/leads` | Qualified lead management |
| ROI Analytics | `/roi` | Return on investment metrics |

The sidebar remains visible on all pages and highlights the currently active section.

---

## Dashboard Page

**URL:** `/`

The main dashboard is the landing page after login. It displays aggregated metrics for the selected time period.

### Period Selector

A dropdown or button group at the top of the page lets you choose the reporting period:
- **Today** -- metrics for the current day only
- **7 Days** -- rolling 7-day window (default)
- **30 Days** -- rolling 30-day window

### Metric Cards

Four summary cards are displayed at the top:

| Card | Value | Description |
|------|-------|-------------|
| Total Consultations | Integer | Number of AI-handled conversations in the period |
| Leads Generated | Integer | Qualified leads extracted from conversations |
| Avg Response Time | Milliseconds | Mean time from user message to AI response |
| Escalation Rate | Percentage | Share of conversations escalated to human SA |

Additional metrics may include satisfaction score and conversion rate when data is available.

### Daily Trend Chart

A line chart spanning the selected period with two series:
- **Consultations** (primary line) -- total conversations per day
- **Leads** (secondary line) -- leads generated per day

The X-axis shows dates; the Y-axis shows counts. Hover over data points to see exact values.

### Top Intents Bar Chart

A horizontal bar chart showing the five most frequent user intents:
- Each bar represents an intent category (e.g., "architecture", "cost_estimation", "compliance", "migration", "ai_factory")
- Bar length corresponds to the percentage of total consultations
- Labels show both the intent name and its percentage

---

## Conversations Page

**URL:** `/conversations`

A paginated table displaying all conversations for the current tenant.

### Table Columns

| Column | Description |
|--------|-------------|
| ID | Conversation UUID (clickable for details) |
| Channel | Source channel icon and label: Telegram, Web Widget, or CRM |
| Status | Badge indicating current state: `active` (blue), `completed` (green), `escalated` (orange), `archived` (gray) |
| Intent | Detected primary intent from the conversation context |
| Created At | Timestamp when the conversation started |

### Pagination

- Page size: 20 conversations per page (configurable)
- Page controls at the bottom: Previous / Next buttons with current page indicator
- Total count displayed (e.g., "Showing 1-20 of 347 conversations")

### Status Badge Colors

| Status | Color | Meaning |
|--------|-------|---------|
| Active | Blue | Conversation is ongoing |
| Completed | Green | Conversation ended normally |
| Escalated | Orange | Handed off to human SA |
| Archived | Gray | Closed and archived |

---

## Leads Page

**URL:** `/leads`

A paginated table of qualified leads extracted from conversations.

### Table Columns

| Column | Description |
|--------|-------------|
| Contact | Name, email, and/or phone from the contact JSON object |
| Company | Company name if provided |
| Qualification | Badge: `cold` (gray), `warm` (yellow), `hot` (orange), `qualified` (green) |
| Intent | The primary intent that generated the lead |
| Deal Value | Estimated deal value in rubles (formatted with thousands separator) |
| Created At | When the lead was first identified |

### Qualification Badges

| Qualification | Color | Criteria |
|---------------|-------|----------|
| Cold | Gray | Contact identified but no clear buying signal |
| Warm | Yellow | Budget or timeline mentioned |
| Hot | Orange | Budget + timeline + decision-maker identified |
| Qualified | Green | Meets all BANT criteria, ready for sales handoff |

### Pagination

Same pagination controls as the Conversations page (20 items per page by default).

---

## ROI Analytics Page

**URL:** `/roi`

Detailed return-on-investment analysis for AI-automated consulting.

### Period Selector

Choose the analysis window: **7 Days**, **30 Days** (default), or **90 Days**.

### Summary Cards

| Card | Value | Description |
|------|-------|-------------|
| SA Hours Saved | Decimal (hours) | Time saved by AI handling consultations instead of human SAs |
| SA Cost Saved | Rubles | Monetary savings based on SA hourly rate (5,000 RUB/hour benchmark) |
| Pipeline Value | Rubles | Total estimated deal value from qualified leads |
| Conversion Rate | Percentage | Ratio of leads to total consultations |
| Total Leads | Integer | Number of leads in the period |
| Qualified Leads | Integer | Leads with "hot" or "qualified" status |
| Average Deal Value | Rubles | Mean estimated deal value across all leads |

### AI vs SA Handling

A summary or pie chart showing:
- **AI-Handled:** Number of consultations resolved entirely by AI
- **Escalated to SA:** Number of consultations that required human intervention
- **AI Handling Rate:** Percentage of conversations handled without escalation

### Lead Funnel

A breakdown showing how leads are distributed across qualification stages:

```
Cold    ████████████████████  45
Warm    ██████████████        30
Hot     ████████              18
Qualified ████                 7
```

Each row shows the qualification stage, a proportional bar, and the count.

### Channel Performance

A table comparing performance across communication channels:

| Channel | Consultations | Leads | Conversion Rate |
|---------|--------------|-------|-----------------|
| Telegram | 245 | 28 | 11.4% |
| Web Widget | 89 | 15 | 16.9% |
| CRM | 34 | 7 | 20.6% |

### Daily Trend Chart

Same format as the dashboard trend chart, but for the ROI-specific period (up to 90 days).

---

## Common UI Patterns

### Loading States

All data-fetching operations show a loading spinner or skeleton placeholder while the API request is in progress.

### Error Handling

If an API request fails, an error toast or inline message is displayed with the error description. Network errors prompt a "Retry" button.

### Responsive Design

The dashboard uses Tailwind CSS responsive utilities. The sidebar collapses to a hamburger menu on smaller screens. Tables become scrollable horizontally on mobile viewports.

### Data Refresh

Dashboard metrics are fetched on page load and when the period selector changes. To manually refresh data, use the browser's refresh function or navigate away and back to the page.
