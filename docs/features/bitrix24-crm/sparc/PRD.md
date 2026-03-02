# PRD -- Bitrix24 CRM Integration

## User Story

```
As a Cloud Sales Manager,
I want qualified consultation leads to be automatically created in Bitrix24 CRM,
So that no high-intent prospect is lost and my team can follow up without manual data entry.
```

## Acceptance Criteria

```gherkin
Feature: Automatic Bitrix24 Lead Creation

  Scenario: Qualified lead pushed to CRM
    Given a consultation scores "hot" or "qualified" (score >= 41)
    And the lead has not yet been pushed to CRM
    When the lead qualification check completes
    Then a Contact is created in Bitrix24 (or existing one found by email)
    And a Deal is created linked to that Contact
    And the deal stage maps to the qualification level
    And lead.crm_external_id is set to "contact:{id}/deal:{id}"

  Scenario: Duplicate contact prevention
    Given a contact with email "ivan@corp.ru" already exists in Bitrix24
    When push_lead is called with the same email
    Then crm.contact.list finds the existing contact
    And no duplicate contact is created
    And the deal is linked to the existing contact ID

  Scenario: CRM unavailable -- graceful degradation
    Given Bitrix24 returns HTTP 500
    When push_lead is called
    Then the system retries once (CRM_MAX_RETRIES=1)
    And if still failing, returns None without raising
    And the consultation continues unaffected
    And the failure is logged for ops alerting

  Scenario: CRM not configured
    Given BITRIX24_WEBHOOK_URL is empty
    When any CRM method is called
    Then it returns None immediately
    And no HTTP requests are made
```

## Affected Files

| File | Role |
|------|------|
| `src/services/crm.py` | Bitrix24Client -- REST API client |
| `src/services/lead_qualification.py` | Scoring, classification, CRM push trigger |
| `src/core/config.py` | `bitrix24_webhook_url` setting |
| `src/models/lead.py` | `crm_external_id` field |
| `tests/unit/test_crm.py` | Unit tests (13 tests) |
| `tests/integration/test_crm.py` | Integration tests (future) |

## Phase Tracking

| Phase | Status | Notes |
|-------|--------|-------|
| Bitrix24Client core (`_call`, retry) | Done | `src/services/crm.py` |
| Contact create + dedup | Done | `find_contact_by_email` + `create_contact` |
| Deal create + stage mapping | Done | `create_deal` with qualification-to-stage map |
| push_lead orchestration | Done | Contact + Deal in single flow |
| Lead qualification trigger | Done | `check_lead_qualification` in lead_qualification.py |
| Unit tests | Done | 13 tests across 5 test classes |
| Integration tests (live Bitrix24) | Planned | Requires sandbox Bitrix24 instance |
| Webhook URL rotation support | Planned | Admin UI for updating webhook |
