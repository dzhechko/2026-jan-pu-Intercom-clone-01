# PRD: Architect Agent

## Overview

The Architect Agent is a config-driven AI agent that provides cloud architecture recommendations using Cloud.ru services. It combines a specialized system prompt (`prompts/architect.md`) with RAG retrieval over Cloud.ru documentation and LLM reasoning via the `AgentExecutor`.

## User Story (US-001)

As an Enterprise CTO, I want to describe my infrastructure and get a cloud architecture recommendation, so that I can evaluate Cloud.ru as a migration target in minutes instead of weeks.

## Acceptance Criteria

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

## Key Files

| File | Role |
|------|------|
| `prompts/architect.md` | System prompt defining agent behavior, response format, tools, constraints |
| `src/agents/base.py` | `AgentDefinition` dataclass, `load_agent_prompt()`, `get_agent_definition()` |
| `src/agents/executor.py` | `AgentExecutor.execute()` -- builds prompt with RAG context, calls Claude API |
| `src/orchestrator/router.py` | `Orchestrator.process_message()` -- intent detection, agent selection, RAG, execution |
| `src/orchestrator/intent.py` | `detect_intent()`, `select_agent_type()` -- maps user message to `"architect"` |

## Phase Tracking

- [x] Phase 1: PLAN -- SPARC docs created, 3 files (prompt, base, executor)
- [x] Phase 2: VALIDATE — code matches SPARC docs
- [x] Phase 3: IMPLEMENT — 138 tests passing, lint clean
- [x] Phase 4: REVIEW — 22 ruff issues fixed, all clean
