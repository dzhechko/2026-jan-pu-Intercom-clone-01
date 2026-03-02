# Specification — AI-Консультант Cloud.ru

## Executive Summary

This specification defines the detailed requirements for the AI-Консультант platform. The system is a multi-agent AI product that automates pre-sales cloud consulting, featuring 6 specialized agents orchestrated via MCP, RAG over 6000+ documents, and multi-channel delivery (Telegram, web widget, CRM).

---

## Feature Matrix

| Feature | MVP (M1-3) | v1.0 (M4-6) | v2.0 (M10-15) | Priority |
|---------|:---:|:---:|:---:|----------|
| Architect Agent | ✅ | ✅ | ✅ | Must |
| Cost Calculator Agent | ✅ | ✅ | ✅ | Must |
| Compliance Agent (152-ФЗ) | ✅ | ✅ | ✅ | Must |
| Migration Agent | | ✅ | ✅ | Should |
| AI Factory Agent (GPU) | | ✅ | ✅ | Should |
| Human Escalation Agent | ✅ | ✅ | ✅ | Must |
| RAG Pipeline | ✅ | ✅ | ✅ | Must |
| Telegram Bot | ✅ | ✅ | ✅ | Must |
| Web Chat Widget | | ✅ | ✅ | Should |
| Admin Dashboard | ✅ (basic) | ✅ (full) | ✅ | Must |
| ROI Analytics | | ✅ | ✅ | Should |
| Bitrix24 CRM | | ✅ | ✅ | Should |
| amoCRM | | | ✅ | Could |
| White-Label | | | ✅ | Could |
| Multi-Provider Comparison | | ✅ | ✅ | Should |
| Partner Portal | | | ✅ | Could |
| Self-Service Onboarding | | | ✅ | Could |

---

## User Stories with Acceptance Criteria

### Epic 1: AI Consultation Engine

#### US-001: Cloud Architecture Consultation

```
As an Enterprise CTO,
I want to describe my infrastructure and get a cloud architecture recommendation,
So that I can evaluate Cloud.ru as a migration target in minutes instead of weeks.
```

**Acceptance Criteria:**

```gherkin
Feature: Cloud Architecture Consultation

  Scenario: Happy path - VMware migration
    Given a CTO connects via Telegram
    And sends "I need to migrate 200 VMware servers to cloud"
    When the Architect Agent processes the request
    Then it asks 2-3 clarifying questions (workload types, specs, compliance)
    And generates a target architecture using Cloud.ru services
    And includes compute, storage, and networking recommendations
    And provides estimated resource sizing
    And response time is under 30 seconds per message

  Scenario: Complex workload requiring human
    Given a CTO describes a custom FPGA-based workload
    When the Architect Agent detects low confidence (<0.6)
    Then it transparently communicates its limitation
    And offers to connect with a human Solution Architect
    And passes full conversation context to the SA

  Scenario: Follow-up questions
    Given a CTO received an architecture recommendation
    When they ask "Can I use Kubernetes instead of VMs?"
    Then the Architect Agent adjusts the recommendation
    And explains trade-offs (cost, complexity, management)
    And maintains conversation context from previous messages
```

#### US-002: TCO Calculation

```
As an Enterprise CTO,
I want to get a real-time cost comparison across cloud providers,
So that I can make a data-driven decision on which provider to choose.
```

**Acceptance Criteria:**

```gherkin
Feature: TCO Calculator

  Scenario: Multi-provider comparison
    Given a CTO asks "Compare costs for 50 VMs: 8 vCPU, 32GB RAM, 500GB SSD"
    When the Cost Calculator Agent processes the request
    Then it shows monthly TCO for Cloud.ru, Yandex Cloud, and VK Cloud
    And displays a formatted comparison table
    And highlights the cost leader with percentage difference
    And includes 1-year and 3-year projections with volume discounts

  Scenario: Cost breakdown by category
    Given a CTO asks "Break down costs for a Kubernetes cluster with 10 nodes"
    When the Cost Calculator Agent processes the request
    Then it shows compute, storage, networking, and management costs separately
    And provides total monthly and annual estimates
    And notes any hidden costs (egress, support tiers)

  Scenario: Pricing data unavailable
    Given pricing for a specific service is not in the RAG corpus
    When the Cost Calculator Agent cannot provide accurate pricing
    Then it clearly states "I don't have current pricing for service X"
    And suggests contacting sales for a custom quote
    And does not hallucinate pricing numbers
```

