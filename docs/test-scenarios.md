# BDD Test Scenarios — AI-Консультант Cloud.ru

## Feature: Cloud Architecture Consultation

### Happy Path

```gherkin
Scenario: VMware migration architecture recommendation
  Given a CTO connects via Telegram bot
  And the RAG corpus contains Cloud.ru documentation (6000+ pages)
  When they send "Мне нужно мигрировать 200 серверов VMware в облако"
  Then the Architect Agent responds within 10 seconds
  And asks 2-3 clarifying questions about workload types and specs
  When the CTO provides workload details (web servers, databases, 8vCPU/32GB each)
  Then the agent recommends a target Cloud.ru architecture
  And the response includes specific service names (Cloud Servers, Block Storage, VPC)
  And the response includes estimated resource sizing
  And the response includes at least 2 source references
  And confidence score is >= 0.7
  And total response time is under 30 seconds

Scenario: Follow-up question adjusts recommendation
  Given a CTO received a VM-based architecture recommendation
  When they ask "А если использовать Kubernetes вместо ВМ?"
  Then the Architect Agent adjusts the recommendation to Cloud Containers
  And explains trade-offs (cost, complexity, management overhead)
  And maintains full conversation context from previous messages
  And response time is under 30 seconds
```

### Error Handling

```gherkin
Scenario: Unsupported workload triggers human escalation
  Given a CTO describes a custom FPGA-based ML inference workload
  When the Architect Agent processes the request
  And confidence score drops below 0.6
  Then the agent transparently says "Этот запрос требует специализированной экспертизы"
  And offers to connect with a human Solution Architect
  And creates an escalation ticket with full conversation transcript

Scenario: RAG corpus has no relevant documents
  Given the CTO asks about a very niche Cloud.ru service not in the corpus
  When the RAG search returns 0 results above similarity threshold 0.7
  Then the agent acknowledges the knowledge gap
  And suggests alternative approaches or contacting sales
  And does not hallucinate information
  And response includes disclaimer about data limitations
```

### Edge Cases

```gherkin
Scenario: Empty or whitespace message
  Given a CTO sends an empty message or only whitespace
  Then the bot responds with a friendly prompt
  And asks what they need help with
  And no error is thrown

Scenario: Very long message (10K+ characters)
  Given a CTO sends a message exceeding 4000 characters
  Then the system truncates to 4000 characters
  And notifies the user "Я обработал первые 4000 символов вашего сообщения"
  And processes the truncated message normally

Scenario: Non-Russian language input
  Given a CTO sends a message in English "I need to migrate to cloud"
  Then the agent detects the language
  And responds in English (or user's detected language)
  And provides the same quality of consultation

Scenario: Conversation context exceeds LLM token window
  Given a conversation has 50+ messages totaling 100K+ tokens
  When the CTO sends a new message
  Then the system summarizes older messages (beyond last 20)
  And includes the summary + recent 20 messages in the prompt
  And response quality is maintained
  And no token overflow error occurs
```

---

## Feature: TCO Calculator

### Happy Path

```gherkin
Scenario: Multi-provider cost comparison
  Given a CTO asks "Сравни стоимость 50 ВМ: 8 vCPU, 32GB RAM, 500GB SSD"
  When the Cost Calculator Agent processes the request
  Then the response contains a comparison table with 3 providers
  And Cloud.ru, Yandex Cloud, and VK Cloud are included
  And each provider shows monthly, annual, and 3-year costs
  And the cheapest option is highlighted with percentage difference
  And costs are broken down by category (compute, storage, networking)
  And response time is under 30 seconds

Scenario: Cost breakdown for Kubernetes cluster
  Given a CTO asks "Разбейте стоимость кластера Kubernetes на 10 нод"
  When the Cost Calculator Agent processes the request
  Then compute, storage, networking, and management costs are shown separately
  And total monthly and annual estimates are provided
  And any hidden costs (egress, support tiers) are noted
```

### Error Handling

```gherkin
Scenario: Pricing data unavailable for a service
  Given pricing for Cloud.ru AI Factory GPU instances is not in the RAG corpus
  When the CTO asks about GPU instance pricing
  Then the agent clearly states "У меня нет актуальных данных о стоимости этого сервиса"
  And suggests contacting Cloud.ru sales for a custom quote
  And does NOT hallucinate pricing numbers
  And logs the knowledge gap for corpus update

Scenario: Stale pricing data (>30 days old)
  Given the RAG corpus pricing data was last updated 45 days ago
  When the CTO requests a TCO comparison
  Then the response includes a disclaimer "Данные о ценах могут быть неактуальны (обновлены более 30 дней назад)"
  And still provides the best available comparison
  And recommends verifying with the provider's website
```

### Edge Cases

