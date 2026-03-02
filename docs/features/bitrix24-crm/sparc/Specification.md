# Specification -- Bitrix24 CRM Integration

## Bitrix24 REST API

Authentication is via incoming webhook URL (no OAuth required for server-to-server).
Format: `https://{portal}.bitrix24.ru/rest/{user_id}/{secret}/{method}`

### Methods Used

| Method | Purpose | Params |
|--------|---------|--------|
| `crm.contact.list` | Find existing contact by email | `filter.EMAIL`, `select: [ID]` |
| `crm.contact.add` | Create new contact | `fields: {NAME, LAST_NAME, EMAIL, PHONE, COMPANY_TITLE, SOURCE_ID}` |
| `crm.deal.add` | Create deal linked to contact | `fields: {TITLE, CONTACT_ID, STAGE_ID, OPPORTUNITY, CURRENCY_ID, SOURCE_ID, COMMENTS}` |

### Response Format

```json
{ "result": 42, "time": { "start": 1.0, "finish": 1.1, "duration": 0.1 } }
```

For list methods, `result` is an array. For add methods, `result` is the new entity ID.

## Field Mapping

### Contact Fields

| Our Field | Bitrix24 Field | Transform |
|-----------|---------------|-----------|
| `contact.name` | `NAME` + `LAST_NAME` | Split on first space |
| `contact.company` | `COMPANY_TITLE` | Direct |
| `contact.email` | `EMAIL[0].VALUE` | Wrapped as `[{VALUE, VALUE_TYPE: "WORK"}]` |
| `contact.phone` | `PHONE[0].VALUE` | Wrapped as `[{VALUE, VALUE_TYPE: "WORK"}]` |
| (hardcoded) | `SOURCE_ID` | Always `"AI_CONSULTANT"` |

### Deal Fields

| Our Field | Bitrix24 Field | Transform |
|-----------|---------------|-----------|
| intent + company | `TITLE` | `"AI Consultant: {intent} -- {company}"` |
| `estimated_deal_value` | `OPPORTUNITY` | Float, RUB |
| qualification | `STAGE_ID` | Via `stage_map` (see below) |
| architecture_summary | `COMMENTS` | Truncated to 1000 chars |
| (hardcoded) | `CURRENCY_ID` | Always `"RUB"` |
| (hardcoded) | `SOURCE_ID` | Always `"AI_CONSULTANT"` |

## Deal Stage Mapping

| Qualification | Bitrix24 Stage | Meaning |
|---------------|---------------|---------|
| `qualified` | `PREPAYMENT_INVOICE` | Ready for commercial proposal |
| `hot` | `PREPARATION` | Active evaluation, needs nurturing |
| `warm` | `NEW` | Early interest (not pushed to CRM) |
| `cold` | `NEW` | No CRM push (below threshold) |

Only `hot` and `qualified` leads trigger CRM push.

## Retry Logic

- Timeout: 15 seconds per request (`CRM_TIMEOUT`)
- Max retries: 1 (`CRM_MAX_RETRIES`) -- total 2 attempts
- Retry on: HTTP 5xx, `httpx.TimeoutException`
- No retry on: HTTP 4xx (client error), unexpected response format
- On final failure: return `None`, log error, do not raise

## Rate Limits

Bitrix24 allows approximately 2 requests/second per webhook. Current flow uses
up to 3 sequential calls per lead (list + contact.add + deal.add). No parallel
calls are made within a single push_lead invocation.
