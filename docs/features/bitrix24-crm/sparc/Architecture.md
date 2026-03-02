# Architecture -- Bitrix24 CRM Integration

## Data Flow

```
Orchestrator (after each message)
  |
  v
check_lead_qualification(conversation, db, tenant_id)
  |
  +-- calculate_lead_score(messages, context)  --> int score
  +-- classify_lead(score)                     --> "cold"|"warm"|"hot"|"qualified"
  +-- extract_contact_info(messages)           --> {name, company, email, phone}
  +-- upsert_lead(db, ...)                     --> Lead ORM object
  |
  v
  [Guard: qualification in ("hot","qualified") AND lead.crm_external_id is None]
  |
  v
Bitrix24Client.push_lead(contact, qualification, value, intent, summary)
  |
  +-- create_contact(name, company, email, phone)
  |     +-- find_contact_by_email(email)  --> existing ID or None
  |     +-- _call("crm.contact.add", ...)  --> new ID
  |
  +-- create_deal(title, contact_id, value, stage, comments)
  |     +-- _call("crm.deal.add", ...)    --> deal ID
  |
  v
lead.crm_external_id = "contact:{id}/deal:{id}"
db.flush()
```

## Component Responsibilities

| Component | File | Responsibility |
|-----------|------|----------------|
| Lead Qualification | `src/services/lead_qualification.py` | Score, classify, extract, trigger CRM |
| CRM Client | `src/services/crm.py` | HTTP calls to Bitrix24 REST API |
| Lead Model | `src/models/lead.py` | Persist lead + `crm_external_id` |
| Config | `src/core/config.py` | `bitrix24_webhook_url` from env |

## Design Decisions

### ADR-1: Webhook auth instead of OAuth

Bitrix24 incoming webhooks provide a static URL with embedded credentials.
Simpler than full OAuth2 flow. Trade-off: webhook URL is a secret that must
be rotated manually if compromised.

### ADR-2: Dedup by email before contact creation

`find_contact_by_email` is called before every `create_contact`. This avoids
duplicates when the same lead is re-qualified (e.g., conversation resumes).
If no email is provided, dedup is skipped and a new contact is created.

### ADR-3: Non-blocking CRM push with exception swallowing

CRM push is wrapped in try/except in `check_lead_qualification`. A Bitrix24
failure must never break the consultation flow. The lead is saved locally
regardless of CRM outcome.

### ADR-4: Sequential API calls (not parallel)

The 3 Bitrix24 calls (list, contact.add, deal.add) run sequentially because
each depends on the previous result. Bitrix24's 2 req/s limit makes this
acceptable.

## Security

- Webhook URL stored in `BITRIX24_WEBHOOK_URL` env var, never in code
- URL contains embedded auth token -- treat as secret
- Comments field truncated to 1000 chars to prevent oversized payloads
- No PII logged (only contact_id, deal_id, qualification level)
