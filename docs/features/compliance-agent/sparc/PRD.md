# PRD: Compliance Agent

## Overview

The Compliance Agent is one of six specialized agents in the AI-Consultant platform. It automates regulatory compliance advisory for Russian cloud infrastructure, covering 152-FZ (personal data), FSTEC (security certification), and KII (critical information infrastructure).

## User Story (US-003)

```
As an Enterprise CTO processing personal data,
I want to verify that a cloud provider meets 152-FZ requirements,
So that I can ensure regulatory compliance for my workload.
```

## Acceptance Criteria

```gherkin
Feature: Compliance Advisory

  Scenario: 152-FZ compliance check
    Given a CTO asks "Does Cloud.ru meet 152-FZ for processing personal data?"
    When the Compliance Agent processes the request
    Then it confirms Cloud.ru's compliance status
    And lists specific certifications and security measures
    And recommends appropriate security level (UZ-1/2/3/4)
    And cites official documentation sources

  Scenario: FSTEC requirements
    Given a CTO asks about FSTEC certification for government data
    When the Compliance Agent processes the request
    Then it explains applicable FSTEC levels
    And maps Cloud.ru services to required security measures
    And identifies any gaps requiring additional configuration

  Scenario: KII workload requirements
    Given a CTO has Critical Information Infrastructure workload
    When they describe their KII classification
    Then the Compliance Agent explains mandatory requirements
    And provides a checklist of necessary security controls
    And flags services that need additional certification
```

## Files

| File | Purpose |
|------|---------|
| `prompts/compliance.md` | Agent system prompt (behavior, response format, constraints) |
| `src/orchestrator/intent.py` | Intent detection: `compliance_check` patterns (152-FZ, FSTEC, KII keywords) |
| `src/orchestrator/router.py` | Routes `compliance_check` intent to `compliance` agent via `Orchestrator` |
| `src/agents/base.py` | `AgentDefinition` dataclass, loads prompt from `prompts/compliance.md` |
| `src/agents/executor.py` | Executes LLM call with system prompt + RAG context |
| `corpus/` | RAG document corpus (regulatory docs, Cloud.ru certifications) |

## Phase Tracking

- [x] Phase 1: PLAN -- SPARC docs created, 1 file (prompt)
- [x] Phase 2: VALIDATE — code matches SPARC docs
- [x] Phase 3: IMPLEMENT — 138 tests passing, lint clean
- [x] Phase 4: REVIEW — 22 ruff issues fixed, all clean
