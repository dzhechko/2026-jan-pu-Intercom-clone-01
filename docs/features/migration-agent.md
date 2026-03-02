# Feature: Migration Agent

**Pipeline:** /feature (score: -1, range -1 to +4)
**Sprint:** v1.0
**Depends on:** architect-agent, orchestrator

## User Story (from Specification.md)

As a CTO or infrastructure manager, I want to get step-by-step migration planning from on-premise/other clouds to Cloud.ru, so that I can minimize risk and plan resources accurately.

### Acceptance Criteria (Gherkin)

```gherkin
Scenario: Migration consultation via Telegram
  Given a CTO connects via Telegram
  And sends "Мне нужно мигрировать 200 серверов VMware в облако"
  When the Migration Agent processes the request
  Then it asks clarifying questions about workload types and dependencies
  And provides a phased migration plan (discovery → pilot → bulk → cutover)
  And includes risk analysis with rollback procedures
  And estimates timelines per strategy
  And response confidence is >= 0.6
  And response time is under 30 seconds

Scenario: Migration strategy selection
  Given the user describes workloads (VMs, databases, containers)
  When the Migration Agent analyzes complexity
  Then it recommends one of: lift-and-shift, re-platform, re-architect
  And explains the trade-offs for each strategy

Scenario: Session continuity for migration
  Given a user had a migration consultation yesterday
  When they return and ask "What about the migration plan?"
  Then the bot restores previous context and continues
```

## Architecture References

### Agent Configuration (Architecture.md L150-157)
```
| Agent | Tools (MCP) | RAG Collections |
| Migration | migration_assessor, timeline_generator | migration_playbooks, case_studies |
```

### Pseudocode: Agent Routing (Pseudocode.md L189-207)
- Intent "migration" → agent_type "migration"
- Migration agent loaded from `prompts/migration.md`
- RAG collections: `{tenant}_migration`, `{tenant}_cloud_docs`

### Database (Architecture.md L293)
- `agent_configs` table supports per-tenant migration agent customization
- `messages.agent_type = 'migration'` for tracking

## Complexity Scoring

| Signal | Score | Notes |
|--------|-------|-------|
| Touches ≤3 files | -2 | prompts/migration.md, intent.py, test_orchestrator.py |
| Routing change in orchestrator | +2 | intent.py select_agent_type() |
| System prompt > 30 lines | +1 | 52-line prompt with strategies |
| Estimated < 30 min | -2 | config + routing only |
| **Total** | **-1** | **/feature pipeline** |

## Implementation Plan

### Files to Create/Modify
1. `prompts/migration.md` — NEW: System prompt (52 lines)
2. `src/orchestrator/intent.py` — MODIFY: Route migration → migration (was → architect)
3. `tests/unit/test_orchestrator.py` — MODIFY: Update routing test

### Implementation Steps
1. Create migration agent prompt with 3 strategies, phased plans, risk analysis
2. Fix routing: `select_agent_type("migration")` returns `"migration"` not `"architect"`
3. Update test assertion
4. Verify AGENT_TYPES includes "migration" (already present)

### Tests Required
1. `test_migration_routes_to_migration` — routing correctness
2. `test_migration_intent_russian` — Russian keyword detection (already exists)
3. `test_migration_intent_english` — English keyword detection (already exists)

### Edge Cases (from Refinement.md)
- Ambiguous workload: "I need cloud" → clarifying questions flow
- Large migration (500+ VMs): batch processing recommendation
- Multi-provider context: user asks about non-Cloud.ru migration

## Phase Tracking

- [x] Phase 1: PLAN — this document
- [x] Phase 2: VALIDATE — requirements score 90/100 (minor: no clarification question template)
- [x] Phase 3: IMPLEMENT — 3 tests passing, routing correct
- [x] Phase 4: REVIEW — 1 lint fix (unused import re in base.py), no security issues
