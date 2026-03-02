# Product Requirements Document

**Product:** AI-Консультант Cloud.ru
**Version:** 0.1
**Author:** SPARC Generator
**Last Updated:** 2026-03-02
**Status:** Draft

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-03-02 | SPARC Generator | Initial draft from Phase 0 Product Discovery |

---

## 1. Executive Summary

### 1.1 Purpose

AI-Консультант Cloud.ru is a multi-agent AI platform that automates pre-sales cloud consulting for Russian cloud providers. It replaces the manual 2-5 week consultation process with instant, AI-driven architecture recommendations, TCO calculations, compliance checking, and migration planning — delivered via Telegram, web widget, and CRM integrations.

### 1.2 Scope

**In Scope:**
- Multi-agent AI system (6 specialized agents)
- RAG pipeline over 6000+ cloud documentation pages
- Real-time TCO calculator with multi-provider comparison
- 152-ФЗ / ФСТЭК compliance advisory
- Migration planning (VMware, AWS, Azure → Cloud.ru)
- Telegram bot, web chat widget, CRM integration (Bitrix24, amoCRM)
- Admin dashboard with ROI analytics
- Human escalation workflow
- Multi-tenant architecture for white-label deployment

**Out of Scope:**
- Actual cloud resource provisioning
- Payment processing
- End-user customer support (post-sales)
- Mobile native apps (Telegram serves this need)
- Real-time infrastructure monitoring

### 1.3 Definitions & Acronyms

| Term | Definition |
|------|------------|
| SA | Solution Architect — human consultant at cloud provider |
| TCO | Total Cost of Ownership — complete cost comparison |
| RAG | Retrieval-Augmented Generation — LLM + document retrieval |
| MCP | Model Context Protocol — standard for AI tool-use |
| 152-ФЗ | Russian Federal Law on Personal Data Protection |
| ФСТЭК | Federal Service for Technical and Export Control |
| CII | Critical Information Infrastructure (российская КИИ) |
| JTBD | Jobs To Be Done — framework for understanding customer needs |

---

## 2. Product Vision

### 2.1 Vision Statement

> Enable any cloud provider to offer instant, AI-powered pre-sales consulting that converts prospects into customers 10x faster than manual processes.

### 2.2 Problem Statement

**Problem:** Cloud providers rely on manual Solution Architects for pre-sales consulting. Each consultation takes 2-5 weeks, creating a pipeline bottleneck. Cloud.ru's SAs handle 10-15 active consultations each, spending 60% of time on repetitive questions (architecture patterns, pricing, compliance).

**Impact:** Lost deals to faster competitors, limited pipeline throughput, high cost per consultation (~₽50-100K in SA time per prospect), inability to scale consultations with business growth.

**Current Solutions:** Fully manual (Solution Architects + Google Docs/Sheets). VK Cloud launched an AI Consultant (Nov 2024) but it only handles documentation Q&A, not pre-sales advisory.

### 2.3 Strategic Alignment

- Aligns with Cloud.ru's mission to scale cloud adoption in Russia
- Supports import substitution mandate (CII migration from Jan 2025)
- Leverages Cloud.ru's AI Factory and Christofari supercomputer capabilities
- Fits into Cloud.ru partner ecosystem (SI partners get white-label tool)

### 2.4 Success Metrics

| Metric | Current | Target | Timeline |
|--------|---------|--------|----------|
| Consultation response time | 2-5 weeks | < 5 minutes | M3 |
| SA workload on repetitive tasks | 100% | 35% | M6 |
| Pipeline throughput (consultations/month) | ~50/SA | 200+ (AI) | M3 |
| Consultation → qualified lead conversion | 15-20% | 30-40% | M6 |
| Client NPS for consultation quality | N/A | > 60 | M6 |
| Pilot → production conversion | N/A | 80% | M3 |

---

## 3. Target Users

### 3.1 Primary Persona: Cloud Sales Director

| Attribute | Description |
|-----------|-------------|
| **Role** | VP Sales / Head of Cloud Sales at a cloud provider |
| **Demographics** | 35-50, B2B tech sales background |
| **Goals** | Increase pipeline, reduce sales cycle, hit revenue targets |
| **Pain Points** | SA bottleneck, slow proposal turnaround, lost deals |
| **Technical Proficiency** | Medium |
| **Usage Frequency** | Daily (dashboard), weekly (reports) |