#### US-003: Compliance Advisory

```
As an Enterprise CTO processing personal data,
I want to verify that a cloud provider meets 152-ФЗ requirements,
So that I can ensure regulatory compliance for my workload.
```

**Acceptance Criteria:**

```gherkin
Feature: Compliance Advisory

  Scenario: 152-ФЗ compliance check
    Given a CTO asks "Does Cloud.ru meet 152-ФЗ for processing personal data?"
    When the Compliance Agent processes the request
    Then it confirms Cloud.ru's compliance status
    And lists specific certifications and security measures
    And recommends appropriate security level (УЗ-1/2/3/4)
    And cites official documentation sources

  Scenario: ФСТЭК requirements
    Given a CTO asks about ФСТЭК certification for government data
    When the Compliance Agent processes the request
    Then it explains applicable ФСТЭК levels
    And maps Cloud.ru services to required security measures
    And identifies any gaps requiring additional configuration

  Scenario: CII workload requirements
    Given a CTO has Critical Information Infrastructure workload
    When they describe their CII classification
    Then the Compliance Agent explains mandatory requirements
    And provides a checklist of necessary security controls
    And flags services that need additional certification
```

### Epic 2: Multi-Channel Delivery

#### US-006: Telegram Bot

```
As an Enterprise CTO,
I want to consult with the AI via Telegram,
So that I can get answers on my preferred communication platform.
```

**Acceptance Criteria:**

```gherkin
Feature: Telegram Bot

  Scenario: Start consultation
    Given a user opens the Telegram bot
    When they send /start
    Then the bot greets them with available capabilities
    And asks what they need help with
    And supports Russian language by default

  Scenario: Rich message formatting
    Given the AI generates a TCO comparison table
    When sending to Telegram
    Then tables are formatted with monospace or as images
    And long responses are split into readable chunks
    And inline buttons offer "Get PDF" or "Continue"

  Scenario: Session continuity
    Given a user had a consultation yesterday
    When they return today and ask "What about the migration plan?"
    Then the bot restores previous conversation context
    And continues from where they left off
```

#### US-008: Web Chat Widget

```
As a website visitor on cloud.ru,
I want to start a consultation via an embedded chat widget,
So that I can get answers without leaving the website.
```

**Acceptance Criteria:**

```gherkin
Feature: Web Chat Widget

  Scenario: Widget initialization
    Given a visitor lands on cloud.ru
    When the page loads
    Then a chat bubble appears in the bottom-right corner
    And clicking it opens the chat panel
    And the greeting message appears within 1 second

  Scenario: Proactive engagement
    Given a visitor has been on the pricing page for 60+ seconds
    When the proactive trigger fires
    Then the widget shows "Need help calculating costs for your workload?"
    And clicking it opens a pre-filled consultation

  Scenario: Lead capture
    Given a visitor completes a consultation with architecture + TCO
    When the AI detects high purchase intent
    Then it asks for contact details (name, company, email)
    And creates a lead in the CRM with full consultation transcript
```

### Epic 3: Admin Dashboard & Analytics

#### US-010: Consultation Metrics

```
As a Cloud Sales Director,
I want to see real-time consultation metrics on a dashboard,
So that I can track pipeline health and AI performance.
```

**Acceptance Criteria:**