```gherkin
Scenario: Large TCO request (500+ VMs)
  Given a CTO describes 500 VMs with different configurations
  When the Cost Calculator processes the request
  Then the system processes in batches
  And delivers progressive results (first batch within 30 seconds)
  And the final comparison covers all 500 VMs
  And no timeout or memory error occurs
```

---

## Feature: Compliance Advisory

### Happy Path

```gherkin
Scenario: 152-ФЗ compliance verification
  Given a CTO asks "Обрабатываем персональные данные. Соответствует ли Cloud.ru 152-ФЗ?"
  When the Compliance Agent processes the request
  Then it confirms Cloud.ru's compliance status
  And lists specific certifications and security measures
  And recommends appropriate security level (УЗ-1/2/3/4)
  And cites at least 2 regulatory documents with article numbers
  And response time is under 30 seconds

Scenario: ФСТЭК certification requirements
  Given a CTO asks about ФСТЭК requirements for government data
  When the Compliance Agent processes the request
  Then it explains applicable ФСТЭК levels
  And maps Cloud.ru services to required security controls
  And identifies gaps requiring additional configuration
  And cites at least 2 source references

Scenario: CII workload compliance
  Given a CTO has Critical Information Infrastructure (КИИ) workload
  When they describe their CII classification
  Then the agent explains mandatory requirements per CII category
  And provides a checklist of necessary security controls
  And flags services that need additional certification
  And references the January 2025 CII regulation deadline
```

### Error Handling

```gherkin
Scenario: Ambiguous compliance question
  Given a CTO asks "Нам нужен compliance" without specifying which regulation
  When the Compliance Agent processes the request
  Then it asks clarifying questions (152-ФЗ? ФСТЭК? PCI DSS? CII?)
  And does not assume which regulation applies
```

---

## Feature: Telegram Bot

### Happy Path

```gherkin
Scenario: Start consultation
  Given a user opens the AI-Консультант Telegram bot
  When they send /start
  Then the bot responds with a greeting in Russian within 2 seconds
  And lists available capabilities (architecture, TCO, compliance, migration)
  And offers to start a consultation

Scenario: Rich message formatting
  Given the AI generates a TCO comparison table
  When sending the response to Telegram
  Then tables are formatted as monospace text (code block)
  And responses exceeding 4096 characters are split into multiple messages
  And inline buttons offer "Получить PDF" and "Продолжить"
  And all message parts are delivered in order
```

### Error Handling

```gherkin
Scenario: Telegram API rate limit
  Given the bot has sent many messages in rapid succession
  When Telegram returns a 429 Too Many Requests error
  Then the system queues the message for retry
  And uses exponential backoff (1s, 2s, 4s)
  And the user eventually receives the message
  And no messages are lost

Scenario: LLM API timeout
  Given the LLM API does not respond within 30 seconds
  When the timeout fires
  Then the system retries once with the same request
  If the retry also fails
  Then the bot sends "Извините, сервис временно недоступен. Попробуйте через минуту."
  And logs the error with full context
```

### Edge Cases

```gherkin
Scenario: Session continuity across days
  Given a CTO had a VMware migration consultation yesterday
  And the conversation is still active (within 24-hour window)
  When they return today and ask "Что насчёт плана миграции?"
  Then the bot restores previous conversation context
  And references the previously discussed workload (200 VMware servers)
  And continues from where they left off without asking for repeated info

Scenario: Conversation timeout (24 hours)
  Given a CTO has been inactive for 24 hours
  When the timeout background job runs
  Then the conversation status is set to "timeout"
  And a summary message is sent to the user
  And when the user returns, a new conversation starts
  And the user can reference the old one if needed

Scenario: Same user on multiple channels simultaneously
  Given a CTO has an active Telegram consultation
  And they start a new consultation via the web widget
  Then two separate conversations are created
  And context does NOT bleed between channels
  And each channel maintains its own conversation state
```

---

## Feature: Web Chat Widget

### Happy Path

```gherkin
Scenario: Widget loads on cloud.ru
  Given a visitor navigates to cloud.ru
  When the page fully loads
  Then a chat bubble appears in the bottom-right corner within 1 second
  And clicking it opens the consultation panel
  And a greeting message appears within 1 second of opening

Scenario: Proactive engagement on pricing page
  Given a visitor has been on the cloud.ru pricing page
  When 60 seconds have elapsed
  Then the widget proactively displays "Нужна помощь с расчётом стоимости?"
  And clicking it opens a pre-filled consultation focused on cost estimation
```

### Error Handling

```gherkin
Scenario: Widget fails to load
  Given the widget JavaScript encounters a network error
  Then the widget does not display (fails silently)
  And the main cloud.ru page is not affected
  And an error is logged to the monitoring system
```

---

