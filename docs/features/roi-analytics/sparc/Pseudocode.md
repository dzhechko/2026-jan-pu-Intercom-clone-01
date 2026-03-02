# Pseudocode -- ROI Analytics

## Constants

```python
SA_AVG_CONSULTATION_MINUTES = 45  # industry benchmark per consultation
SA_HOURLY_RATE = 5000             # rubles per SA hour
```

## calculate_sa_time_saved

```python
def calculate_sa_time_saved(total_consultations: int, escalated_count: int):
    """Return (ai_handled, sa_hours_saved, sa_cost_saved)."""
    ai_handled = total_consultations - escalated_count
    sa_hours_saved = round(ai_handled * SA_AVG_CONSULTATION_MINUTES / 60, 1)
    sa_cost_saved = round(sa_hours_saved * SA_HOURLY_RATE, 2)
    return ai_handled, sa_hours_saved, sa_cost_saved
```

Examples: `(200, 30)` -> `(170, 127.5, 637500.0)` | `(0, 0)` -> `(0, 0.0, 0.0)`

## calculate_conversion_rate

```python
def calculate_conversion_rate(total_consultations: int, total_leads: int) -> float:
    """Return lead conversion rate, 0.0 when no consultations."""
    if total_consultations == 0:
        return 0.0
    return round(total_leads / total_consultations, 3)
```

Examples: `(200, 40)` -> `0.2` | `(0, 0)` -> `0.0` | `(100, 100)` -> `1.0`

## aggregate_channel_stats

```python
def aggregate_channel_stats(channel_rows, channel_lead_map):
    """Build per-channel stats with safe division."""
    result = []
    for row in channel_rows:
        leads = channel_lead_map.get(row.channel, 0)
        rate = round(leads / row.total, 3) if row.total > 0 else 0.0
        result.append(ChannelStatsSchema(
            channel=row.channel, consultations=row.total,
            leads=leads, conversion_rate=rate,
        ))
    return result
```

## aggregate_lead_breakdown

```python
def aggregate_lead_breakdown(lead_rows):
    """Return (total_leads, qualified_leads, pipeline_value, breakdown)."""
    total_leads = sum(r.count for r in lead_rows)
    qualified = ("hot", "qualified")
    qualified_leads = sum(r.count for r in lead_rows if r.qualification in qualified)
    pipeline_value = float(sum(r.total_value for r in lead_rows if r.qualification in qualified))
    breakdown = [
        LeadBreakdownSchema(qualification=r.qualification, count=r.count,
                            total_value=float(r.total_value))
        for r in lead_rows
    ]
    return total_leads, qualified_leads, pipeline_value, breakdown
```

## Frontend: period switching

```typescript
useEffect(() => {
    setLoading(true);
    api.getRoiMetrics(period)
       .then(setMetrics)
       .catch(err => setError(err.message))
       .finally(() => setLoading(false));
}, [period]);
```
