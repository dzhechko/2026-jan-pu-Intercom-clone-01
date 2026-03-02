"""Lead qualification service — scoring, classification, extraction, CRM push."""

import re
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logging import get_logger
from src.models.conversation import Conversation
from src.models.lead import Lead
from src.models.message import Message

logger = get_logger(__name__)

# --- Scoring constants ---

INTENT_SIGNALS: dict[str, int] = {
    "architect": 20,
    "cost_calculator": 25,
    "compliance": 15,
    "migration": 20,  # if detected as agent_type
    "ai_factory": 10,
}

ENGAGEMENT_THRESHOLDS = {
    "message_count": (10, 10),       # (threshold, score)
    "follow_up_bonus": 10,
    "company_details_bonus": 15,
    "pricing_interest_bonus": 20,
    "timeline_mention_bonus": 15,
}

NEGATIVE_SIGNALS = {
    "browsing": -20,
    "competitor": -50,
}

QUALIFICATION_THRESHOLDS = [
    (66, "qualified"),
    (41, "hot"),
    (21, "warm"),
    (0, "cold"),
]

# --- Keyword patterns ---

COMPANY_PATTERNS = re.compile(
    r"(?:компани[яию]|организаци[яию]|фирм[ау]|company|ООО|ОАО|АО|ЗАО|ПАО)\s+[\"«]?([А-ЯA-Z][^\n\"»,]{2,40})",
    re.IGNORECASE,
)
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_PATTERN = re.compile(r"(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}")
NAME_PATTERNS = re.compile(
    r"(?:меня зовут|я\s+—?\s*|my name is|i(?:'m| am))\s+([А-ЯA-Z][а-яa-z]+(?:\s+[А-ЯA-Z][а-яa-z]+)?)",
    re.IGNORECASE,
)

PRICING_KEYWORDS = re.compile(
    r"(?:цен[аы]|стоимост|прайс|pricing|тариф|contract|контракт|договор|оплат|бюджет|budget)",
    re.IGNORECASE,
)
TIMELINE_KEYWORDS = re.compile(
    r"(?:сроки?|когда|к\s+(?:январ|феврал|март|апрел|ма[йю]|июн|июл|август|сентябр|октябр|ноябр|декабр)"
    r"|timeline|deadline|квартал|Q[1-4]|до конца|месяц|неделю|через)",
    re.IGNORECASE,
)
BROWSING_KEYWORDS = re.compile(
    r"(?:просто интересно|just curious|из любопытства|just looking|для общего)",
    re.IGNORECASE,
)
COMPETITOR_KEYWORDS = re.compile(
    r"(?:работаю в yandex|работаю в vk|competitor|конкурент|аналитика рынка|market research)",
    re.IGNORECASE,
)
FOLLOW_UP_KEYWORDS = re.compile(
    r"(?:а\s+(?:как|что|если|можно)|ещё|еще|подробнее|расскажи больше|can you also|tell me more|what about)",
    re.IGNORECASE,
)


def calculate_lead_score(messages: list[dict], context: dict) -> int:
    """Calculate lead qualification score from conversation messages and context.

    Args:
        messages: List of message dicts with keys: role, content, agent_type, metadata.
        context: Conversation context dict.

    Returns:
        Integer score (can be negative).
    """
    score = 0
    agent_types_seen: set[str] = set()
    user_messages: list[str] = []

    for msg in messages:
        if msg.get("agent_type"):
            agent_types_seen.add(msg["agent_type"])
        if msg.get("role") == "user":
            user_messages.append(msg.get("content", ""))

    # Intent signals — which agents were involved
    for agent_type, points in INTENT_SIGNALS.items():
        if agent_type in agent_types_seen:
            score += points

    all_user_text = " ".join(user_messages)

    # Engagement signals
    if len(user_messages) > ENGAGEMENT_THRESHOLDS["message_count"][0]:
        score += ENGAGEMENT_THRESHOLDS["message_count"][1]

    if FOLLOW_UP_KEYWORDS.search(all_user_text):
        score += ENGAGEMENT_THRESHOLDS["follow_up_bonus"]

    if COMPANY_PATTERNS.search(all_user_text):
        score += ENGAGEMENT_THRESHOLDS["company_details_bonus"]

    if PRICING_KEYWORDS.search(all_user_text):
        score += ENGAGEMENT_THRESHOLDS["pricing_interest_bonus"]

    if TIMELINE_KEYWORDS.search(all_user_text):
        score += ENGAGEMENT_THRESHOLDS["timeline_mention_bonus"]

    # Negative signals
    if BROWSING_KEYWORDS.search(all_user_text):
        score += NEGATIVE_SIGNALS["browsing"]

    if COMPETITOR_KEYWORDS.search(all_user_text):
        score += NEGATIVE_SIGNALS["competitor"]

    return score


def classify_lead(score: int) -> str:
    """Classify lead based on score.

    Returns:
        One of: 'cold', 'warm', 'hot', 'qualified'.
    """
    for threshold, qualification in QUALIFICATION_THRESHOLDS:
        if score >= threshold:
            return qualification
    return "cold"


