# User Guide

## Overview

AI Consultant Cloud.ru is a multi-agent AI platform that automates pre-sales consulting for cloud services. It provides expert-level guidance on cloud architecture, cost estimation, regulatory compliance, migration planning, and AI/ML infrastructure through natural conversation.

You can interact with the platform through three channels:
- **Telegram bot** (primary)
- **Web chat widget** (embedded on websites)
- **CRM integration** (Bitrix24)

---

## Getting Started with the Telegram Bot

### 1. Find the Bot

Search for the bot by its username in Telegram (provided by your organization's administrator) or follow the direct link shared with you.

### 2. Start a Conversation

Send `/start` to the bot. It will greet you and explain the available consultation topics.

### 3. Ask Your Question

Simply type your question in natural language. The system automatically detects your intent and routes the conversation to the appropriate specialist agent.

**Example first messages:**

- "We need to migrate 50 VMware VMs to the cloud. Where do we start?"
- "What will it cost to host a 10TB PostgreSQL database on Cloud.ru?"
- "Does Cloud.ru meet 152-FZ requirements for storing personal data?"
- "We want to deploy a GPU cluster for training LLMs. What are our options?"

---

## Consultation Flow

A typical consultation follows this pattern:

### Step 1: Initial Question

You describe your need or problem. The AI detects your intent and selects the right specialist agent.

### Step 2: Clarifying Questions

The agent may ask follow-up questions to understand your requirements better:
- Current infrastructure details
- Performance requirements
- Budget constraints
- Timeline expectations
- Compliance needs

### Step 3: Recommendation

Based on your answers, the agent provides:
- **Architecture recommendations** with specific Cloud.ru services
- **Cost estimates** (TCO calculations with monthly/annual breakdowns)
- **Compliance guidance** (152-FZ, FSTEC requirements)
- **Migration plans** (phased approach with timelines)

### Step 4: Refinement

You can ask follow-up questions, request modifications, or explore alternative configurations. The agent remembers the full conversation context.

### Step 5: Summary and Handoff

When the consultation is complete, you receive a summary. If the deal looks promising, the system qualifies you as a lead and a human solutions architect may reach out.

---

## Available Agents

The platform has six specialized agents, each handling a distinct area of expertise:

### Architect Agent

Designs cloud architectures using Cloud.ru services. Handles questions about:
- Infrastructure design and service selection
- High availability and disaster recovery
- Performance optimization
- Reference architecture recommendations
- Service sizing and configuration

**Example:** "Design a fault-tolerant architecture for an e-commerce platform with 100K daily users."

### Cost Calculator Agent

Provides detailed cost estimates and TCO analysis. Handles:
- Monthly and annual cost projections
- Cloud.ru pricing for specific configurations
- Cost comparison (on-premise vs cloud)
- Discount and commitment plan guidance
- Budget optimization recommendations

**Example:** "Calculate the monthly cost for 20 VMs with 8 vCPU and 32 GB RAM each."

### Compliance Agent (152-FZ)

Advises on regulatory compliance for Russian data protection laws. Handles:
- 152-FZ personal data requirements
- FSTEC certification questions
- Data residency requirements
- Compliance audit preparation
- Security control recommendations

**Example:** "What do we need to comply with 152-FZ for storing customer personal data?"

### Migration Agent

Plans and guides infrastructure migrations to Cloud.ru. Handles:
- VMware to cloud migration
- Database migration strategies
- Application modernization paths
- Migration timeline and phasing
- Risk assessment and mitigation

**Example:** "We have 200 VMs on VMware vSphere. Plan our migration to Cloud.ru."

### AI Factory Agent

Advises on ML/AI infrastructure and GPU resources. Handles:
- GPU cluster sizing for model training
- ML pipeline architecture
- Inference infrastructure
- AI/ML service recommendations on Cloud.ru
- Benchmark data and performance estimates

**Example:** "We need to fine-tune a 70B parameter LLM. What GPU configuration do you recommend?"

### Human Escalation

When the AI's confidence is below the threshold (60%) or when the question requires human judgment, the conversation is automatically escalated to a human solutions architect. You will be notified when this happens.

---

## Web Chat Widget

If the web widget is embedded on your organization's website:

1. Click the chat icon (typically in the bottom-right corner)
2. Type your question in the text field
3. The conversation works identically to the Telegram bot
4. You can close and reopen the widget without losing context

---

## Human Escalation

### When It Happens

Conversations are escalated to a human solutions architect in these cases:

- The AI's confidence score drops below 60%
- The question is outside the scope of all agents
- You explicitly request to speak with a human
- The conversation exceeds the maximum turn limit (20 turns by default)
- Complex commercial negotiations are needed

### What to Expect

When escalation occurs:
1. You receive a notification that a human specialist will take over
2. The full conversation history is forwarded to the solutions architect
3. A human responds within business hours (typically within 2 hours)
4. The conversation can continue in the same channel (Telegram, web, or CRM)

---

## Tips for Best Results

1. **Be specific about your infrastructure.** Include numbers: VM count, CPU/RAM specs, storage volumes, user counts.
2. **Mention your timeline.** "We need to migrate within 3 months" helps the agent prioritize recommendations.
3. **State your constraints early.** Budget limits, compliance requirements, or technology preferences help narrow the options.
4. **Ask follow-up questions.** The agent retains full context. You can drill into specific aspects of a recommendation.
5. **Request cost breakdowns.** Ask for monthly and annual estimates with itemized service costs.

---

## Frequently Asked Questions

### Can I switch between agents mid-conversation?

Yes. Simply change the topic of your question. The orchestrator automatically routes to the appropriate agent. For example, you can start by asking about architecture and then ask about costs for the proposed configuration.

### Is my conversation data stored?

Yes, conversations are stored in a secure database for quality assurance and lead follow-up. All data is stored in a Moscow data center in compliance with 152-FZ. Conversations are anonymized after 90 days.

### Can I get a written summary of the consultation?

At any point, you can ask: "Summarize our conversation so far." The agent will provide a structured summary of the discussion, recommendations, and next steps.

### What languages does the bot support?

The primary language is Russian. The bot also understands and can respond in English, though Cloud.ru-specific terminology and pricing are optimized for Russian-language interactions.

### How accurate are the cost estimates?

Cost estimates are based on current Cloud.ru public pricing data stored in the RAG knowledge base. They are intended as planning estimates. Final pricing may vary based on committed usage, discounts, and specific configurations. Always confirm with a sales representative for contract-level pricing.

### Can I use the platform for multiple projects?

Yes. Each new conversation is independent. Start a new conversation for each distinct project or inquiry to keep the context clean.
