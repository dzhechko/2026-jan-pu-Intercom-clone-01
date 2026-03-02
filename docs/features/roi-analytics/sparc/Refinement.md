# Refinement -- ROI Analytics

## Edge Cases

### EC-1: Zero Consultations

**Trigger:** New tenant or empty period with no conversations.
**Risk:** Division by zero in `conversion_rate = leads / consultations`.
**Mitigation:** Guard `if total_consultations == 0: return 0.0` (already implemented).
**Test:** `test_conversion_rate_zero_consultations`, `test_roi_metrics_empty`.

### EC-2: Division by Zero in Channel Stats

**Trigger:** A channel row has `total = 0` (possible with deleted conversations).
**Risk:** `leads / row.total` raises `ZeroDivisionError`.
**Mitigation:** Guard `if r.total > 0 else 0.0` in channel stats loop.
**Test:** Add parametrized test with `consultations=0` per channel.

### EC-3: Large Date Ranges (90d+)

**Trigger:** Tenant with high volume selects 90-day period.
**Risk:** Slow DB queries on `conversation` and `lead` tables.
**Mitigation:**
- Daily trend uses pre-aggregated `DailyMetric` table (no full scan).
- Add composite index on `(tenant_id, created_at)` for `conversation` and `lead`.
- Consider caching the `/roi` response in Redis with 5-minute TTL for 90d queries.

### EC-4: Missing or Null Deal Values

**Trigger:** Leads created without `estimated_deal_value`.
**Risk:** `AVG()` returns `None`; `SUM()` includes nulls incorrectly.
**Mitigation:**
- `func.coalesce(func.sum(...), 0)` for pipeline totals (implemented).
- `avg_deal_value` returns `None` when no non-null values exist (schema allows `float | None`).
- Frontend displays "N/A" when `avg_deal_value` is null.

### EC-5: No Lead Breakdown Data

**Trigger:** Period has consultations but zero leads.
**Risk:** Empty `lead_breakdown` array renders blank chart.
**Mitigation:** Frontend bar chart renders empty; no crash. Consider showing
"No leads generated yet" placeholder text.

### EC-6: Channel Without Leads (Outer Join)

**Trigger:** Channel has conversations but the `LEFT JOIN` to `lead` returns 0.
**Risk:** `channel_lead_map` missing the channel key.
**Mitigation:** `channel_lead_map.get(r.channel, 0)` defaults to 0 (implemented).

### EC-7: Concurrent Period Switches

**Trigger:** User clicks period buttons rapidly.
**Risk:** Stale response from a slow request overwrites a newer response.
**Mitigation:** The `useEffect` cleanup or an `AbortController` should cancel
in-flight requests. Currently not implemented -- add `AbortController` to
`api.getRoiMetrics()`.

## Testing Gaps

| Gap                              | Priority | Type        |
|----------------------------------|----------|-------------|
| Integration test for `/roi` endpoint | High     | Integration |
| Channel with zero consultations  | Medium   | Unit        |
| 90d query performance benchmark  | Medium   | Performance |
| AbortController for rapid switching | Low    | Frontend    |
| Multi-tenant isolation assertion | High     | Integration |

## Recommended Indexes

```sql
CREATE INDEX ix_conversation_tenant_created ON conversation(tenant_id, created_at);
CREATE INDEX ix_lead_tenant_created ON lead(tenant_id, created_at);
CREATE INDEX ix_daily_metric_tenant_date ON daily_metric(tenant_id, date);
```
