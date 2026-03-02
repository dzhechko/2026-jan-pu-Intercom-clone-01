# Architecture -- ROI Analytics

## Data Flow

```
RoiAnalyticsPage.tsx
  |  GET /api/v1/dashboard/roi?period=30d
  v
FastAPI router (dashboard.py)
  |  get_roi_metrics()
  |--- query Conversation (group by channel, filter escalated)
  |--- query Lead (group by qualification, sum deal values)
  |--- join Conversation+Lead (channel lead counts)
  |--- query DailyMetric (daily trend)
  v
RoiMetricsSchema (JSON response)
  |
  v
Recharts (PieChart, BarChart, LineChart) + MetricCard components
```

## Component Responsibilities

| Component                  | Responsibility                           |
|----------------------------|------------------------------------------|
| `RoiAnalyticsPage.tsx`     | Period selector, layout, charts, cards   |
| `MetricCard`               | Reusable KPI card with trend indicator   |
| `api.getRoiMetrics()`      | HTTP client call to `/api/v1/dashboard/roi` |
| `get_roi_metrics()`        | DB aggregation, formula application      |
| `RoiMetricsSchema`         | Response serialization and validation    |
| `Conversation` model       | Source for consultation + channel counts |
| `Lead` model               | Source for qualification + deal values   |
| `DailyMetric` model        | Pre-aggregated daily stats for trends    |

## Database Queries (in endpoint handler)

1. **Channel consultations** -- `SELECT channel, COUNT(id) FROM conversation WHERE tenant_id = ? AND created_at >= ? GROUP BY channel`
2. **Escalated count** -- `SELECT COUNT(id) FROM conversation WHERE status = 'escalated' AND ...`
3. **Lead breakdown** -- `SELECT qualification, COUNT(id), SUM(estimated_deal_value) FROM lead WHERE ... GROUP BY qualification`
4. **Average deal value** -- `SELECT AVG(estimated_deal_value) FROM lead WHERE estimated_deal_value IS NOT NULL AND ...`
5. **Channel leads** -- `SELECT channel, COUNT(lead.id) FROM conversation LEFT JOIN lead ON ... GROUP BY channel`
6. **Daily trend** -- `SELECT * FROM daily_metric WHERE date BETWEEN ? AND ? ORDER BY date`

## Security

- JWT-protected endpoint via `get_current_user` dependency.
- `tenant_id` extracted from token; all queries scoped to tenant.
- Period parameter validated by regex `^(7d|30d|90d)$`.

## ADR: Pre-aggregated DailyMetric Table

The daily trend uses `DailyMetric` (pre-aggregated by a scheduled job) instead of
real-time `GROUP BY date` on conversations. This avoids slow full-table scans on
large tenants and keeps the `/roi` endpoint response under 500ms.
