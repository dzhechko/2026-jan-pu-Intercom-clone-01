# Specification -- ROI Analytics

## Metrics Catalog

### 1. SA Time Saved

| Field            | Type    | Description                                |
|------------------|---------|--------------------------------------------|
| `ai_handled`     | int     | Consultations resolved without escalation  |
| `escalated_to_sa`| int     | Consultations handed off to a human SA     |
| `sa_hours_saved` | float   | `ai_handled * 45 / 60`                    |
| `sa_cost_saved`  | float   | `sa_hours_saved * 5000` (rub)              |

Constants: `SA_AVG_CONSULTATION_MINUTES = 45`, `SA_HOURLY_RATE = 5000`.

### 2. Consultation-to-Lead Conversion

| Field               | Type        | Description                              |
|---------------------|-------------|------------------------------------------|
| `total_consultations`| int        | All conversations in the period          |
| `total_leads`       | int         | Leads created from conversations         |
| `conversion_rate`   | float       | `total_leads / total_consultations`      |
| `avg_deal_value`    | float|null  | Mean `estimated_deal_value` where not null|

### 3. Pipeline Value

| Field             | Type  | Description                                    |
|-------------------|-------|------------------------------------------------|
| `qualified_leads` | int   | Leads with qualification `hot` or `qualified`  |
| `pipeline_value`  | float | Sum of `estimated_deal_value` for qualified    |

### 4. Lead Breakdown

Array of `LeadBreakdownSchema`:

| Field          | Type   | Description                   |
|----------------|--------|-------------------------------|
| `qualification`| string | `cold`, `warm`, `hot`, `qualified` |
| `count`        | int    | Number of leads               |
| `total_value`  | float  | Sum of deal values            |

### 5. Channel Stats

Array of `ChannelStatsSchema`:

| Field            | Type   | Description                          |
|------------------|--------|--------------------------------------|
| `channel`        | string | `telegram`, `web_widget`, `crm`      |
| `consultations`  | int    | Conversations from this channel      |
| `leads`          | int    | Leads generated from this channel    |
| `conversion_rate`| float  | `leads / consultations`              |

## API Contract

```
GET /api/v1/dashboard/roi?period={7d|30d|90d}
Authorization: Bearer <jwt>
Response: RoiMetricsSchema (200)
```

## Period Options

| Value | Days | Default |
|-------|------|---------|
| `7d`  | 7    | No      |
| `30d` | 30   | Yes     |
| `90d` | 90   | No      |

## Frontend Visualizations

| Chart               | Library  | Data Source          |
|----------------------|----------|----------------------|
| AI vs SA donut       | Recharts PieChart  | `ai_handled`, `escalated_to_sa` |
| Lead funnel bar      | Recharts BarChart  | `lead_breakdown`     |
| Daily trend line     | Recharts LineChart | `daily_trend`        |
| Channel performance  | HTML list cards    | `channel_stats`      |
| Cost savings banner  | Tailwind gradient  | `sa_hours_saved`, `sa_cost_saved`, `pipeline_value` |
