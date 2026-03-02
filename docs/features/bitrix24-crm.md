# Feature: Bitrix24 CRM Integration

## User Story
As a sales team, I want qualified leads to be automatically created in Bitrix24, so that our CRM pipeline stays up-to-date without manual data entry.

## Complexity Score: +4 (via /feature)
- Touches 4-10 files: 0
- External API integration (Bitrix24 REST): +2
- No new database entities (uses Lead.crm_external_id): 0
- Error handling for external service: +1
- Estimated 1-2 hours: +1
- **Pipeline: /feature**

## Files to Create/Modify
1. `src/services/crm.py` — Bitrix24 CRM service (create lead, create deal, push contact)
2. `src/services/lead_qualification.py` — Trigger CRM push after lead upsert for hot/qualified
3. `src/core/config.py` — Add bitrix24_webhook_url setting
4. `tests/unit/test_crm.py` — Unit tests for CRM service (mocked HTTP)

## Implementation Steps
1. Add `bitrix24_webhook_url` to Settings (optional, empty = disabled)
2. Create `src/services/crm.py`:
   - `Bitrix24Client` class wrapping webhook REST API
   - `create_contact(name, company, email, phone)` → contact_id
   - `create_deal(title, contact_id, value, stage)` → deal_id
   - `push_lead(lead: Lead)` → combines contact + deal creation
   - Error handling with retries (httpx, async)
   - Logging of all CRM operations
3. Integrate into lead_qualification.py:
   - After `upsert_lead()`, if qualification is "hot" or "qualified" and bitrix24 configured
   - Call `push_lead()` non-blocking (log errors, don't fail consultation)
   - Store `crm_external_id` in Lead model
4. Write unit tests with mocked httpx responses

## Bitrix24 REST API
- Webhook URL format: `https://{domain}.bitrix24.ru/rest/{user_id}/{secret}/`
- Create contact: `POST {webhook}/crm.contact.add`
- Create deal: `POST {webhook}/crm.deal.add`
- Check existing: `POST {webhook}/crm.contact.list` (filter by email)
- Response format: `{ "result": <id>, "time": {...} }`

## Tests
1. `test_crm.py::TestBitrix24Client::test_create_contact` — successful creation
2. `test_crm.py::TestBitrix24Client::test_create_deal` — deal with contact link
3. `test_crm.py::TestBitrix24Client::test_push_lead` — full lead push flow
4. `test_crm.py::TestBitrix24Client::test_push_lead_disabled` — no-op when webhook not configured
5. `test_crm.py::TestBitrix24Client::test_api_error_handling` — retry on 5xx, skip on 4xx
6. `test_crm.py::TestBitrix24Client::test_duplicate_detection` — existing contact by email

## Edge Cases
- Bitrix24 webhook not configured: skip silently (no-op)
- Network timeout: retry once, then log and continue (don't fail consultation)
- Duplicate contacts: check by email before creating new
- Missing contact fields: create with available data (name and company optional)
- Rate limiting: Bitrix24 allows 2 req/sec per webhook

## Dependencies
- Depends on: lead-qualification
- Uses: Lead model (contact, qualification, estimated_deal_value, crm_external_id)
- External: Bitrix24 REST API via webhook

## Status: PLANNED
