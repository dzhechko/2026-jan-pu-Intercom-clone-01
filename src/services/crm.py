"""Bitrix24 CRM integration service."""

import httpx

from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger(__name__)

# Bitrix24 allows ~2 req/sec per webhook
CRM_TIMEOUT = 15.0
CRM_MAX_RETRIES = 1


class Bitrix24Client:
    """Client for Bitrix24 CRM REST API via webhook."""

    def __init__(self, webhook_url: str | None = None):
        self.webhook_url = (webhook_url or settings.bitrix24_webhook_url).rstrip("/")
        self.enabled = bool(self.webhook_url)

    async def _call(self, method: str, params: dict) -> dict | None:
        """Call Bitrix24 REST method. Returns result or None on failure."""
        if not self.enabled:
            return None

        url = f"{self.webhook_url}/{method}"
        retries = 0

        while retries <= CRM_MAX_RETRIES:
            try:
                async with httpx.AsyncClient(timeout=CRM_TIMEOUT) as client:
                    resp = await client.post(url, json=params)

                if resp.status_code == 200:
                    data = resp.json()
                    if "result" in data:
                        return data
                    logger.warning("bitrix24_unexpected_response", method=method, body=data)
                    return None

                if resp.status_code >= 500 and retries < CRM_MAX_RETRIES:
                    retries += 1
                    logger.warning("bitrix24_server_error_retrying", method=method, status=resp.status_code)
                    continue

                logger.error("bitrix24_api_error", method=method, status=resp.status_code, body=resp.text[:500])
                return None

            except httpx.TimeoutException:
                if retries < CRM_MAX_RETRIES:
                    retries += 1
                    logger.warning("bitrix24_timeout_retrying", method=method)
                    continue
                logger.error("bitrix24_timeout", method=method)
                return None
            except Exception:
                logger.exception("bitrix24_request_failed", method=method)
                return None

        return None

    async def find_contact_by_email(self, email: str) -> int | None:
        """Find existing contact by email. Returns contact ID or None."""
        result = await self._call("crm.contact.list", {
            "filter": {"EMAIL": email},
            "select": ["ID"],
        })
        if result and result.get("result"):
            contacts = result["result"]
            if isinstance(contacts, list) and len(contacts) > 0:
                return int(contacts[0]["ID"])
        return None

    async def create_contact(
        self,
        name: str | None = None,
        company: str | None = None,
        email: str | None = None,
        phone: str | None = None,
    ) -> int | None:
        """Create a contact in Bitrix24. Returns contact ID or None."""
        # Check for duplicate by email
        if email:
            existing_id = await self.find_contact_by_email(email)
            if existing_id:
                logger.info("bitrix24_contact_exists", email=email, contact_id=existing_id)
                return existing_id

        fields: dict = {}
        if name:
            parts = name.split(maxsplit=1)
            fields["NAME"] = parts[0]
            if len(parts) > 1:
                fields["LAST_NAME"] = parts[1]
        if company:
            fields["COMPANY_TITLE"] = company
        if email:
            fields["EMAIL"] = [{"VALUE": email, "VALUE_TYPE": "WORK"}]
        if phone:
            fields["PHONE"] = [{"VALUE": phone, "VALUE_TYPE": "WORK"}]

        fields["SOURCE_ID"] = "AI_CONSULTANT"

        result = await self._call("crm.contact.add", {"fields": fields})
        if result:
            contact_id = int(result["result"])
            logger.info("bitrix24_contact_created", contact_id=contact_id)
            return contact_id
        return None

    async def create_deal(
        self,
        title: str,
        contact_id: int | None = None,
        value: float = 0.0,
        stage: str = "NEW",
        comments: str = "",
    ) -> int | None:
        """Create a deal in Bitrix24. Returns deal ID or None."""
        fields: dict = {
            "TITLE": title,
            "STAGE_ID": stage,
            "SOURCE_ID": "AI_CONSULTANT",
            "CURRENCY_ID": "RUB",
        }
        if contact_id:
            fields["CONTACT_ID"] = contact_id
        if value > 0:
            fields["OPPORTUNITY"] = value
        if comments:
            fields["COMMENTS"] = comments[:1000]

        result = await self._call("crm.deal.add", {"fields": fields})
        if result:
            deal_id = int(result["result"])
            logger.info("bitrix24_deal_created", deal_id=deal_id, contact_id=contact_id)
            return deal_id
        return None

    async def push_lead(
        self,
        contact: dict,
        qualification: str,
        estimated_deal_value: float | None = None,
        intent: str | None = None,
        architecture_summary: str | None = None,
    ) -> str | None:
        """Push a qualified lead to Bitrix24 (contact + deal).

        Returns external CRM ID string (format: "contact:{id}/deal:{id}") or None.
        """
        if not self.enabled:
            return None

        name = contact.get("name")
        company = contact.get("company")
        email = contact.get("email")
        phone = contact.get("phone")

        # Create or find contact
        contact_id = await self.create_contact(name, company, email, phone)

        # Determine deal stage based on qualification
        stage_map = {"hot": "PREPARATION", "qualified": "PREPAYMENT_INVOICE"}
        stage = stage_map.get(qualification, "NEW")

        # Build deal title
        intent_label = (intent or "consultation").replace("_", " ")
        company_label = company or "Unknown"
        title = f"AI Consultant: {intent_label} — {company_label}"

        # Build comments from architecture summary
        comments = ""
        if architecture_summary:
            comments = f"Architecture recommendation:\n{architecture_summary}"

        deal_id = await self.create_deal(
            title=title,
            contact_id=contact_id,
            value=float(estimated_deal_value) if estimated_deal_value else 0.0,
            stage=stage,
            comments=comments,
        )

        if contact_id or deal_id:
            external_id = f"contact:{contact_id or 'none'}/deal:{deal_id or 'none'}"
            logger.info("bitrix24_lead_pushed", external_id=external_id, qualification=qualification)
            return external_id

        return None
