# Pseudocode — AI-Консультант Cloud.ru

## Data Structures

### Conversation

```
type Conversation = {
  id: UUID
  tenant_id: UUID              // cloud provider (multi-tenant)
  channel: "telegram" | "web_widget" | "crm"
  channel_user_id: string      // Telegram user ID, session ID, etc.
  status: "active" | "escalated" | "completed" | "archived"
  messages: Message[]
  context: ConversationContext
  lead: Lead | null
  created_at: Timestamp
  updated_at: Timestamp
}

type Message = {
  id: UUID
  conversation_id: UUID
  role: "user" | "assistant" | "system" | "agent"
  agent_type: AgentType | null  // which agent responded
  content: string
  metadata: {
    confidence: float           // 0.0 - 1.0
    sources: Source[]           // RAG source references
    tool_calls: ToolCall[]      // MCP tool invocations
    response_time_ms: int
  }
  created_at: Timestamp
}

type ConversationContext = {
  detected_intent: Intent
  workload_description: string | null
  compliance_requirements: string[]
  budget_range: string | null
  timeline: string | null
  company_name: string | null
  company_size: string | null
  current_infrastructure: string | null
}
```

### Agent System

```
type AgentType = "architect" | "cost_calculator" | "compliance"
               | "migration" | "ai_factory" | "human_escalation"

type Agent = {
  type: AgentType
  name: string
  description: string
  system_prompt: string
  tools: MCPTool[]             // available MCP tools
  rag_collections: string[]    // which RAG collections to search
  confidence_threshold: float  // below this → escalate
  max_turns: int               // max dialogue turns before escalation
}

type MCPTool = {
  name: string
  description: string
  input_schema: JSONSchema
  handler: string              // MCP server endpoint
}

type AgentResponse = {
  content: string
  confidence: float
  sources: Source[]
  tool_results: ToolResult[]
  should_escalate: boolean
  suggested_next_agent: AgentType | null
}
```

### RAG Pipeline

```
type Document = {
  id: UUID
  tenant_id: UUID
  collection: string           // "cloud_ru_docs", "pricing", "compliance"
  title: string
  content: string
  metadata: {
    source_url: string
    last_updated: Timestamp
    category: string
    provider: string           // "cloud_ru", "yandex", "vk"
  }
  embedding: float[1536]       // vector embedding
  chunk_id: int                // chunk index within document
}

type RAGQuery = {
  query: string
  collections: string[]
  top_k: int                   // default 5
  min_similarity: float        // default 0.7
  filters: {
    tenant_id: UUID
    provider: string | null
    category: string | null
  }
}

type RAGResult = {
  documents: Document[]
  scores: float[]
  query_embedding: float[1536]
}
```

### Lead & Analytics

```
type Lead = {
  id: UUID
  tenant_id: UUID
  conversation_id: UUID
  contact: {
    name: string | null
    company: string | null
    email: string | null
    phone: string | null
    telegram_username: string | null
  }
  qualification: "cold" | "warm" | "hot" | "qualified"
  intent: Intent
  estimated_deal_value: float | null
  architecture_summary: string | null
  tco_data: TCOComparison | null
  compliance_requirements: string[]
  crm_external_id: string | null   // Bitrix24/amoCRM deal ID
  created_at: Timestamp
}

type Intent = "migration" | "new_deployment" | "cost_optimization"
            | "compliance_check" | "gpu_ai" | "general_inquiry"

type TCOComparison = {
  workload_description: string
  providers: {
    name: string
    monthly_cost: float
    annual_cost: float
    three_year_cost: float
    breakdown: { category: string, cost: float }[]
  }[]
  recommended: string
  savings_vs_current: float | null
}

type ConsultationMetric = {
  id: UUID
  tenant_id: UUID
  date: Date
  total_consultations: int
  avg_response_time_ms: int
  leads_generated: int
  escalations: int
  satisfaction_score: float | null
  top_intents: { intent: Intent, count: int }[]
}
```

---

## Core Algorithms

### Algorithm: Orchestrator — Route User Message to Agent

