# PRD — Migration Agent

## User Story (US-004)

```
As an IT Director with on-premise infrastructure,
I want to receive a step-by-step migration plan to Cloud.ru,
So that I can move workloads safely with clear timelines and rollback options.
```

## Acceptance Criteria

```gherkin
Feature: Migration Planning

  Scenario: VMware fleet migration assessment
    Given an IT Director sends "We need to migrate 150 VMware VMs to Cloud.ru"
    When the Migration Agent processes the request
    Then it asks clarifying questions (workload types, dependencies, data volumes)
    And generates a phased migration plan (discovery, pilot, bulk, cutover)
    And provides timeline estimates per phase
    And includes rollback procedures for each phase
    And response time is under 30 seconds

  Scenario: Strategy recommendation
    Given the IT Director describes mixed workloads (VMs, databases, legacy apps)
    When the Migration Agent assesses infrastructure
    Then it recommends per-workload strategy (lift-and-shift / re-platform / re-architect)
    And explains trade-offs for each strategy
    And flags 152-FZ data sovereignty requirements early

  Scenario: Complex legacy system escalation
    Given the IT Director describes a mainframe-based ERP system
    When the Migration Agent detects confidence < 0.6
    Then it acknowledges limitations transparently
    And offers to connect with a human Solution Architect
    And passes full conversation context to the SA

  Scenario: Follow-up timeline adjustment
    Given the IT Director received an initial migration plan
    When they say "We need to finish in 3 months instead of 6"
    Then the Migration Agent adjusts the plan with trade-offs
    And identifies which phases can be parallelized
    And flags increased risk from compressed timeline
```

## Files Affected

| File | Action | Purpose |
|------|--------|---------|
| `prompts/migration.md` | Exists | Agent system prompt |
| `src/orchestrator/intent.py` | Exists | Migration intent patterns |
| `src/orchestrator/router.py` | Exists | Routes to migration agent |
| `src/agents/configs/migration.yaml` | Create | Agent config (RAG collections, tools) |
| `src/services/migration.py` | Create | Migration plan generation logic |
| `corpus/migration/` | Populate | Cloud.ru migration docs for RAG |

## Phase Tracking

| Phase | Scope | Status |
|-------|-------|--------|
| P1 - Intent & Routing | Migration intent detection, agent selection | Done |
| P2 - RAG Corpus | Index Cloud.ru migration docs into Qdrant | Planned |
| P3 - Assessment Logic | Infrastructure assessment, strategy selection | Planned |
| P4 - Plan Generation | Phased plan with timelines and rollback | Planned |
| P5 - MCP Tools | pricing_api + config_api integration | Planned |