def extract_contact_info(messages: list[dict]) -> dict:
    """Extract contact information from user messages.

    Returns:
        Dict with keys: name, company, email, phone, telegram_username.
    """
    contact: dict[str, str | None] = {
        "name": None,
        "company": None,
        "email": None,
        "phone": None,
    }

    user_text = " ".join(
        msg.get("content", "") for msg in messages if msg.get("role") == "user"
    )

    name_match = NAME_PATTERNS.search(user_text)
    if name_match:
        contact["name"] = name_match.group(1).strip()

    company_match = COMPANY_PATTERNS.search(user_text)
    if company_match:
        contact["company"] = company_match.group(1).strip().rstrip("\"»")

    email_match = EMAIL_PATTERN.search(user_text)
    if email_match:
        contact["email"] = email_match.group(0)

    phone_match = PHONE_PATTERN.search(user_text)
    if phone_match:
        contact["phone"] = phone_match.group(0)

    return contact


def extract_architecture_summary(messages: list[dict]) -> str | None:
    """Extract architecture discussion summary from architect agent messages."""
    architect_responses = [
        msg.get("content", "")
        for msg in messages
        if msg.get("agent_type") == "architect" and msg.get("role") == "assistant"
    ]
    if not architect_responses:
        return None
    # Take the last (most complete) architect response, truncate to 500 chars
    summary = architect_responses[-1][:500]
    return summary if summary else None


def extract_tco_data(messages: list[dict]) -> dict | None:
    """Extract TCO calculation data from cost_calculator agent messages."""
    tco_responses = [
        msg for msg in messages
        if msg.get("agent_type") == "cost_calculator" and msg.get("role") == "assistant"
    ]
    if not tco_responses:
        return None
    last_response = tco_responses[-1]
    metadata = last_response.get("metadata", {})
    return {
        "content_preview": last_response.get("content", "")[:300],
        "sources": metadata.get("sources", []),
    }


async def upsert_lead(
    db: AsyncSession,
    tenant_id: str,
    conversation_id: str,
    contact: dict,
    qualification: str,
    intent: str | None = None,
    architecture_summary: str | None = None,
    tco_data: dict | None = None,
    compliance_requirements: list[str] | None = None,
) -> Lead:
    """Create or update a lead for the given conversation."""
    result = await db.execute(
        select(Lead).where(
            Lead.conversation_id == conversation_id,
            Lead.tenant_id == tenant_id,
        )
    )
    lead = result.scalar_one_or_none()

    if lead is None:
        lead = Lead(
            tenant_id=tenant_id,
            conversation_id=conversation_id,
        )
        db.add(lead)

    # Update fields — only override if new values are better
    lead.contact = {**lead.contact, **{k: v for k, v in contact.items() if v}}
    lead.qualification = qualification
    if intent:
        lead.intent = intent
    if architecture_summary:
        lead.architecture_summary = architecture_summary
    if tco_data:
        lead.tco_data = tco_data
    if compliance_requirements:
        lead.compliance_requirements = compliance_requirements

    # Estimate deal value based on qualification
    deal_estimates: dict[str, Decimal] = {
        "cold": Decimal("0"),
        "warm": Decimal("100000"),
        "hot": Decimal("500000"),
        "qualified": Decimal("1000000"),
    }
    lead.estimated_deal_value = deal_estimates.get(qualification, Decimal("0"))

    await db.flush()
    return lead


async def check_lead_qualification(
    conversation: Conversation,
    db: AsyncSession,
    tenant_id: str,
) -> Lead:
    """Main entry point — score, classify, extract, upsert lead.

    Called from orchestrator after each message is processed.
    """
    # Build messages list from ORM objects
    messages = [
        {
            "role": msg.role,
            "content": msg.content,
            "agent_type": msg.agent_type,
            "metadata": msg.metadata_,
        }
        for msg in conversation.messages
    ]

    # 1. Score
    score = calculate_lead_score(messages, conversation.context)

    # 2. Classify
    qualification = classify_lead(score)

    # 3. Extract contact info
    contact = extract_contact_info(messages)

    # 4. Extract context
    architecture_summary = extract_architecture_summary(messages)
    tco_data = extract_tco_data(messages)
    compliance_reqs = conversation.context.get("compliance_requirements")

    # 5. Upsert lead
    lead = await upsert_lead(
        db=db,
        tenant_id=tenant_id,
        conversation_id=conversation.id,
        contact=contact,
        qualification=qualification,
        intent=conversation.context.get("detected_intent"),
        architecture_summary=architecture_summary,
        tco_data=tco_data,
        compliance_requirements=compliance_reqs,
    )

    logger.info(
        "lead_qualified",
        conversation_id=conversation.id,
        score=score,
        qualification=qualification,
        contact_has_email=bool(contact.get("email")),
        contact_has_company=bool(contact.get("company")),
    )

    # 6. Push to CRM if qualified (non-blocking)
    if qualification in ("hot", "qualified") and not lead.crm_external_id:
        try:
            from src.services.crm import Bitrix24Client

            crm = Bitrix24Client()
            if crm.enabled:
                external_id = await crm.push_lead(
                    contact=contact,
                    qualification=qualification,
                    estimated_deal_value=float(lead.estimated_deal_value) if lead.estimated_deal_value else None,
                    intent=conversation.context.get("detected_intent"),
                    architecture_summary=architecture_summary,
                )
                if external_id:
                    lead.crm_external_id = external_id
                    await db.flush()
                    logger.info("crm_lead_pushed", conversation_id=conversation.id, external_id=external_id)
        except Exception:
            logger.exception("crm_push_failed", conversation_id=conversation.id)

    return lead