```
INPUT: conversation: Conversation, user_message: string
OUTPUT: AgentResponse

STEPS:
1. APPEND user_message to conversation.messages
2. intent = DETECT_INTENT(user_message, conversation.context)
3. UPDATE conversation.context.detected_intent = intent

4. // Determine which agent should handle
   agent_type = SELECT_AGENT(intent, conversation)

   FUNCTION SELECT_AGENT(intent, conversation):
     // Check for explicit escalation request
     IF user_message matches escalation_patterns ("человек", "оператор", "помощь"):
       RETURN "human_escalation"

     // Route by intent
     MATCH intent:
       "migration"          → RETURN "architect"  // then "migration" as follow-up
       "new_deployment"     → RETURN "architect"
       "cost_optimization"  → RETURN "cost_calculator"
       "compliance_check"   → RETURN "compliance"
       "gpu_ai"             → RETURN "ai_factory"
       "general_inquiry"    → RETURN "architect"  // default technical agent

     // If conversation already has an active agent, continue with it
     IF conversation has recent agent context:
       RETURN conversation.last_agent_type

5. agent = LOAD_AGENT(agent_type)

6. // Build prompt with RAG context
   rag_results = RAG_SEARCH(
     query = user_message,
     collections = agent.rag_collections,
     filters = { tenant_id: conversation.tenant_id }
   )

7. prompt = BUILD_PROMPT(
     system = agent.system_prompt,
     rag_context = rag_results.documents,
     conversation_history = conversation.messages[-20:],  // last 20 messages
     tools = agent.tools
   )

8. // Call LLM with MCP tools
   llm_response = LLM_CALL(prompt, tools = agent.tools)

9. // Process tool calls if any
   WHILE llm_response.has_tool_calls:
     FOR tool_call IN llm_response.tool_calls:
       result = EXECUTE_MCP_TOOL(tool_call)
       llm_response = LLM_CONTINUE(result)

10. // Calculate confidence
    confidence = CALCULATE_CONFIDENCE(
      rag_scores = rag_results.scores,
      llm_response = llm_response,
      tool_success = all tool calls succeeded
    )

11. // Check if escalation needed
    IF confidence < agent.confidence_threshold:
      RETURN ESCALATE_TO_HUMAN(conversation, reason = "low_confidence")

    IF conversation.messages.length > agent.max_turns * 2:
      RETURN ESCALATE_TO_HUMAN(conversation, reason = "max_turns_exceeded")

12. // Build response
    response = AgentResponse {
      content: llm_response.text,
      confidence: confidence,
      sources: rag_results.documents.map(d => d.metadata.source_url),
      tool_results: llm_response.tool_results,
      should_escalate: false,
      suggested_next_agent: DETECT_NEXT_AGENT(llm_response)
    }

13. APPEND response to conversation.messages
14. ASYNC: CHECK_LEAD_QUALIFICATION(conversation)
15. RETURN response

COMPLEXITY: O(n) where n = conversation length (for context window)
```

### Algorithm: RAG Search with Hybrid Retrieval

```
INPUT: query: RAGQuery
OUTPUT: RAGResult

STEPS:
1. // Generate query embedding
   query_embedding = EMBED(query.query)  // e.g., text-embedding-3-small

2. // Vector similarity search
   vector_results = VECTOR_DB.search(
     collection = query.collections,
     embedding = query_embedding,
     top_k = query.top_k * 2,  // over-fetch for reranking
     filters = query.filters,
     min_similarity = query.min_similarity
   )

3. // Keyword search (BM25) for hybrid
   keyword_results = KEYWORD_SEARCH(
     query = query.query,
     collections = query.collections,
     top_k = query.top_k * 2,
     filters = query.filters
   )

4. // Reciprocal Rank Fusion (RRF) to merge results
   merged = RRF_MERGE(vector_results, keyword_results, k = 60)

5. // Rerank with cross-encoder (if available)
   IF RERANKER_AVAILABLE:
     reranked = RERANK(query.query, merged, top_k = query.top_k)
   ELSE:
     reranked = merged[:query.top_k]

6. RETURN RAGResult {
     documents: reranked.documents,
     scores: reranked.scores,
     query_embedding: query_embedding
   }

COMPLEXITY: O(log n) for vector search + O(n) for BM25 + O(k log k) for merge
```

