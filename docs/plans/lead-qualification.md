# Feature: lead-qualification

## User Story
As a Sales Manager, I want leads to be automatically scored from consultation conversations,
so that I can prioritize follow-ups and focus on high-value prospects.

## Files Created/Modified
1. `src/services/lead_qualification.py` — scoring logic, classification, contact extraction
2. `tests/unit/test_lead_qualification.py` — 35 unit tests covering all scoring signals

## Implementation Steps
1. Define scoring signals (agent usage, engagement, keywords)
2. Implement `calculate_lead_score()` with weighted signal accumulation
3. Implement `classify_lead()` with thresholds: cold ≤20, warm 21-40, hot 41-65, qualified >65
4. Implement `extract_contact_info()` — regex extraction of email, phone, company, name
5. Implement `extract_architecture_summary()` — last architect response, truncated to 1000 chars
6. Implement `extract_tco_data()` — last cost calculator response
7. Write parameterized tests for all threshold boundaries

## Tests
1. `tests/unit/test_lead_qualification.py::TestCalculateLeadScore` — 13 tests (scoring signals)
2. `tests/unit/test_lead_qualification.py::TestClassifyLead` — 13 tests (threshold boundaries)
3. `tests/unit/test_lead_qualification.py::TestExtractContactInfo` — 7 tests (regex extraction)
4. `tests/unit/test_lead_qualification.py::TestExtractArchitectureSummary` — 3 tests (truncation)
5. `tests/unit/test_lead_qualification.py::TestExtractTcoData` — 2 tests

## Edge Cases
- Empty conversation → score 0, classify as cold
- Whitespace-only messages → ignored
- Assistant messages excluded from contact extraction
- Long architecture summary → truncated to 1000 chars (from Refinement.md)
- Competitor mentions → penalty applied

## Dependencies
- `src/orchestrator/` — provides agent_type metadata on messages
- `src/models/` — Conversation, Message models
