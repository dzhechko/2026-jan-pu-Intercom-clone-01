# Module 4: Business & Finance — AI-Консультант Cloud.ru

## A. Revenue Model

| План | Цена | Включено |
|------|------|----------|
| Pilot | ₽0 (3 мес) | 1 канал, 3 агента, 200 консультаций/мес |
| Production | ₽500К/мес | Все каналы, 6 агентов, безлимит, CRM, аналитика |
| Enterprise | ₽1-2М/мес | White-label, on-premise, custom training, SLA |

Additional streams: per-lead bonus (₽3-5К), success fee, partner API.

## B. Unit Economics

| Метрика | Значение | Benchmark |
|---------|----------|-----------|
| ARPU | ₽500К-1М/мес | — |
| CAC | ₽500К-1М | $5K-50K B2B Enterprise |
| LTV | ₽36М (3yr, 15% churn) | — |
| LTV:CAC | **36:1 — 72:1** | >5:1 отлично |
| Payback | **1-2 мес** | <12 мес хорошо |
| Gross Margin | **85-90%** | 72% median |
| Monthly Churn | ~1-2% | 1-2% Enterprise |
| NRR | 120%+ | 110% median |

### COGS per client/month
- LLM API: ₽50-80К (10-16%)
- Infrastructure: ₽20-30К (4-6%)
- Support (0.2 FTE): ₽30К (6%)
- **Total COGS: ₽100-140К (20-28%)**
- **Gross Profit: ₽360-400К (72-80%)**

## C. P&L Projection (24 months)

### Assumptions

| Параметр | Значение | Тип |
|----------|----------|-----|
| Pilot start | Month 1 | [F]act |
| Pilot → Production conversion | 80% | [H]ypothesis |
| Second client | Month 6 | [H] |
| Avg MRR/client | ₽600К | [B]enchmark |
| Team (start) | 3 people | [F] |
| Team (Y2) | 8 people | [H] |

### Monthly Model

| Месяц | Клиенты | MRR | Расходы/мес | EBITDA |
|-------|---------|-----|-------------|--------|
| 1-3 | 1 (pilot free) | 0 | 1.2М | -3.6М |
| 4-6 | 1 (production) | 500К | 1.5М | -3.0М |
| 7-9 | 2 | 1.1М | 1.8М | -2.1М |
| 10-12 | 3 | 1.8М | 2.2М | -1.2М |
| **Y1** | **3** | — | — | **-9.9М** |
| 13-15 | 4 | 2.4М | 2.8М | -1.2М |
| 16-18 | 5 | 3.2М | 3.2М | **0 (BE)** |
| 19-21 | 7 | 4.5М | 3.5М | +3.0М |
| 22-24 | 10 | 6.5М | 4.0М | +7.5М |
| **Y2** | **10** | — | — | **+9.3М** |

**ARR end of Y2: ~₽78М**

## D. Resolved Contradictions (TRIZ)

| Противоречие | Решение |
|-------------|---------|
| Low CAC vs Enterprise clients | Free pilot 3mo → product sells itself |
| High price vs Small market (15 providers) | Per-lead + white-label for SI → expand TAM |
| Small team vs Enterprise-ready | MCP: agents = config, not code. 1 engineer/week per new client |

## E. Funding Roadmap

| Stage | Amount | Goal | Timing |
|-------|--------|------|--------|
| Bootstrap | ₽0 | MVP + pilot | M1-6 |
| Pre-seed | ₽5-10М | Team 5 + 2nd client | M6 |
| Seed | ₽30-50М | 10 clients + white-label | M12-15 |
| Series A | ₽150-300М | CIS + verticals | M24+ |

Alternative: Cloud.ru as strategic investor.

## F. Break-Even Scenarios

| Scenario | Clients | MRR | Break-Even |
|----------|---------|-----|------------|
| Optimistic | 4 × ₽700К | ₽2.8М | Month 12 |
| Realistic | 5 × ₽600К | ₽3.0М | Month 16 |
| Pessimistic | 7 × ₽500К | ₽3.5М | Month 20 |

## G. Sensitivity Analysis

| Change | Impact | Risk |
|--------|--------|------|
| CAC +50% | +2 months | 🟡 Medium |
| Churn +3% | +4 months | 🟡 Medium |
| ARPU -30% | +6 months | 🟠 High |
| Pilot conversion -50% | +8 months | 🔴 Critical |
| LLM costs +100% | +1 month | 🟢 Low |

**Key risk:** Pilot → Production conversion. Mitigation: free 3mo pilot + ROI dashboard.

## H. Key Financial Sources

- B2B SaaS benchmarks — [Industry benchmarks reference](https://www.index.dev/blog/ai-agents-statistics)
- AI SDR pricing ($500-$5,000/mo) — [JoinValley](https://www.joinvalley.co/blog/ai-sdr-pricing-costs-roi-2026)
- AI SDR cost per lead: $39 (AI) vs $262 (human) — [SalesTools.io](https://salestools.io/en/blog/ai-sdr-tools-comparison-2025)
- Cloud.ru revenue ₽49.4B — [Interfax](https://www.interfax.ru/business/1039559)
- Russian cloud market ₽416.5B — [CNews](https://www.cnews.ru/reviews/oblachnye_servisy_2025)