### 3.2 Secondary Persona: Enterprise CTO (End User)

| Attribute | Description |
|-----------|-------------|
| **Role** | CTO / VP Engineering at enterprise considering cloud migration |
| **Demographics** | 35-55, technical background, decision maker |
| **Goals** | Get architecture recommendation, understand TCO, verify compliance |
| **Pain Points** | Waiting weeks for proposal, navigating compliance, comparing providers |
| **Technical Proficiency** | High |
| **Usage Frequency** | Ad-hoc (during evaluation phase) |

### 3.3 Tertiary Persona: SI Partner Manager

| Attribute | Description |
|-----------|-------------|
| **Role** | Project Manager / Architect at system integrator |
| **Demographics** | 30-45, IT consulting background |
| **Goals** | Offer cloud consulting to clients without deep cloud expertise |
| **Pain Points** | Lack of specialized cloud architects, slow responses from providers |
| **Technical Proficiency** | Medium-High |
| **Usage Frequency** | Weekly (client projects) |

### 3.4 Anti-Personas (Who this is NOT for)

- Individual developers looking for code snippets
- Small businesses needing shared hosting
- Cloud provider's internal DevOps teams (post-sales)
- End consumers of cloud-hosted applications

---

## 4. Requirements

### 4.1 Functional Requirements

#### 4.1.1 Feature: AI Consultation Engine

**Description:** Multi-agent system that handles cloud consulting dialogues via natural language.

**User Stories:**

| ID | As a... | I want to... | So that... | Priority | Effort |
|----|---------|--------------|------------|----------|--------|
| US-001 | Enterprise CTO | ask about migrating 200 VMware servers to cloud | I get an architecture recommendation in minutes | Must | L |
| US-002 | Enterprise CTO | get a real-time TCO comparison of 3 providers | I can make an informed decision quickly | Must | L |
| US-003 | Enterprise CTO | check 152-ФЗ compliance for my workload | I know which cloud meets regulatory requirements | Must | M |
| US-004 | Enterprise CTO | receive a step-by-step migration plan | I can estimate effort and timeline | Should | L |
| US-005 | Enterprise CTO | ask follow-up questions in natural dialogue | the consultation feels like talking to a human expert | Must | M |

**Acceptance Criteria:**

```gherkin
Feature: AI Consultation Engine

  Scenario: VMware migration consultation
    Given a CTO asks "I need to migrate 200 VMware servers to cloud"
    When the Architect Agent processes the request
    Then it recommends a target architecture with specific Cloud.ru services
    And provides estimated resource sizing
    And includes a migration timeline (4-wave approach)
    And response time is under 30 seconds

  Scenario: TCO comparison
    Given a CTO asks "Compare costs for 50 VMs with 8 vCPU, 32GB RAM"
    When the Cost Calculator Agent processes the request
    Then it shows monthly TCO for Cloud.ru, Yandex Cloud, and VK Cloud
    And highlights cost differences with percentages
    And includes 1-year and 3-year projections
```

#### 4.1.2 Feature: Multi-Channel Delivery

**Description:** Consultation available via Telegram, web widget, and CRM.

| ID | As a... | I want to... | So that... | Priority | Effort |
|----|---------|--------------|------------|----------|--------|
| US-006 | Enterprise CTO | consult via Telegram | I can get answers on my preferred platform | Must | M |
| US-007 | Cloud Sales Rep | see AI consultations in Bitrix24 CRM | deals are automatically tracked | Should | M |
| US-008 | Website Visitor | start a consultation via web widget on cloud.ru | I get instant answers without leaving the site | Must | S |
| US-009 | SI Partner | use white-label bot with their branding | their clients see partner's brand, not ours | Could | L |

#### 4.1.3 Feature: Admin Dashboard & Analytics

**Description:** Real-time dashboard showing consultation metrics, pipeline, and ROI.