### Algorithm: TCO Calculation

```
INPUT: workload: WorkloadSpec, providers: string[]
OUTPUT: TCOComparison

type WorkloadSpec = {
  vms: { count: int, vcpu: int, ram_gb: int, disk_gb: int, disk_type: string }[]
  storage: { type: string, size_tb: float } | null
  networking: { egress_gb_month: float } | null
  managed_services: string[]  // e.g., "kubernetes", "postgresql", "redis"
  period: "monthly" | "annual" | "three_year"
}

STEPS:
1. results = []
2. FOR EACH provider IN providers:
     pricing = LOAD_PRICING(provider)  // from RAG or MCP tool

     // Calculate compute costs
     compute_cost = 0
     FOR EACH vm IN workload.vms:
       sku = MATCH_SKU(provider, vm.vcpu, vm.ram_gb)
       IF sku NOT FOUND:
         compute_cost += ESTIMATE_FROM_CLOSEST(provider, vm)
         FLAG as "estimated"
       ELSE:
         compute_cost += sku.price_monthly * vm.count

     // Calculate storage costs
     storage_cost = 0
     IF workload.storage:
       storage_sku = MATCH_STORAGE_SKU(provider, workload.storage.type)
       storage_cost = storage_sku.price_per_gb * workload.storage.size_tb * 1024

     // Calculate disk costs for VMs
     FOR EACH vm IN workload.vms:
       disk_sku = MATCH_DISK_SKU(provider, vm.disk_type)
       storage_cost += disk_sku.price_per_gb * vm.disk_gb * vm.count

     // Calculate networking costs
     network_cost = 0
     IF workload.networking:
       network_cost = CALC_EGRESS(provider, workload.networking.egress_gb_month)

     // Calculate managed service costs
     managed_cost = 0
     FOR EACH service IN workload.managed_services:
       managed_sku = MATCH_MANAGED_SKU(provider, service)
       managed_cost += managed_sku.price_monthly

     // Apply volume discounts
     total_monthly = compute_cost + storage_cost + network_cost + managed_cost
     IF workload.period == "annual":
       total_monthly *= ANNUAL_DISCOUNT(provider)  // typically 10-20% off
     IF workload.period == "three_year":
       total_monthly *= THREE_YEAR_DISCOUNT(provider)  // typically 20-40% off

     results.APPEND({
       name: provider,
       monthly_cost: total_monthly,
       annual_cost: total_monthly * 12,
       three_year_cost: total_monthly * 36,
       breakdown: [
         { category: "Compute", cost: compute_cost },
         { category: "Storage", cost: storage_cost },
         { category: "Networking", cost: network_cost },
         { category: "Managed Services", cost: managed_cost }
       ]
     })

3. // Sort by monthly cost
   results.SORT_BY(monthly_cost, ASC)
   recommended = results[0].name

4. RETURN TCOComparison {
     workload_description: SUMMARIZE(workload),
     providers: results,
     recommended: recommended,
     savings_vs_current: null  // calculated if current costs provided
   }

COMPLEXITY: O(p * v) where p = providers, v = VMs
```

### Algorithm: Lead Qualification