## Feature: Admin Dashboard

### Happy Path

```gherkin
Scenario: View daily consultation metrics
  Given an admin is logged into the dashboard with valid JWT
  When they view the main page
  Then they see today's consultation count
  And average response time in seconds
  And leads generated count
  And escalation rate as percentage
  And a 7-day trend chart
  And page loads within 3 seconds

Scenario: ROI calculation display
  Given 30 days of consultation data exists in the system
  When the admin navigates to the ROI analytics page
  Then they see total SA hours saved (calculated from consultation count × avg SA time)
  And total leads generated in the period
  And estimated pipeline value in rubles
  And cost comparison: AI cost vs equivalent SA headcount cost
  And ROI displayed as both percentage and absolute rubles
```

### Security

```gherkin
Scenario: RBAC enforcement - viewer cannot modify agents
  Given a user with "viewer" role is logged in
  When they attempt to access the agent configuration page
  Then they receive a 403 Forbidden response
  And the agent configuration UI is not rendered
  And the action is logged in the audit log

Scenario: Invalid JWT token
  Given a user presents an expired or invalid JWT token
  When they make any API request to the dashboard
  Then they receive a 401 Unauthorized response
  And are redirected to the login page
```

---

## Feature: Human Escalation

### Happy Path

```gherkin
Scenario: Low confidence triggers automatic escalation
  Given the AI's confidence score drops below 0.6 during a consultation
  When the escalation threshold is triggered
  Then the bot says "Этот вопрос требует специализированной экспертизы. Подключаю специалиста."
  And creates an escalation ticket with full conversation transcript
  And sends notification to an available SA via Telegram
  And the SA receives: conversation summary, detected intent, architecture data, TCO data

Scenario: User explicitly requests human
  Given a CTO types "Хочу поговорить с человеком"
  When the escalation is triggered
  Then the handoff acknowledgement is sent within 5 seconds
  And during business hours (Mon-Fri 09:00-18:00 MSK), SA connects within 30 seconds
  And outside business hours, a callback is scheduled for next business day
  And the SA receives complete conversation context in the same Telegram thread
```

### Error Handling

```gherkin
Scenario: No SA available during business hours
  Given all SAs are currently busy with other escalations
  When an escalation is triggered
  Then the bot informs the user of the delay
  And estimates wait time
  And offers to continue the AI consultation while waiting
  And the escalation remains in queue
```

---

## Feature: Rate Limiting

```gherkin
Scenario: Per-user rate limit exceeded
  Given a user has sent 30 messages in the last 60 seconds
  When they send the 31st message
  Then the system returns a 429 rate limit response
  And the user-facing message says "Слишком много запросов. Пожалуйста, подождите минуту."
  And includes a Retry-After header
  And the 30 previous messages were all processed normally

Scenario: Global rate limit does not affect individual users unfairly
  Given the global rate limit is 1000 req/min
  And current load is 950 req/min from 50 users
  When a new user sends their first message
  Then it is processed normally (not rejected)
  And per-user fairness is maintained via per-user quotas
```

---

## Feature: Multi-Tenant Data Isolation

```gherkin
Scenario: Tenant A cannot access Tenant B data
  Given Tenant A (Cloud.ru) has 100 conversations
  And Tenant B (Selectel) has 50 conversations
  When Tenant A queries the dashboard API
  Then only Tenant A's 100 conversations are returned
  And no data from Tenant B appears in results
  And RAG search only returns Tenant A's document corpus

Scenario: RAG collections are tenant-isolated
  Given Tenant A's RAG corpus contains Cloud.ru pricing
  And Tenant B's RAG corpus contains Selectel pricing
  When a user on Tenant A asks about pricing
  Then only Cloud.ru pricing documents are retrieved
  And Selectel pricing never appears in the response
```

---

## Feature: Offensive Content Handling

```gherkin
Scenario: Abusive message is rejected
  Given a user sends an offensive or abusive message
  When the content filter processes the message
  Then the bot responds politely "Я помогаю с облачным консалтингом. Чем могу быть полезен?"
  And the offensive message is logged for review
  And the conversation continues normally if the next message is appropriate
  And no agent processing occurs for the offensive message
```

---

## Feature: Webhook Security

```gherkin
Scenario: Valid Telegram webhook with correct signature
  Given the Telegram webhook is configured with a secret token
  When Telegram sends an update with valid X-Telegram-Bot-Api-Secret-Token header
  Then the update is processed normally
  And the conversation receives the message

Scenario: Invalid webhook signature rejected
  Given a malicious actor sends a request to the webhook endpoint
  When the X-Telegram-Bot-Api-Secret-Token header is missing or invalid
  Then the request is rejected with 401
  And the IP is logged for security review
  And no conversation or message is created
```
