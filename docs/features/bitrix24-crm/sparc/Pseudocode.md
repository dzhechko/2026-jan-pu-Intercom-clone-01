# Pseudocode -- Bitrix24 CRM Integration

## push_lead(contact, qualification, value, intent, summary)

```
function push_lead(contact, qualification, value, intent, summary):
    if not self.enabled: return None
    contact_id = create_contact(contact.name, contact.company, contact.email, contact.phone)
    stage = map_deal_stage(qualification)
    title = "AI Consultant: {intent} -- {company or 'Unknown'}"
    comments = "Architecture recommendation:\n{summary}" if summary else ""
    deal_id = create_deal(title, contact_id, value, stage, comments)
    if contact_id or deal_id:
        return "contact:{contact_id}/deal:{deal_id}"
    return None
```

## create_contact(name, company, email, phone)

```
function create_contact(name, company, email, phone):
    if email:
        existing_id = find_contact_by_email(email)  # dedup
        if existing_id: return existing_id
    fields = {SOURCE_ID: "AI_CONSULTANT"}
    if name: fields.NAME, fields.LAST_NAME = name.split(maxsplit=1)
    if company: fields.COMPANY_TITLE = company
    if email:   fields.EMAIL = [{VALUE: email, VALUE_TYPE: "WORK"}]
    if phone:   fields.PHONE = [{VALUE: phone, VALUE_TYPE: "WORK"}]
    result = _call("crm.contact.add", {fields})
    return int(result["result"]) if result else None
```

## create_deal(title, contact_id, value, stage, comments)

```
function create_deal(title, contact_id, value, stage, comments):
    fields = {TITLE: title, STAGE_ID: stage, SOURCE_ID: "AI_CONSULTANT", CURRENCY_ID: "RUB"}
    if contact_id: fields.CONTACT_ID = contact_id
    if value > 0:  fields.OPPORTUNITY = value
    if comments:   fields.COMMENTS = comments[:1000]
    result = _call("crm.deal.add", {fields})
    return int(result["result"]) if result else None
```

## map_deal_stage(qualification)

```
function map_deal_stage(qualification):
    return {"hot": "PREPARATION", "qualified": "PREPAYMENT_INVOICE"}.get(qualification, "NEW")
```

## _call(method, params) -- retry_on_5xx

```
function _call(method, params):
    if not self.enabled: return None
    url = "{webhook_url}/{method}"
    retries = 0
    while retries <= CRM_MAX_RETRIES:
        try:
            response = POST(url, json=params, timeout=CRM_TIMEOUT)
            if response.status == 200:
                data = response.json()
                return data if "result" in data else None
            if response.status >= 500 and retries < CRM_MAX_RETRIES:
                retries += 1; continue
            return None  # 4xx or exhausted retries
        except TimeoutException:
            if retries < CRM_MAX_RETRIES: retries += 1; continue
            return None
        except Exception:
            log_exception("request failed"); return None
    return None
```