| ID | As a... | I want to... | So that... | Priority | Effort |
|----|---------|--------------|------------|----------|--------|
| US-010 | Cloud Sales Director | see daily consultation volume and conversion rates | I can track pipeline health | Must | M |
| US-011 | Cloud Sales Director | view ROI metrics (time saved, leads generated) | I can justify continued investment | Must | M |
| US-012 | Admin | manage AI agent configurations | I can tune responses without code changes | Should | L |
| US-013 | Admin | review and approve AI recommendations before sending | quality control for high-stakes consultations | Should | M |

#### 4.1.4 Feature: Human Escalation

**Description:** Seamless handoff to human SA when AI confidence is low or request is complex.

| ID | As a... | I want to... | So that... | Priority | Effort |
|----|---------|--------------|------------|----------|--------|
| US-014 | Enterprise CTO | be transferred to a human expert when AI can't help | I always get the answer I need | Must | S |
| US-015 | SA | receive full context of AI conversation when escalated | I don't ask the client to repeat information | Must | M |
| US-016 | SA | rate AI responses after reviewing | the AI learns from human feedback | Should | S |

### 4.2 Non-Functional Requirements

#### 4.2.1 Performance

| Metric | Requirement | Rationale |
|--------|-------------|-----------|
| Response Time (simple query, p50) | < 5 seconds | User expects chat-like speed |
| Response Time (complex TCO calc, p99) | < 30 seconds | Multi-agent orchestration |
| Throughput | 100 concurrent dialogues | Peak load for 5 providers |
| RAG retrieval latency | < 2 seconds | Acceptable for conversational UX |

#### 4.2.2 Availability & Reliability

| Metric | Requirement |
|--------|-------------|
| Uptime SLA | 99.5% (production), 99.9% (enterprise) |
| RTO | 4 hours (production), 1 hour (enterprise) |
| RPO | 1 hour |
| MTTR | 30 minutes |

#### 4.2.3 Security

| Requirement | Implementation |
|-------------|----------------|
| Authentication | JWT + OAuth2 for admin; Telegram OAuth for users |
| Authorization | RBAC: admin, agent_manager, viewer |
| Data Encryption (at rest) | AES-256 for conversation logs and client data |
| Data Encryption (in transit) | TLS 1.3 for all communications |
| Compliance | 152-ФЗ data residency (Russian servers), ФСТЭК guidelines |
| API Security | Rate limiting, API key rotation, audit logs |
| PII Handling | Conversation logs anonymized after 90 days |

#### 4.2.4 Scalability

| Dimension | Current (MVP) | Target (1 year) | Target (3 years) |
|-----------|:---:|:---:|:---:|
| Cloud provider clients | 1 | 5 | 15+ |
| Concurrent dialogues | 20 | 100 | 500 |
| RAG document corpus | 6,000 pages | 20,000 pages | 100,000+ pages |
| Monthly consultations | 200 | 2,000 | 10,000+ |

### 4.3 Technical Requirements

#### 4.3.1 Platform Support

| Platform | Minimum Version | Notes |
|----------|----------------|-------|
| Web browsers | Chrome 90+, Firefox 88+, Safari 15+ | Admin dashboard + web widget |
| Telegram | Bot API 7.0+ | Primary end-user channel |
| Bitrix24 | REST API v1 | CRM integration |
| amoCRM | API v4 | CRM integration |

#### 4.3.2 Integration Requirements

| System | Integration Type | Data Flow | Priority |
|--------|-----------------|-----------|----------|
| Cloud.ru API | REST API / MCP | Bidirectional (pricing, services, config) | Must |
| Telegram Bot API | Webhook | Bidirectional (messages, callbacks) | Must |
| Bitrix24 CRM | REST API | Out (create leads, update deals) | Should |
| amoCRM | REST API | Out (create leads) | Could |
| LLM Provider (Claude/GigaChat) | REST API | Bidirectional (completions) | Must |
| Vector DB (for RAG) | Native driver | Bidirectional (index, query) | Must |

#### 4.3.3 Constraints

| Constraint Type | Description | Impact |
|-----------------|-------------|--------|
| Technical | Must use Docker + Docker Compose on VPS | Architecture pattern |
| Technical | Monorepo structure (distributed monolith) | Code organization |
| Business | Free 3-month pilot required | Revenue delay |
| Regulatory | 152-ФЗ — all data stored in Russia | Infrastructure location |
| Regulatory | ФСТЭК — security levels for CII clients | Additional certification |
| Timeline | MVP in 3 months (pilot start) | Feature prioritization |