```gherkin
Feature: Admin Dashboard

  Scenario: Daily overview
    Given a Sales Director logs into the admin dashboard
    When they view the main page
    Then they see today's metrics: consultations, leads, avg response time
    And a 7-day trend chart
    And top consultation topics

  Scenario: ROI calculation
    Given 30 days of consultation data exists
    When the Sales Director views ROI analytics
    Then it shows: time saved (SA hours), leads generated, estimated pipeline value
    And compares AI cost (₽100-140K/mo) vs equivalent SA cost
    And displays ROI as percentage and absolute numbers
```

### Epic 4: Human Escalation

#### US-014: Seamless Handoff

```
As an Enterprise CTO,
I want to be transferred to a human expert when the AI can't help,
So that I always get the answer I need regardless of complexity.
```

**Acceptance Criteria:**

```gherkin
Feature: Human Escalation

  Scenario: Low confidence escalation
    Given the AI's confidence score drops below 0.6
    When it detects it cannot adequately help
    Then it says "This requires specialized expertise. Let me connect you with our SA."
    And creates an escalation ticket with full conversation transcript
    And sends notification to available SA via Telegram/email

  Scenario: User-requested escalation
    Given a user types "I want to talk to a human"
    When the escalation is triggered
    Then the handoff happens within 30 seconds during business hours
    And outside business hours, a callback is scheduled
    And the SA receives complete conversation context

  Scenario: SA context preservation
    Given an escalation is triggered
    When the SA receives the ticket
    Then they see: conversation transcript, detected intent, recommended architecture, TCO data
    And can continue the conversation in the same Telegram thread
```

---

## Non-Functional Requirements (Detailed)

### Performance Requirements

| Metric | MVP Target | Production Target | Enterprise Target |
|--------|:---:|:---:|:---:|
| Simple query response (p50) | < 5s | < 3s | < 2s |
| Complex query response (p99) | < 30s | < 20s | < 15s |
| RAG retrieval (p50) | < 2s | < 1s | < 500ms |
| Dashboard page load | < 3s | < 2s | < 1s |
| Concurrent dialogues | 20 | 100 | 500 |
| RAG corpus size | 6K pages | 20K pages | 100K+ pages |

### Security Requirements

| Requirement | Standard | Implementation |
|-------------|----------|----------------|
| Data at rest | AES-256 | PostgreSQL TDE + encrypted volumes |
| Data in transit | TLS 1.3 | Nginx termination, internal mTLS |
| Authentication (admin) | OAuth2 + JWT | Keycloak or custom auth service |
| Authentication (user) | Telegram OAuth | Telegram Bot API login widget |
| Authorization | RBAC | Roles: superadmin, admin, agent_manager, viewer |
| Audit logging | All actions logged | Structured logs with user, action, timestamp |
| PII handling | 152-ФЗ compliant | Russian data center, 90-day anonymization |
| Secret management | No plaintext secrets | Docker secrets / Vault |
| Rate limiting | Per-user and global | Token bucket: 30 req/min per user, 1000 req/min global |

### Reliability Requirements

| Metric | Target | Measurement |
|--------|--------|-------------|
| Uptime | 99.5% (production), 99.9% (enterprise) | Monthly, excluding planned maintenance |
| RTO | 4 hours (production), 1 hour (enterprise) | Time to restore service |
| RPO | 1 hour | Maximum data loss window |
| Backup frequency | Daily full + hourly incremental | PostgreSQL + vector DB |
| Health checks | Every 30 seconds | Liveness + readiness probes |

---

## Success Metrics

| Metric | MVP Target (M3) | v1.0 Target (M6) | v2.0 Target (M15) |
|--------|:---:|:---:|:---:|
| Monthly consultations | 200 | 1,000 | 5,000 |
| Avg response time | < 30s | < 15s | < 10s |
| Consultation → lead conversion | 20% | 35% | 40% |
| Client NPS | > 50 | > 65 | > 75 |
| SA time saved | 50% | 65% | 75% |
| Pilot → paid conversion | 80% | 85% | 90% |
| RAG answer accuracy | 80% | 90% | 95% |
| Human escalation rate | 30% | 15% | 8% |
