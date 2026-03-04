# User Flows

This document describes the key user journeys through the AI Consultant Cloud.ru platform, covering both end-user and administrator workflows.

---

## 1. Admin Login Flow

**Actor:** Administrator
**Channel:** Web browser (Admin Dashboard)

```
1. Admin opens https://consultant.example.com (or http://localhost:3000)
2. System displays the login page with email and password fields
3. Admin enters credentials:
   - Email: admin@cloud.ru
   - Password: (configured password)
4. System sends POST /api/v1/auth/login with email and password
5. API validates credentials:
   - If admin_password_hash is configured: verify against bcrypt hash
   - If not configured (dev mode): accept "admin123admin"
6. API returns JWT token (access_token, token_type, expires_in)
7. Dashboard stores the token in browser storage
8. System redirects to the main Dashboard page (/)
9. All subsequent API requests include Authorization: Bearer <token>
```

**Error path:** Invalid credentials return HTTP 401. The login form shows "Invalid email or password."

**Token expiration:** After 60 minutes, the token expires. The dashboard detects 401 responses and redirects back to the login page.

---

## 2. VMware Migration Consultation (Telegram)

**Actor:** IT Manager at a company with VMware infrastructure
**Channel:** Telegram

```
1. User finds the bot in Telegram and sends /start
2. Bot responds with a welcome message explaining available consultation topics
3. User sends: "We have 150 VMware VMs and need to migrate to the cloud"
4. System processes the message:
   a. Webhook receives the Telegram update (POST /api/v1/webhooks/telegram)
   b. Orchestrator detects intent: "migration"
   c. Orchestrator routes to the Migration Agent
5. Migration Agent queries RAG pipeline:
   a. Searches migration_playbooks and case_studies collections
   b. Retrieves relevant VMware-to-cloud migration guides
6. Agent asks clarifying questions:
   - "What VMware version are you running (vSphere 7/8)?"
   - "What are the VM sizes (CPU/RAM ranges)?"
   - "Do you have any compliance requirements (152-FZ)?"
   - "What is your target migration timeline?"
7. User answers each question in the conversation
8. Agent generates a migration plan:
   - Phase 1: Assessment and planning (2 weeks)
   - Phase 2: Pilot migration of 10 non-critical VMs (2 weeks)
   - Phase 3: Batch migration of remaining VMs (6-8 weeks)
   - Phase 4: Validation and cutover (1 week)
9. Agent provides estimated costs (delegates to Cost Calculator tools)
10. Confidence score: 0.82 (above threshold -- no escalation needed)
11. System qualifies the user as a lead:
    - Qualification: "hot" (budget + timeline + decision-maker signals)
    - Estimated deal value calculated from VM count and sizing
12. Lead is saved to the database and optionally synced to CRM
```

---

## 3. TCO Calculation Flow

**Actor:** CFO or IT Director evaluating cloud costs
**Channel:** Telegram or Web Widget

```
1. User sends: "Calculate TCO for migrating our on-premise database cluster"
2. Orchestrator detects intent: "cost_estimation"
3. Orchestrator routes to the Cost Calculator Agent
4. Agent asks for infrastructure details:
   - "What database engine? (PostgreSQL, MySQL, MS SQL, Oracle)"
   - "Current configuration: CPU cores, RAM, storage?"
   - "Expected data growth per year?"
   - "High availability requirements? (single, HA, multi-region)"
   - "Desired commitment term? (on-demand, 1 year, 3 years)"
5. User provides: "PostgreSQL, 16 cores, 128 GB RAM, 5 TB storage, 20% annual growth, HA required, 1 year commitment"
6. Agent retrieves Cloud.ru pricing via MCP tools:
   a. Calls pricing_lookup for managed PostgreSQL service
   b. Calls discount_calculator for 1-year commitment discount
   c. Calls tco_templates for comparison framework
7. Agent generates TCO report:
   - Current on-premise cost (hardware, licensing, ops staff)
   - Cloud.ru monthly cost breakdown:
     - Compute: X RUB/month
     - Storage: Y RUB/month
     - Network: Z RUB/month
     - HA standby: W RUB/month
   - Annual total with commitment discount
   - 3-year TCO comparison (on-premise vs cloud)
   - Break-even analysis
8. Agent presents the formatted report to the user
9. User asks follow-up: "What if we add read replicas?"
10. Agent recalculates with additional read replica costs
11. Confidence score: 0.88 -- no escalation
12. If the user shows buying intent, lead is created with tco_data JSONB populated
```

---

## 4. Compliance Check Flow

**Actor:** Chief Information Security Officer (CISO)
**Channel:** Any (Telegram, Web Widget, or CRM)

```
1. User sends: "Does Cloud.ru support 152-FZ for storing personal data?"
2. Orchestrator detects intent: "compliance"
3. Orchestrator routes to the Compliance Agent
4. Agent queries RAG collections:
   a. Searches compliance_docs for 152-FZ documentation
   b. Searches regulatory_updates for recent changes
5. Agent provides initial response:
   - Confirms Cloud.ru data centers are in Moscow (152-FZ compliant)
   - Lists relevant certifications (FSTEC, FSB)
   - Outlines data protection measures available
6. Agent asks: "What types of personal data will you store?"
7. User responds: "Customer PII -- names, phone numbers, addresses, payment data"
8. Agent calls compliance_checker MCP tool with data categories
9. Agent provides detailed compliance guidance:
   - Required security controls for each data category
   - Recommended Cloud.ru services for data protection
   - Encryption requirements (at rest and in transit)
   - Audit logging requirements
   - Data retention and deletion policies
10. Agent asks: "Do you need FSTEC Level 2 or Level 3 certification?"
11. User responds, agent provides specific requirements for that level
12. Confidence score: 0.75 -- sufficient for automated response
13. Agent suggests: "For detailed compliance audit assistance, I can connect you with a certified specialist."
14. Lead created with compliance_requirements array populated
```