---

## 5. User Journeys

### 5.1 Journey: VMware Migration Consultation

**Persona:** Enterprise CTO
**Goal:** Get architecture recommendation for migrating 200 VMware servers
**Trigger:** CTO visits cloud.ru or writes to Telegram bot

```
Step 1: Initial Contact
  User Action: "I need to migrate 200 VMware servers to cloud"
  System Response: Architect Agent activates, asks clarifying questions
  (workload types, current specs, compliance requirements)

Step 2: Architecture Recommendation
  User Action: Provides workload details
  System Response: Generates target architecture with Cloud.ru services
  (compute, storage, networking, security groups)

Step 3: TCO Calculation
  User Action: "How much will this cost?"
  System Response: Cost Calculator Agent provides monthly TCO
  comparison: Cloud.ru vs Yandex Cloud vs VK Cloud

Step 4: Compliance Check
  User Action: "We process personal data, need 152-ФЗ compliance"
  System Response: Compliance Agent checks requirements, confirms
  Cloud.ru meets 152-ФЗ, suggests specific security configurations

Step 5: Migration Plan
  User Action: "What's the migration timeline?"
  System Response: Migration Agent creates 4-wave plan with
  timeline, risk assessment, and rollback procedures

Step 6: Lead Qualification
  System Response: Creates qualified lead in CRM (Bitrix24)
  with full consultation transcript, TCO data, architecture diagram
  Outcome: Sales team receives warm, qualified lead with all technical data
```

**Error Paths:**

| Step | Error Condition | System Response | User Recovery |
|------|-----------------|-----------------|---------------|
| 2 | Workload type not supported | "This workload requires custom architecture. Connecting you with our SA." | Human escalation |
| 3 | Pricing data unavailable for a service | "I don't have current pricing for X. Let me check with the team." | Escalate, respond async |
| 4 | Compliance requirement unclear | "Can you specify which data types you process?" | Clarifying question |

---

## 6. UI/UX Requirements

### 6.1 Design Principles

