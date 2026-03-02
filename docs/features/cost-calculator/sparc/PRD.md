# PRD: Cost Calculator Agent

## Overview

The Cost Calculator agent provides real-time Total Cost of Ownership (TCO) comparisons across Russian cloud providers (Cloud.ru, Yandex Cloud, VK Cloud). It parses workload specifications from natural language, calculates costs per category, applies volume discounts, and presents formatted comparison tables.

## User Story (US-002)

```
As an Enterprise CTO,
I want to get a real-time cost comparison across cloud providers,
So that I can make a data-driven decision on which provider to choose.
```

## Acceptance Criteria

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

  Scenario: Pricing data unavailable
    Given pricing for a specific service is not in the RAG corpus
    When the Cost Calculator Agent cannot provide accurate pricing
    Then it clearly states "I don't have current pricing for service X"
    And suggests contacting sales for a custom quote
    And does not hallucinate pricing numbers
```

## Key Files

| File | Purpose |
|------|---------|
| `prompts/cost_calculator.md` | Agent system prompt and response format |
| `tests/unit/test_tco.py` | Unit tests for TCO calculation logic |
| `src/services/lead_qualification.py` | `extract_tco_data()` -- extracts TCO from conversation |
| `docs/Pseudocode.md` | TCO algorithm definition (WorkloadSpec, calculate steps) |

## Phase Tracking

- [x] Phase 1: PLAN -- SPARC docs created, 2 files (prompt, test_tco)
- [x] Phase 2: VALIDATE — code matches SPARC docs
- [x] Phase 3: IMPLEMENT — 138 tests passing, lint clean
- [x] Phase 4: REVIEW — 22 ruff issues fixed, all clean