```
INPUT: conversation: Conversation
OUTPUT: Lead (updated qualification)

STEPS:
1. // Score conversation signals
   score = 0

   // Intent signals
   IF conversation has architecture discussion: score += 20
   IF conversation has TCO calculation: score += 25
   IF conversation has compliance check: score += 15
   IF conversation has migration plan: score += 20

   // Engagement signals
   IF conversation.messages.length > 10: score += 10
   IF user asked follow-up questions: score += 10
   IF user provided company details: score += 15
   IF user asked about pricing/contracts: score += 20
   IF user mentioned timeline: score += 15

   // Negative signals
   IF user seems to be just browsing: score -= 20
   IF user is a competitor researching: score -= 50

2. // Classify
   qualification = MATCH score:
     0-20   → "cold"
     21-40  → "warm"
     41-65  → "hot"
     66+    → "qualified"

3. // Extract contact info from conversation
   contact = EXTRACT_CONTACT_INFO(conversation.messages)

4. // Create or update lead
   lead = UPSERT_LEAD({
     tenant_id: conversation.tenant_id,
     conversation_id: conversation.id,
     contact: contact,
     qualification: qualification,
     intent: conversation.context.detected_intent,
     architecture_summary: EXTRACT_ARCHITECTURE(conversation),
     tco_data: EXTRACT_TCO(conversation),
     compliance_requirements: conversation.context.compliance_requirements
   })

5. // Push to CRM if qualified
   IF qualification IN ("hot", "qualified") AND tenant.crm_enabled:
     CRM_CREATE_DEAL(tenant.crm_config, lead)

6. RETURN lead

COMPLEXITY: O(m) where m = messages in conversation
```

### Algorithm: Human Escalation

```
INPUT: conversation: Conversation, reason: string
OUTPUT: AgentResponse

STEPS:
1. // Prepare escalation context
   summary = SUMMARIZE_CONVERSATION(conversation)
   context = {
     customer_intent: conversation.context.detected_intent,
     workload: conversation.context.workload_description,
     compliance: conversation.context.compliance_requirements,
     tco_data: EXTRACT_TCO(conversation),
     architecture: EXTRACT_ARCHITECTURE(conversation),
     reason: reason,
     confidence_scores: GET_CONFIDENCE_HISTORY(conversation)
   }

2. // Find available SA
   available_sas = GET_AVAILABLE_SAS(conversation.tenant_id)

   IF available_sas.length == 0:
     // Outside business hours or all busy
     SCHEDULE_CALLBACK(conversation, next_business_hour())
     RETURN AgentResponse {
       content: "К сожалению, все специалисты сейчас заняты. " +
                "Я запланировал обратный звонок. Когда вам удобно?",
       should_escalate: true
     }

3. // Assign to SA
   sa = SELECT_BEST_SA(available_sas, conversation.context)

4. // Notify SA
   SEND_NOTIFICATION(sa, {
     type: "escalation",
     conversation_id: conversation.id,
     summary: summary,
     context: context,
     priority: IF reason == "user_request" THEN "high" ELSE "medium"
   })

5. // Update conversation status
   conversation.status = "escalated"

6. RETURN AgentResponse {
     content: "Подключаю специалиста " + sa.name + ". " +
              "Я передал всю информацию о нашем разговоре, " +
              "так что вам не придётся повторять.",
     confidence: 1.0,
     should_escalate: true
   }

COMPLEXITY: O(s) where s = available SAs
```

---

## API Contracts

### POST /api/v1/conversations

Create a new conversation.

```
Request:
  Headers: { Authorization: Bearer <tenant_api_key> }
  Body: {
    channel: "telegram" | "web_widget" | "crm",
    channel_user_id: string,
    initial_message: string | null
  }

Response (201):
  {
    data: {
      id: UUID,
      status: "active",
      channel: string,
      created_at: Timestamp
    }
  }

Response (401):
  { error: { code: "AUTH_REQUIRED", message: "Invalid or missing API key" } }

Response (429):
  { error: { code: "RATE_LIMITED", message: "Too many requests" } }
```

### POST /api/v1/conversations/:id/messages

Send a message in a conversation.

```
Request:
  Headers: { Authorization: Bearer <tenant_api_key> }
  Body: {
    content: string,
    role: "user"
  }

Response (200):
  {
    data: {
      user_message: { id: UUID, content: string, created_at: Timestamp },
      assistant_response: {
        id: UUID,
        content: string,
        agent_type: string,
        confidence: float,
        sources: [{ title: string, url: string }],
        created_at: Timestamp
      }
    },
    meta: {
      response_time_ms: int,
      tokens_used: int
    }
  }

Response (404):
  { error: { code: "NOT_FOUND", message: "Conversation not found" } }
```

### GET /api/v1/dashboard/metrics

Get consultation metrics for dashboard.