- **Conversational first** — primary interaction is natural language dialogue
- **Progressive disclosure** — start simple, reveal complexity as needed
- **Source transparency** — every claim links to documentation source
- **Human-in-the-loop** — escalation is always one click away
- **Cloud.ru branding** — orange accent (#FF6B00), clean, professional

### 6.2 Key Screens/Views

| Screen | Purpose | Key Elements |
|--------|---------|--------------|
| Chat Interface (Telegram) | Primary consultation channel | Message bubbles, inline TCO tables, architecture diagrams as images |
| Web Widget | Website embed for cloud.ru | Floating chat bubble, expandable panel, same AI capabilities |
| Admin Dashboard | Metrics and management | KPI cards, consultation list, agent config, ROI chart |
| Agent Console | Monitor active consultations | Real-time feed, confidence scores, escalation queue |
| Analytics | Historical performance | Charts: consultations/day, conversion funnel, avg response time |

### 6.3 Accessibility Requirements

- WCAG 2.1 Level: AA for admin dashboard
- Telegram accessibility: native platform features
- Keyboard navigation for admin interface
- Screen reader support for dashboard

---

## 7. Release Strategy

### 7.1 MVP (Phase 1) — Month 1-3

**Timeline:** Month 3

**Features:**

| Feature | Priority | Status |
|---------|----------|--------|
| Architect Agent (Cloud.ru services) | Must | Planned |
| Cost Calculator Agent (3 providers) | Must | Planned |
| Compliance Agent (152-ФЗ basics) | Must | Planned |
| Telegram bot integration | Must | Planned |
| Basic RAG pipeline (Cloud.ru docs) | Must | Planned |
| Human escalation (manual) | Must | Planned |
| Basic admin dashboard (metrics) | Must | Planned |

**Success Criteria:**
- [ ] 200+ consultations/month processed
- [ ] Response time < 30 seconds (p99)
- [ ] User satisfaction > 70% (survey)
- [ ] 3+ qualified leads/week generated

### 7.2 v1.0 (Phase 2) — Month 4-6

**Features:**

| Feature | Priority | Status |
|---------|----------|--------|
| Migration Agent (VMware, AWS) | Should | Planned |
| AI Factory Agent (GPU consulting) | Should | Planned |
| Web widget for cloud.ru | Should | Planned |
| Bitrix24 CRM integration | Should | Planned |
| ROI dashboard with analytics | Should | Planned |
| Multi-tenant architecture | Should | Planned |

### 7.3 Future Phases

| Phase | Features | Tentative Timeline |
|-------|----------|-------------------|
| v1.1 (M7-9) | amoCRM integration, white-label, 2nd client onboarding | Month 7-9 |
| v2.0 (M10-15) | Multi-cloud comparison, partner portal, advanced analytics | Month 10-15 |
| v3.0 (M16-24) | Self-service onboarding, marketplace, CIS expansion | Month 16-24 |

---

## 8. Dependencies

### 8.1 Internal Dependencies

| Dependency | Owner | Impact | Status |
|------------|-------|--------|--------|
| Cloud.ru documentation corpus | Cloud.ru team | RAG quality | Need access |
| Cloud.ru pricing API | Cloud.ru team | TCO accuracy | Need API key |
| Cloud.ru SA team for pilot validation | Cloud.ru | Quality feedback | Need commitment |

### 8.2 External Dependencies

| Dependency | Provider | Risk Level | Mitigation |
|------------|----------|------------|------------|
| LLM API (Claude / GigaChat) | Anthropic / Sber | Medium | Model-agnostic architecture, multi-provider fallback |
| Vector DB hosting | Self-hosted (Qdrant) | Low | Docker container, easy to migrate |
| Telegram Bot API | Telegram | Low | Stable, well-documented |
| VPS hosting (Russia) | AdminVPS / HOSTKEY | Low | Multiple providers available |

---

## 9. Risks & Mitigations

| Risk ID | Description | Probability | Impact | Mitigation Strategy | Owner |
|---------|-------------|:-----------:|:------:|---------------------|-------|
| R-001 | Cloud.ru pilot doesn't convert to paid | Medium | Critical | ROI dashboard with daily metrics; executive alignment | PM |
| R-002 | LLM hallucination in architecture advice | Medium | High | RAG source attribution; confidence scoring; human review | Tech Lead |
| R-003 | VK Cloud extends AI Consultant to pre-sales | High | Medium | Data moat; deeper CRM integration; faster feature velocity | PM |
| R-004 | 152-ФЗ requirements change | Low | Medium | Compliance agent auto-updates; legal advisory | Legal |
| R-005 | LLM API costs exceed budget | Medium | Medium | Caching; model-agnostic; smaller models for simple queries | Tech Lead |
| R-006 | Single-client dependency in Year 1 | High | High | Aggressive 2nd client from M4; partner channel from M6 | Sales |

---

## 10. Open Questions

| ID | Question | Owner | Due Date | Resolution |
|----|----------|-------|----------|------------|
| Q-001 | Will Cloud.ru provide API access to pricing data? | PM | M1 | Pending pilot agreement |
| Q-002 | Which LLM to use as primary (Claude vs GigaChat)? | Tech Lead | M1 | Benchmark during MVP |
| Q-003 | On-premise or SaaS deployment for Cloud.ru? | Architect | M1 | Depends on 152-ФЗ requirements |
| Q-004 | White-label pricing model for SI partners? | PM | M6 | After first paid client |

---

## 11. Appendices

### A. Research Findings

See `Research_Findings.md` for complete market and technology research.

### B. Competitive Analysis

| Competitor | Strengths | Weaknesses | Differentiation Opportunity |
|------------|-----------|------------|----------------------------|
| VK Cloud AI Consultant | Free, native, Terraform gen | Docs-only, not pre-sales | Pre-sales focus + TCO + compliance |
| Qualified (US) | Enterprise CRM, AI SDR | No Russian market | Russian compliance + Telegram |
| Intercom Fin | Proven AI support | Not pre-sales advisory | Cloud architecture expertise |
| AWS Amazon Q | Deep AWS integration | AWS-only, no Russian market | Multi-cloud + 152-ФЗ |

### C. Technical Specifications

See `Architecture.md` and `Pseudocode.md` for detailed technical design.

### D. Glossary

See Section 1.3 for definitions and acronyms.
