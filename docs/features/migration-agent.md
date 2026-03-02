# Feature: Migration Agent

## User Story
As a CTO or infrastructure manager, I want to get step-by-step migration planning from on-premise/other clouds to Cloud.ru, so that I can minimize risk and plan resources accurately.

## Complexity Score: -1 (via /plan)
- Touches ≤3 files: -2
- Agent is config, not code: -3
- Routing change in existing intent system: +2
- Estimated < 30 min: -2
- **Pipeline: /plan**

## Files Created/Modified
1. `prompts/migration.md` — Agent system prompt (lift-and-shift, re-platform, re-architect strategies)
2. `src/orchestrator/intent.py` — Route `migration` intent to `migration` agent (was routed to `architect`)
3. `tests/unit/test_orchestrator.py` — Update routing test assertion

## Implementation Steps
1. Create `prompts/migration.md` with migration specialist prompt:
   - 3 migration strategies: lift-and-shift, re-platform, re-architect
   - Phased migration plan (discovery → pilot → bulk → cutover)
   - Risk analysis and rollback procedures
   - Timeline estimates per strategy
2. Update `select_agent_type()` in `intent.py`: `"migration" → "migration"` (was `"architect"`)
3. Update test to match new routing: `test_migration_routes_to_migration`
4. Verify `AGENT_TYPES` tuple already includes `"migration"` — confirmed

## Tests
1. `tests/unit/test_orchestrator.py::test_migration_routes_to_migration` — routing assertion updated

## Edge Cases
- Migration intent already had keyword patterns defined (миграц, перенос, vmware, etc.)
- `AGENT_TYPES` in `base.py` already included "migration" — no change needed

## Dependencies
- Depends on: architect-agent (for architecture recommendations in migration context)
- `load_agent_prompt()` loads from `prompts/{agent_type}.md` — file naming convention

## Status: DONE
Committed: `feat: migration agent + AI factory agent with dedicated routing`
