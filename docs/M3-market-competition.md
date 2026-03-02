# Module 3: Market & Competition — AI-Консультант Cloud.ru

## A. TAM / SAM / SOM

### Top-Down

| Level | Описание | Размер |
|-------|----------|--------|
| **TAM** | Глобальный рынок conversational AI для B2B sales | **$14.79B** (2024) → **$41.39B** (2030) |
| **SAM** | Российский рынок AI для облачного консалтинга | **~₽12.5B** (416.5B облачный рынок × ~3% pre-sales cost) |
| **SOM** | Первые 3-5 облачных провайдеров РФ | **~₽500M-1B** в первые 2 года |

### Bottom-Up

| Расчёт | Данные |
|--------|--------|
| Облачных провайдеров РФ (крупных) | ~10-15 |
| Средний чек платформы | ₽500К-2М/мес |
| ARR на провайдера | ₽6-24М |
| SOM (5 провайдеров × ₽12М avg) | **₽60М ARR** (Y1) |
| SAM (15 провайдеров + партнёры) | **₽270-500М ARR** |

Convergence: Bottom-up SOM (₽60М) = 0.5% от SAM — реалистично для Y1.

### Sources
- Conversational AI market $14.79B — [Fortune Business Insights](https://www.fortunebusinessinsights.com/conversational-ai-market-109850)
- Облачный рынок РФ 416.5 млрд ₽ — [CNews](https://www.cnews.ru/reviews/oblachnye_servisy_2025)
- AI рынок России $4.98B — [IMARC Group](https://www.imarcgroup.com/russia-artificial-intelligence-market)
- AI SDR market $4.27B → $18.19B к 2032 — [SalesTools.io](https://salestools.io/en/blog/ai-sdr-tools-comparison-2025)

---

## B. Competitive Matrix

| Фактор | Наш AI-Консультант | VK Cloud AI | Qualified (US) | Intercom Fin | AWS Amazon Q |
|--------|-------------------|-------------|----------------|-------------|-------------|
| Cloud-специфичная архитектура | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ | ⭐⭐⭐ |
| TCO-калькулятор в чате | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐ |
| Compliance 152-ФЗ / ФСТЭК | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐ | ⭐ |
| Migration planning | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐⭐ |
| Multi-agent | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Telegram-native | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐ |
| Русский язык | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐ |
| CRM (Bitrix/amoCRM) | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Стоимость | ₽500К/мес | Бесплатно | ~$2,500+/мес | $29/seat+$0.99/res | Часть AWS |

### Key Finding
Ни один продукт не объединяет: cloud-специфичная архитектура + TCO + compliance + migration planning + Telegram — в одном диалоговом интерфейсе. Это whitespace.

---

## C. Game Theory: Entry Strategy

### Players & Incentives

| Игрок | Инцентив | Стратегия |
|-------|----------|-----------|
| **Cloud.ru** | Увеличить pipeline, снизить нагрузку SA | Купить / интегрировать |
| **Yandex Cloud** | Догнать по AI-сервисам | Строить своё на YandexGPT |
| **VK Cloud** | Уже запустили AI Consultant | Расширять до pre-sales |
| **Мы** | Занять нишу first-mover | Pilot с Cloud.ru → scale |
| **Западные AI SDR** | Не работают в РФ | Не конкурент |

### Payoff Matrix

| | Cloud.ru строит сам | Cloud.ru покупает |
|---|---|---|
| Время | 6-12 мес | 2-4 нед (pilot) |
| Стоимость | ₽15-30М (R&D) | ₽6М/год (SaaS) |
| Риск | Высокий | Низкий |
| Фокус | Отвлечение | Core не страдает |

**Nash Equilibrium:** Cloud.ru выгоднее купить (5x дешевле, 10x быстрее).

**Рекомендация:** First-mover с Cloud.ru → white-label для остальных.

---

## D. Blue Ocean Strategy Canvas

### ERRC Framework

| Action | Что | TRIZ |
|--------|-----|------|
| **ELIMINATE** | Ожидание 2-5 недель до КП, повторные звонки | Пр. 10: Предварительное действие |
| **REDUCE** | Нагрузка на SA (100% → 35%), ручной TCO | Пр. 25: Самообслуживание |
| **RAISE** | Скорость (5 мин vs 5 недель), 24/7, compliance | Пр. 15: Динамичность |
| **CREATE** | Multi-agent, in-chat POC, сравнение провайдеров, Telegram | Пр. 6: Универсальность |

**Resolved Contradiction:** "Глубокая экспертиза" vs "Мгновенный ответ" → AI + RAG 6000+ docs + MCP API = экспертиза за секунды.

---

## E. Market Trends

| # | Тренд | Источник |
|---|-------|----------|
| 1 | Импортозамещение — миграция с AWS/Azure/GCP | [InferitCloud](https://inferitcloud.ru/importozameshhenie-v-oblakah-rossijskij-rynok-posle-uhoda-zapadnyh-provajderov/) |
| 2 | AI agents → $15T B2B покупок к 2028 | [Gartner/DC360](https://www.digitalcommerce360.com/2025/11/28/gartner-ai-agents-15-trillion-in-b2b-purchases-by-2028/) |
| 3 | GPU дефицит → спрос на AI Factory консалтинг | [CNews](https://www.cnews.ru/articles/2025-04-04_importozameshcheniemultiklaud_i_eksport) |
| 4 | 70%+ компаний используют GenAI | [TAdviser](https://tadviser.com/index.php/Article:Artificial_Intelligence_(Russian_market)) |
| 5 | AI рынок РФ: $4.98B → $40.67B к 2033 (CAGR 26.5%) | [IMARC](https://www.imarcgroup.com/russia-artificial-intelligence-market) |

---

## F. Regulatory Landscape

| Регуляция | Влияние |
|-----------|---------|
| 152-ФЗ | Compliance Agent — killer feature |
| ФСТЭК | Объяснение уровней защиты |
| Реестр отечественного ПО | Преимущество при госзакупках |
| ФЗ об AI (проект) | Audit trail консультаций |

---

## G. Competitive Sources

- VK Cloud AI Consultant (Jan 2025) — [TAdviser](https://tadviser.com/index.php/Product:VK_Cloud_Universal_Cloud_Platform_for_Digital_Services_Development_(formerly_VK_Cloud_Solutions))
- Qualified AI SDR — [Qualified](https://www.qualified.com/ai-sdr)
- Drift → Salesloft acquisition — [Salesloft](https://www.salesloft.com)
- Amazon Q — [AWS](https://aws.amazon.com/q/)
- AI SDR pricing benchmarks — [JoinValley](https://www.joinvalley.co/blog/ai-sdr-pricing-costs-roi-2026)
- Russia AI chatbot startups (88 total) — [Tracxn](https://tracxn.com/d/artificial-intelligence/ai-startups-in-chatbots-in-russia/__SpkG6QelQhRCY3VdkhM9Zq17lLxMjYJEvv8CRoAC3Zo/companies)
- Bitrix24 + amoCRM = 70% CRM рынка РФ — [Infullbroker](https://www.infullbroker.ru/articles/rossiyskiye-crm-sistemy/)
- AI economic impact: 7.9-12.8 трлн ₽ к 2030 — [Yakov&Partners](https://yakovpartners.com/publications/ai-2025/)
