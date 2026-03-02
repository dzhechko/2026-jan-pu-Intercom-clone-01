# Feature: Bitrix24 CRM Integration

**Pipeline:** /feature (score: +4, range -1 to +4)
**Sprint:** v1.0
**Depends on:** lead-qualification

## User Story

As a sales team, I want qualified leads to be automatically created in Bitrix24, so that our CRM pipeline stays up-to-date without manual data entry.

### Acceptance Criteria (Gherkin)

```gherkin
Scenario: Auto-push qualified lead to Bitrix24
  Given a conversation has qualification "hot" or "qualified"
  And bitrix24_webhook_url is configured
  When lead qualification runs
  Then a contact is created in Bitrix24 (or existing found by email)
  And a deal is created linked to the contact
  And Lead.crm_external_id is set to "contact:{id}/deal:{id}"

Scenario: Duplicate contact detection
  Given a contact with email "ivan@corp.ru" already exists in Bitrix24
  When a new lead with the same email is pushed
  Then the existing contact ID is reused (no duplicate)
  And a new deal is created linked to existing contact

Scenario: CRM not configured
  Given bitrix24_webhook_url is empty
  When lead qualification runs on a "qualified" lead
  Then no CRM push occurs (no-op)
  And no errors are logged

Scenario: CRM API error
  Given Bitrix24 returns a 500 error
  When the CRM push fails
  Then it retries once
  And if still failing, logs error and continues
  And the consultation is not affected
```

## Architecture References

### External API (Bitrix24 REST)
- Webhook URL: `https://{domain}.bitrix24.ru/rest/{user_id}/{secret}/`
- `crm.contact.add` — create contact
- `crm.contact.list` — find by email (duplicate check)
- `crm.deal.add` — create deal
- Rate limit: 2 req/sec per webhook

### Data Model
- `Lead.crm_external_id` — stores "contact:{id}/deal:{id}" after push
- `Lead.contact` — JSONB with name, company, email, phone
- `Lead.qualification` — triggers push when "hot" or "qualified"
- `Lead.estimated_deal_value` — maps to deal OPPORTUNITY

### Deal Stage Mapping
| Qualification | Bitrix24 Stage |
|---|---|
| hot | PREPARATION |
| qualified | PREPAYMENT_INVOICE |
| cold/warm | NEW (not pushed) |

## Complexity Scoring

| Signal | Score | Notes |
|--------|-------|-------|
| Touches 4-10 files | 0 | crm.py, lead_qualification.py, config.py, test_crm.py |
| External API integration | +2 | Bitrix24 REST webhook |
| Error handling / retries | +1 | Retry on 5xx, timeout handling |
| Estimated 1-2 hours | +1 | New service + integration + tests |
| **Total** | **+4** | **/feature pipeline** |

## Implementation Plan

### Files to Create/Modify
1. `src/core/config.py` — MODIFY: Add `bitrix24_webhook_url` setting
2. `src/services/crm.py` — NEW: Bitrix24Client class
3. `src/services/lead_qualification.py` — MODIFY: Add CRM push after upsert
4. `tests/unit/test_crm.py` — NEW: 19 tests

### Architecture Decisions
- **httpx async**: Non-blocking HTTP calls to Bitrix24
- **Non-blocking integration**: CRM errors don't fail the consultation (try/except)
- **Lazy import**: CRM client imported inside function to avoid circular deps
- **Webhook-based auth**: No OAuth flow needed, simpler for MVP

### Tests Required
1. Disabled state tests (no webhook → all operations return None)
2. CRUD tests (contact + deal creation with mocked httpx)
3. Full push flow test (find/create contact → create deal → return external ID)
4. Error handling tests (5xx retry, 4xx no retry)
5. Stage mapping tests
6. Contact field mapping tests

### Edge Cases
- No webhook configured → silent no-op
- Network timeout → retry once, then log and continue
- Duplicate contacts → find by email first
- Missing contact fields → create with available data
- Bitrix24 rate limiting → handled by retry logic
- Very long architecture_summary → truncated to 1000 chars in comments

## Phase Tracking

- [x] Phase 1: PLAN — this document (written before implementation)
- [x] Phase 2: VALIDATE — requirements score 95/100 (fixed: architecture_summary truncation 500→1000)
- [x] Phase 3: IMPLEMENT — 19 tests passing
- [x] Phase 4: REVIEW — 2 fixes: unused Message import removed, import sorting fixed
