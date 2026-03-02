# Refinement -- Bitrix24 CRM Integration

## Edge Cases

### EC-1: Duplicate Contacts

**Trigger:** Same user qualifies in multiple conversations, or conversation resumes.
**Current handling:** `find_contact_by_email` checks before `create_contact`.
**Gap:** If no email is provided, dedup is impossible -- a new contact is created each time.
**Mitigation:** Add phone-based dedup as fallback. Consider matching by Telegram username.

### EC-2: Bitrix24 Down (5xx / Timeout)

**Trigger:** Bitrix24 server error or network timeout.
**Current handling:** Retry once (CRM_MAX_RETRIES=1), then return None. Lead saved locally.
**Gap:** Lead sits with `crm_external_id=None` permanently if CRM never recovers.
**Mitigation:** Add a periodic background job that retries un-pushed leads (where
`crm_external_id IS NULL AND qualification IN ('hot','qualified')`). Run every 15 minutes.

### EC-3: Invalid or Expired Webhook URL

**Trigger:** Webhook secret rotated in Bitrix24 admin, or URL pasted incorrectly.
**Current handling:** Returns 401/403, logged as error, returns None.
**Gap:** Silent failure -- no alert to admin that all CRM pushes are failing.
**Mitigation:** Track consecutive CRM failures. After 5 failures in a row, send alert
to admin dashboard and/or Telegram notification channel.

### EC-4: Bitrix24 Rate Limiting

**Trigger:** Burst of qualified leads exceeds 2 req/s webhook limit.
**Current handling:** No explicit rate limiting. Sequential calls naturally throttle.
**Gap:** Under high load (many simultaneous conversations qualifying), Bitrix24
may return 503 or throttle responses.
**Mitigation:** Add a simple async semaphore or token bucket (2 req/s) around `_call`.
Queue excess requests with short backoff.

### EC-5: Partial Push (Contact Created, Deal Failed)

**Trigger:** Contact creation succeeds, but deal creation fails (network, validation).
**Current handling:** Returns `"contact:{id}/deal:none"` -- contact is orphaned in CRM.
**Gap:** Orphaned contact without a deal is not actionable for sales team.
**Mitigation:** On deal failure, log the contact_id for retry. Background job can
attempt `crm.deal.add` for leads where external_id contains `deal:none`.

### EC-6: Contact Info Extraction Fails

**Trigger:** User never shares name, email, or company during consultation.
**Current handling:** All contact fields default to None. Contact created with no
identifiable info (only SOURCE_ID).
**Gap:** Useless CRM record with no way to follow up.
**Mitigation:** If no email and no phone extracted, skip CRM push entirely. Log as
`crm_push_skipped_no_contact_info`. Prompt user for contact info when qualification
threshold is reached.

### EC-7: Very Long Architecture Summary

**Trigger:** Architect agent produces a multi-page response.
**Current handling:** `comments[:1000]` truncation in `create_deal`.
**Risk:** Truncation may cut mid-sentence or mid-URL.
**Mitigation:** Truncate at last sentence boundary within 1000 chars.

## Test Coverage Gaps

| Gap | Priority | Test to Add |
|-----|----------|-------------|
| Phone-based dedup | Medium | `test_find_contact_by_phone` |
| Consecutive failure alerting | Medium | `test_alert_on_n_failures` |
| Background retry job | High | `test_retry_unpushed_leads` |
| Partial push recovery | Medium | `test_deal_retry_after_partial` |
| Rate limit handling | Low | `test_rate_limit_backoff` |
| Empty contact skip | High | `test_skip_push_no_contact_info` |