```
Request:
  Headers: { Authorization: Bearer <admin_jwt> }
  Query: {
    period: "today" | "7d" | "30d" | "custom",
    start_date: Date | null,
    end_date: Date | null
  }

Response (200):
  {
    data: {
      total_consultations: int,
      leads_generated: int,
      avg_response_time_ms: int,
      escalation_rate: float,
      satisfaction_score: float | null,
      conversion_rate: float,
      top_intents: [{ intent: string, count: int, percentage: float }],
      daily_trend: [{ date: Date, consultations: int, leads: int }]
    }
  }
```

### POST /api/v1/webhooks/telegram

Telegram webhook endpoint.

```
Request:
  Body: Telegram Update object (as per Bot API spec)

Response (200):
  {} // empty — responses sent async via Telegram API

Processing:
  1. Parse Telegram Update
  2. Extract chat_id, user_id, message text
  3. Find or create Conversation for this chat_id
  4. Route to Orchestrator
  5. Send response via Telegram Bot API sendMessage
```

### POST /api/v1/agents/:type/config

Update agent configuration.

```
Request:
  Headers: { Authorization: Bearer <admin_jwt> }
  Body: {
    system_prompt: string | null,
    confidence_threshold: float | null,
    max_turns: int | null,
    rag_collections: string[] | null,
    tools: string[] | null
  }

Response (200):
  { data: { agent_type: string, updated_at: Timestamp } }
```

---

## State Transitions

### Conversation State Machine

```
                    ┌──────────┐
                    │  active  │
                    └────┬─────┘
                         │
              ┌──────────┼──────────┐
              │          │          │
              ▼          ▼          ▼
        ┌──────────┐ ┌────────┐ ┌──────────┐
        │escalated │ │completed│ │ timeout  │
        └────┬─────┘ └────────┘ └────┬─────┘
             │                       │
             ▼                       ▼
        ┌──────────┐           ┌──────────┐
        │completed │           │ archived │
        └──────────┘           └──────────┘

Transitions:
  active → escalated:   confidence < threshold OR user requests human
  active → completed:   user ends conversation OR lead is qualified
  active → timeout:     no messages for 24 hours
  escalated → completed: SA resolves the inquiry
  timeout → archived:   after 7 days with no activity
```

### Lead Qualification State Machine

```
  ┌──────┐  score 21+  ┌──────┐  score 41+  ┌─────┐  score 66+  ┌───────────┐
  │ cold │ ──────────→ │ warm │ ──────────→ │ hot │ ──────────→ │ qualified │
  └──────┘             └──────┘             └─────┘             └───────────┘
                                                                      │
                                                                      ▼
                                                                ┌──────────┐
                                                                │ CRM Deal │
                                                                └──────────┘
```

---

## Error Handling Strategy

| Error Category | Error Code | HTTP | Trigger | Action |
|----------------|-----------|:----:|---------|--------|
| Authentication | AUTH_001 | 401 | Missing/invalid API key | Return error, log attempt |
| Authentication | AUTH_002 | 403 | Insufficient permissions | Return error, log |
| Rate Limiting | RATE_001 | 429 | Per-user limit exceeded | Return retry-after header |
| Rate Limiting | RATE_002 | 429 | Global limit exceeded | Return retry-after header |
| LLM Error | LLM_001 | 502 | LLM API timeout | Retry 2x, then fallback message |
| LLM Error | LLM_002 | 502 | LLM API error | Switch to fallback model, log |
| RAG Error | RAG_001 | 500 | Vector DB unavailable | Use cached results or acknowledge gap |
| RAG Error | RAG_002 | 200 | No relevant documents found | Acknowledge, suggest alternative query |
| MCP Error | MCP_001 | 502 | MCP tool call failed | Skip tool, note limitation in response |
| CRM Error | CRM_001 | 502 | CRM sync failed | Queue for retry, log |
| Validation | VAL_001 | 400 | Invalid input | Return field-level errors |
| Not Found | NOT_001 | 404 | Resource not found | Return error |
| Conversation | CONV_001 | 409 | Conversation already completed | Return error, suggest new conversation |
