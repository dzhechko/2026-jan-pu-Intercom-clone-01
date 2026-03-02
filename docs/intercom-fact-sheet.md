# Intercom Verified Fact Sheet

> Compiled: 2026-03-02
> Purpose: Reverse engineering analysis baseline
> Legend: [H] = Hypothesis / unverified estimate

---

## 1. Company Basics

| Data Point | Value | Source |
|---|---|---|
| **Legal Name** | Intercom, Inc. | [Wikipedia](https://en.wikipedia.org/wiki/Intercom,_Inc.) |
| **Founded** | 2011 (California, USA) | [Wikipedia](https://en.wikipedia.org/wiki/Intercom,_Inc.) |
| **Incorporated** | Delaware, USA | [Wikipedia](https://en.wikipedia.org/wiki/Intercom,_Inc.) |
| **HQ Location** | San Francisco, California, USA | [Intercom About](https://www.intercom.com/about) |
| **Other Offices** | Dublin (Ireland), London (UK), Chicago (IL, USA), Sydney (Australia) | [Glassdoor Locations](https://www.glassdoor.com/Location/All-Intercom-Office-Locations-E1035935.htm) |
| **Employees** | ~1,948 (as of Jan 31, 2026) | [Tracxn](https://tracxn.com/d/companies/intercom/__QjX3fjzW0zfyXFUopScRM09RgKkysZYa5l-W1sdKY1w) |
| **Current CEO** | Eoghan McCabe (co-founder; returned as CEO Oct 2022) | [Intercom About](https://www.intercom.com/about/eoghan-mccabe) |
| **Mission Statement** | "Make internet business personal" | [Comparably](https://www.comparably.com/companies/intercom/mission) |
| **Vision** | "Bring a Messenger-first, personal experience to all customer and business communication" | [Comparably](https://www.comparably.com/companies/intercom/mission) |

### Founders (all four are Irish)

| Name | Role | Source |
|---|---|---|
| Eoghan McCabe | CEO & Chairman | [Intercom About](https://www.intercom.com/about) |
| Des Traynor | Co-founder (Chief Strategy Officer) | [Wikipedia](https://en.wikipedia.org/wiki/Intercom,_Inc.) |
| Ciaran Lee | Co-founder | [Wikipedia](https://en.wikipedia.org/wiki/Intercom,_Inc.) |
| David Barrett | Co-founder | [Wikipedia](https://en.wikipedia.org/wiki/Intercom,_Inc.) |

### CEO History

| Period | CEO | Source |
|---|---|---|
| 2011 - 2020 | Eoghan McCabe | [Contrary Research](https://research.contrary.com/company/intercom) |
| 2020 - Oct 2022 | Karen Peacock | [Wikipedia](https://en.wikipedia.org/wiki/Intercom,_Inc.) |
| Oct 2022 - present | Eoghan McCabe (returned) | [Intercom About](https://www.intercom.com/about/eoghan-mccabe) |

---

## 2. Funding History

**Total Raised: ~$241M** across 6+ rounds from 35 investors.

| Round | Date | Amount | Lead Investor(s) | Post-Money Valuation | Source |
|---|---|---|---|---|---|
| Seed | Oct 2011 - Jan 2012 | $1M | 500 Global (fka 500 Startups), angel investors incl. Biz Stone, David Sacks, Dan Martell | Undisclosed | [Tracxn](https://tracxn.com/d/companies/intercom/__QjX3fjzW0zfyXFUopScRM09RgKkysZYa5l-W1sdKY1w/funding-and-investors), [Wikipedia](https://en.wikipedia.org/wiki/Intercom,_Inc.) |
| Series A | Mar 2013 | $6M | Social Capital | Undisclosed | [Clay](https://www.clay.com/dossier/intercom-funding) |
| Series B | Jan 2014 | $23M | Bessemer Venture Partners | Undisclosed | [Clay](https://www.clay.com/dossier/intercom-funding) |
| Series C | Aug 2015 | $35M | ICONIQ Growth | Undisclosed | [Clay](https://www.clay.com/dossier/intercom-funding) |
| Series D (Tranche 1) | Apr 2016 | $50M | Index Ventures | Undisclosed | [Clay](https://www.clay.com/dossier/intercom-funding) |
| Series D (Tranche 2) | Mar 2018 | $125M | Kleiner Perkins (w/ GV participation) | $1.275B (unicorn status) | [Tracxn](https://tracxn.com/d/companies/intercom/__QjX3fjzW0zfyXFUopScRM09RgKkysZYa5l-W1sdKY1w/funding-and-investors) |

**Total: ~$240-242M** (varies by source due to undisclosed micro-rounds)

### Key Investors
- Kleiner Perkins, Bessemer Venture Partners, Social Capital, ICONIQ Capital/Growth, Index Ventures, GV (Google Ventures), 500 Global
- Angel investors: Biz Stone (Twitter co-founder), David Sacks, Andy McLoughlin (Huddle founder), Dan Martell, Digital Garage

### Latest Valuation
- **$1.28-1.30B** (last priced at 2018 Series D); valuation/revenue multiple ~4.3x as of 2024
- Source: [Sacra](https://sacra.com/c/intercom/valuation/), [PremierAlts](https://www.premieralts.com/companies/intercom/valuation)

---

## 3. Product Details

### Main Products

| Product | Description | Source |
|---|---|---|
| **Fin AI Agent** | #1 AI agent for customer service; powered by Anthropic Claude; resolves queries across chat, email, phone, WhatsApp, SMS | [Intercom Fin](https://www.intercom.com/fin) |
| **Helpdesk / Inbox** | Shared inbox for support agents with AI copilot, ticketing, macros, SLA management | [Intercom Suite](https://www.intercom.com/suite) |
| **Messenger** | Embeddable web/mobile chat widget for live chat, bots, product tours | [Intercom Features](https://www.intercom.com/help/en/articles/591233-intercom-features-explained) |
| **Help Center** | Self-serve knowledge base (public + internal articles) | [Intercom Features](https://www.intercom.com/help/en/articles/591233-intercom-features-explained) |
| **Outbound Messaging** | Proactive messages: in-app banners, tooltips, push notifications, email campaigns, SMS | [Intercom Features](https://www.intercom.com/help/en/articles/591233-intercom-features-explained) |
| **Workflows / Automation** | Visual bot builder, custom bots, routing rules, Fin Tasks | [Intercom Suite](https://www.intercom.com/suite) |
| **Reporting & Analytics** | Pre-built and custom reports, CSAT, Fin performance dashboard | [Intercom Suite](https://www.intercom.com/suite) |

### Platforms

| Platform | Details | Source |
|---|---|---|
| **Web App** | SaaS dashboard (app.intercom.com) for agents/admins | [Intercom](https://www.intercom.com) |
| **Messenger (JS SDK)** | Embeddable widget for websites | [Intercom Developers](https://developers.intercom.com/docs) |
| **iOS SDK** | Native iOS (Swift/ObjC), iOS 15+ | [GitHub](https://github.com/intercom/intercom-ios) |
| **Android SDK** | Native Android (Kotlin/Java), API 21+ | [GitHub](https://github.com/intercom/intercom-android) |
| **React Native SDK** | Cross-platform mobile wrapper, RN 0.59+ | [GitHub](https://github.com/intercom/intercom-react-native) |
| **REST API** | Full CRUD API for contacts, conversations, messages, data events, tags | [Intercom Developers](https://developers.intercom.com/docs) |
| **Webhooks** | Real-time event notifications | [Intercom Developers](https://developers.intercom.com/docs) |

### Current Pricing (as of 2026)

| Plan | Monthly (per seat) | Annual (per seat/mo) | Key Differentiators | Source |
|---|---|---|---|---|
| **Essential** | $39 | $29 | Messenger, Fin AI, shared inbox, pre-built reports, public help center | [Intercom Pricing](https://www.intercom.com/pricing) |
| **Advanced** | $99 | $85 | + 20 free lite seats, workflows, multilingual help center, side conversations | [Intercom Pricing](https://www.intercom.com/pricing) |
| **Expert** | $139 | $132 | + 50 lite seats, HIPAA, multibrand, workload management, SSO, custom roles | [Intercom Pricing](https://www.intercom.com/pricing) |

**Additional / Usage-Based Costs:**
- Fin AI Agent: **$0.99 per resolution** (only charged on successful resolutions)
- SMS: $0.01 - $0.10 per message
- WhatsApp: usage-based
- Email campaigns: overage fees beyond plan limits
- Startup discount: up to 90% off for companies <2 years old with <$1M funding

Source: [Intercom Pricing](https://www.intercom.com/pricing), [SaaSGenie](https://www.saasgenie.ai/blogs/intercom-plans-and-pricing)

### Top 5 Features

1. **Fin AI Agent** - AI-first customer service bot (Anthropic Claude-powered), ~51% avg resolution rate, up to 67%+ for optimized deployments; handles chat, email, and voice
2. **Omnichannel Inbox** - Unified inbox across live chat, email, WhatsApp, SMS, social with AI Copilot for agent assist
3. **Messenger & Product Tours** - Embeddable chat widget with targeted in-app messages, banners, tooltips, carousels
4. **Help Center** - Multilingual self-serve knowledge base with AI-powered article suggestions
5. **Workflows & Automation** - Visual bot builder, custom routing, Fin Tasks for multi-step process automation

Sources: [Intercom Suite](https://www.intercom.com/suite), [Fin AI](https://www.intercom.com/fin)

---

## 4. Scale & Traction

| Metric | Value | Date | Source |
|---|---|---|---|
| **Total Customers** | 25,000 - 30,000 | 2024 | [GetLatka](https://getlatka.com/companies/intercom-1), [Intercom About](https://www.intercom.com/about) |
| **Revenue** | ~$343M/year | 2024 | [Sacra](https://sacra.com/research/intercom-at-343m/) |
| **Revenue Growth** | 25% YoY (2024 vs 2023) | 2024 | [Sacra](https://sacra.com/c/intercom/) |
| **Prior Year Revenue** | ~$274M [H] (derived from 25% growth on $343M) | 2023 | Calculated |
| **ARR (Historical)** | ~$300M | 2022 | [Growfusely](https://growfusely.com/blog/intercom) |
| **Revenue Projection** | ~$703M (base case, 22% CAGR) | 2027 [H] | [Sacra](https://sacra.com/c/intercom/) |
| **2025 Revenue** | ~$400-430M [H] (estimated at ~20-25% growth on $343M) | 2025 [H] | Estimated |
| **Fin AI Revenue** | $100M+ ARR run-rate from Fin AI alone | 2024-2025 | [Substack / GTM Newsletter](https://thegtmnewsletter.substack.com/p/gtm-178-intercom-ai-agent-outcome-based-pricing-archana-agrawal) |
| **Deploy Frequency** | ~150 deploys/day | Ongoing | [Buildkite Case Study](https://buildkite.com/resources/case-studies/intercom/) |
| **Database Scale** | Hundreds of TB, 2M reads/sec, tens of thousands writes/sec | 2024 | [Intercom Blog](https://www.intercom.com/blog/evolving-intercoms-database-infrastructure/) |

### Key Markets
- **Primary**: North America (US focus), Europe (strong UK/Ireland presence)
- **Secondary**: Australia/APAC
- **Segment Focus**: Mid-market and SMB; B2B over B2C (higher-value interactions)
- **Industry Mix**: Technology/SaaS, E-commerce, Financial Services, Healthcare, Manufacturing
- Source: [Sacra](https://sacra.com/c/intercom/), [Contrary Research](https://research.contrary.com/company/intercom)

### Notable Enterprise Customers
| Company | Industry | Source |
|---|---|---|
| Atlassian | Software/DevTools | [Intercom About](https://www.intercom.com/about) |
| Amazon | E-commerce/Cloud | [Intercom About](https://www.intercom.com/about) |
| Lyft Business | Transportation | [Intercom About](https://www.intercom.com/about) |
| Microsoft | Software/Cloud | [AppsRunTheWorld](https://www.appsruntheworld.com/customers-database/products/view/intercom) |
| Shopify | E-commerce | [H] Widely reported |
| Notion | Productivity | [H] Widely reported |
| Unity | Gaming/Dev Platform | [H] Widely reported |
| BASF Catalysts | Chemicals/Manufacturing | [AppsRunTheWorld](https://www.appsruntheworld.com/customers-database/products/view/intercom) |
| Amgen | Pharmaceuticals | [AppsRunTheWorld](https://www.appsruntheworld.com/customers-database/products/view/intercom) |
| Sysco | Food Distribution | [AppsRunTheWorld](https://www.appsruntheworld.com/customers-database/products/view/intercom) |

### Customer Size Distribution
- 0-100 employees: 77.92%
- 101-1,000 employees: 19.15%
- 1,001-10,000 employees: 2.64%
- 10,000+ employees: 0.29%
- Source: [ZoomInfo](https://www.zoominfo.com/tech/297/intercom-tech-by-revenue)

---

## 5. Technology Stack

### Backend

| Technology | Usage | Source |
|---|---|---|
| **Ruby on Rails** | Core monolith application; serves web, API, and async workers on dedicated per-function clusters | [Intercom Blog](https://www.intercom.com/blog/intercom-for-enterprise-infrastructure-and-scale/) |
| **Ruby** | Primary backend language | [Intercom Blog](https://www.intercom.com/blog/core-technologies-team/) |
| **ActiveRecord** | ORM layer for Rails monolith | [Intercom Blog](https://www.intercom.com/blog/evolving-intercoms-database-infrastructure/) |
| **Python** | AI/ML workloads (Fin AI, data science) [H] | Inferred from AI team scaling |
| **Java/Kotlin** | Android SDK | [GitHub](https://github.com/intercom/intercom-android) |
| **Swift/Objective-C** | iOS SDK | [GitHub](https://github.com/intercom/intercom-ios) |

### Frontend

| Technology | Usage | Source |
|---|---|---|
| **React** | New default for all UI development (migrated from Ember) | [Intercom Blog](https://www.intercom.com/blog/betting-on-the-future-of-frontend-at-intercom/) |
| **Ember.js** | Legacy frontend (teammate app); being phased out | [Intercom Blog](https://www.intercom.com/blog/evolution-of-ember-at-intercom/) |
| **TypeScript** | Frontend language [H] (standard for React codebases at this scale) | Inferred |
| **JavaScript** | Messenger widget SDK, web integrations | [Intercom Developers](https://developers.intercom.com/docs) |

### Databases & Data Stores

| Technology | Usage | Source |
|---|---|---|
| **MySQL (via Vitess / PlanetScale Metal)** | Primary relational database; migrated from Amazon Aurora MySQL to PlanetScale-managed Vitess for sharding, zero-downtime migrations | [Intercom Blog](https://www.intercom.com/blog/evolving-intercoms-database-infrastructure-lessons-and-progress/) |
| **Amazon Aurora MySQL** | Legacy primary DB (being migrated off) | [Intercom Blog](https://www.intercom.com/blog/evolving-intercoms-database-infrastructure/) |
| **MongoDB** | Secondary datastore for specific workloads | [Intercom Blog](https://www.intercom.com/blog/keeping-intercom-up/) |
| **Redis** | Low-latency cache, transient data, short-lived counters | [Intercom Blog](https://www.intercom.com/blog/keeping-intercom-up/) |
| **Elasticsearch** | Full-text search engine; self-hosted on EC2 in per-function clusters; powers UI search and custom data attributes | [Intercom Blog](https://www.intercom.com/blog/building-elasticsearch-at-intercom/) |

### Cloud & Infrastructure

| Technology | Usage | Source |
|---|---|---|
| **AWS (exclusive)** | Sole cloud provider; EC2, RDS, S3, and more | [Intercom Blog](https://www.intercom.com/blog/intercom-for-enterprise-infrastructure-and-scale/) |
| **3 Data Regions** | US, EU, Australia (multi-AZ each) | [Intercom Blog](https://www.intercom.com/blog/intercom-for-enterprise-infrastructure-and-scale/) |
| **PlanetScale Metal** | Managed Vitess database platform within Intercom's AWS accounts | [Intercom Blog](https://www.intercom.com/blog/evolving-intercoms-database-infrastructure-lessons-and-progress/) |

### AI/ML

| Technology | Usage | Source |
|---|---|---|
| **Anthropic Claude** | Powers Fin AI Agent (switched from OpenAI/GPT-4 in late 2024) | [TheLetterTwo](https://thelettertwo.com/2024/10/12/intercom-releases-fin-2-ai-agent-switching-anthropic-from-openai/) |
| **OpenAI GPT-4** | Previously powered Fin v1 (pre-Oct 2024) | [TheLetterTwo](https://thelettertwo.com/2024/10/12/intercom-releases-fin-2-ai-agent-switching-anthropic-from-openai/) |
| **Proprietary CX Models** | In-house customer experience AI models (50+ AI researchers as of 2025) | [Sacra](https://sacra.com/c/intercom/) |
| **$100M+ AI Investment** | Committed to AI R&D | [Sacra](https://sacra.com/c/intercom/) |

### CI/CD & Observability

| Technology | Usage | Source |
|---|---|---|
| **Buildkite** | CI/CD orchestration; runs tens of thousands of tests in ~3 minutes; ~150 deploys/day | [Buildkite Case Study](https://buildkite.com/resources/case-studies/intercom/) |
| **Honeycomb** | Observability platform; auto-instrumented traces via Honeycomb Refinery with dynamic sampling | [Honeycomb Case Study](https://www.honeycomb.io/case-studies/intercom) |
| **EC2-based CI Agents** | Build agents self-hosted on EC2 | [Buildkite Case Study](https://buildkite.com/resources/case-studies/intercom/) |

### Architecture Philosophy
- **Distributed Monolith**: Core is a single Rails monolith deployed to thousands of workers on per-function clusters
- **Small core tech set**: Deliberately limits technology choices to build deep domain expertise
- **Auto-instrumented**: Rails monolith has zero-code observability via attribute-rich traces
- **"Shipping is our heartbeat"**: Culture of rapid, frequent deploys
- Source: [Intercom Blog](https://www.intercom.com/blog/core-technologies-team/)

---

## Confidence Summary

| Section | Confidence | Notes |
|---|---|---|
| Company basics | HIGH | Public record, official sources |
| Funding history | HIGH | Cross-verified across Tracxn, Crunchbase, Clay |
| Product details | HIGH | Official pricing page and product pages |
| Pricing | HIGH | Verified on intercom.com/pricing (as of 2026) |
| Revenue ($343M 2024) | MEDIUM-HIGH | Sacra equity research; not audited public filing |
| Customer count (25-30K) | MEDIUM | Varies by source and definition |
| 2025 revenue estimate | LOW | [H] Extrapolated from growth rate |
| Technology stack | HIGH | First-party engineering blog posts |
| Notable customers | MEDIUM | Some [H] - not all independently verified |
| Employee count | MEDIUM-HIGH | Tracxn Jan 2026 snapshot |
