# Specification: API Endpoints

Base URL: `/api/v1`. All JSON, all async.

## POST /auth/login -- Auth: none (public)

- **Request:** `{ "email": "str", "password": "str (min 8)" }`
- **Response 200:** `{ "access_token": "str", "token_type": "bearer", "expires_in": 3600 }`
- **Errors:** 401 invalid credentials

## POST /conversations -- Auth: X-API-Key (tenant)

- **Request:** `{ "channel": "telegram|web_widget|crm", "channel_user_id": "str", "initial_message": "str|null" }`
- **Response 201:** `{ "id": "uuid", "status": "active", "channel": "str", "created_at": "ISO8601" }`
- **Errors:** 401 missing/invalid API key

## POST /conversations/{id}/messages -- Auth: X-API-Key (tenant)

- **Request:** `{ "content": "str (max 10000)", "role": "user" }`
- **Response 200:**
  ```json
  {
    "user_message": { "id": "uuid", "content": "str", "role": "user", "created_at": "ISO8601" },
    "assistant_response": {
      "id": "uuid", "content": "str", "agent_type": "architect",
      "confidence": 0.85, "sources": [{"title":"str","url":"str"}], "created_at": "ISO8601"
    },
    "response_time_ms": 1200
  }
  ```
- **Errors:** 401 no key, 404 conversation not found, 409 conversation not active

## GET /conversations/{id} -- Auth: X-API-Key (tenant)

- **Response 200:** `{ "id", "status", "channel", "created_at" }`
- **Errors:** 401, 404

## GET /dashboard/metrics -- Auth: Bearer JWT

- **Query:** `period` (today|7d|30d|custom), `start_date`, `end_date`
- **Response 200:** `{ total_consultations, leads_generated, avg_response_time_ms, escalation_rate, satisfaction_score, conversion_rate, top_intents[], daily_trend[] }`

## GET /dashboard/roi -- Auth: Bearer JWT

- **Query:** `period` (7d|30d|90d)
- **Response 200:** `{ total_consultations, total_leads, qualified_leads, pipeline_value, avg_deal_value, conversion_rate, ai_handled, escalated_to_sa, sa_hours_saved, sa_cost_saved, lead_breakdown[], channel_stats[], daily_trend[] }`

## Auth Mechanisms

| Endpoint group | Mechanism | Dependency |
|----------------|-----------|------------|
| Conversations | `X-API-Key` header | `get_current_tenant` (bcrypt lookup) |
| Dashboard | `Bearer` JWT | `get_current_user` (JWT decode) |
| Auth/login | None | Public |