---

## 5. Human Escalation Flow

**Actor:** User with a question outside agent capabilities
**Channel:** Any

```
1. User sends a complex or ambiguous question:
   "We need a hybrid setup with some workloads on-premise and some in the cloud,
    with real-time data sync and failover. Our budget is 50M RUB."
2. Orchestrator processes the message:
   a. Intent detection returns mixed signals (architecture + migration + cost)
   b. Orchestrator selects Architect Agent as primary
3. Architect Agent processes the query:
   a. RAG retrieval confidence: 0.45 (limited hybrid cloud documentation)
   b. Agent generates a partial response
   c. Confidence score: 0.52 (below 0.60 threshold)
4. Orchestrator triggers escalation:
   a. Routes to Human Escalation Agent
   b. Escalation Agent calls sa_availability MCP tool to find available SA
   c. Escalation Agent calls notification_sender to alert the SA team
5. System updates conversation status to "escalated"
6. User receives message:
   "Your question requires expert consultation. I've forwarded your conversation
    to a solutions architect who will respond within 2 hours during business hours.
    Here's a summary of what we've discussed so far: [summary]"
7. Human SA receives:
   - Full conversation history
   - Detected intents and partial analysis
   - User's stated requirements and budget
   - Confidence scores and reason for escalation
8. SA responds in the same channel (Telegram/web/CRM)
9. Conversation continues with human SA (status remains "escalated")
```

**Automatic escalation triggers:**
- Confidence score below 0.60
- User explicitly requests a human ("let me talk to a person")
- Conversation exceeds 20 turns without resolution
- Agent detects sensitive commercial negotiation

---

## 6. Lead Qualification Flow

**Actor:** System (automated process during any consultation)
**Channel:** Internal (no direct user interaction)

```
1. During any consultation, the orchestrator monitors for qualification signals
2. Signal detection (checked after each user message):
   a. Company name or industry mentioned → +1 signal
   b. Budget or spending amount mentioned → +1 signal
   c. Timeline or deadline mentioned → +1 signal
   d. Decision-making authority implied → +1 signal
   e. Specific infrastructure size mentioned → +1 signal
3. When signals reach threshold:
   - 1-2 signals → qualification: "cold"
   - 3 signals → qualification: "warm"
   - 4 signals → qualification: "hot"
   - 4+ signals with explicit budget and timeline → "qualified"
4. System creates or updates lead record:
   - Extracts contact info from conversation (if provided)
   - Records detected intent
   - Calculates estimated_deal_value from infrastructure sizing and pricing
   - Stores architecture_summary from Architect Agent output
   - Stores tco_data from Cost Calculator Agent output
   - Stores compliance_requirements from Compliance Agent output
5. If CRM integration is configured:
   a. Calls crm-server MCP tool (lead_create or deal_update)
   b. Syncs lead to Bitrix24 or amoCRM
   c. Stores crm_external_id for future updates
6. Lead appears in the admin dashboard Leads page
7. For "hot" and "qualified" leads:
   - Notification sent to sales team
   - Lead flagged for priority follow-up
```

---

## 7. Dashboard Monitoring Workflow

**Actor:** Administrator or Manager
**Channel:** Web browser (Admin Dashboard)

```
1. Admin logs in (see Flow #1)
2. Dashboard page (/) loads with default 7-day period
3. Admin reviews summary metrics:
   - Total consultations: trending up or down?
   - Lead generation: meeting targets?
   - Response time: within acceptable limits?
   - Escalation rate: too high (agents may need retraining)?
4. Admin checks daily trend chart:
   - Identifies peak days (marketing campaign effects, seasonal patterns)
   - Spots anomalies (sudden drops may indicate system issues)
5. Admin reviews top intents:
   - "architecture" at 35% → high demand for architecture consulting
   - "cost_estimation" at 25% → active cost comparison phase
   - "compliance" at 20% → regulatory concerns are common
6. Admin navigates to Conversations page:
   - Filters by "escalated" status to review human-handled cases
   - Checks if escalation reasons indicate agent improvement needs
   - Reviews conversation quality for training data
7. Admin navigates to Leads page:
   - Reviews "hot" and "qualified" leads for sales handoff
   - Checks estimated deal values for pipeline forecasting
   - Verifies CRM sync status via crm_external_id
8. Admin navigates to ROI Analytics page:
   - Switches to 30-day period for monthly report
   - Notes SA hours saved (cost justification for the platform)
   - Reviews pipeline value (business impact)
   - Compares channel performance:
     - If web widget has higher conversion → invest in widget placement
     - If Telegram has higher volume → focus on Telegram experience
   - Exports key metrics for management reporting
9. Admin adjusts system if needed:
   - If escalation rate > 20%: review agent prompts, update RAG corpus
   - If response time > 10s: check LLM API latency, optimize prompts
   - If conversion is low: review lead qualification thresholds
```

---

## Flow Dependencies

```
Login Flow ──→ Dashboard Monitoring
                    │
                    ├──→ Conversation Review
                    ├──→ Lead Management
                    └──→ ROI Reporting

User Question ──→ Orchestrator ──→ Agent Selection
                                        │
                     ┌──────────────────┼──────────────────┐
                     │                  │                  │
              Migration Flow     TCO Calculation    Compliance Check
                     │                  │                  │
                     └──────────────────┼──────────────────┘
                                        │
                                  Lead Qualification
                                        │
                                ┌───────┴───────┐
                                │               │
                         CRM Sync      Dashboard Update

Low Confidence ──→ Human Escalation ──→ SA Notification
```
