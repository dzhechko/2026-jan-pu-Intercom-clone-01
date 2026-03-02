"""Intent detection for routing messages to the correct agent."""

import re

# Escalation patterns — explicit user request for human
ESCALATION_PATTERNS = [
    r"человек",
    r"оператор",
    r"специалист",
    r"живой",
    r"менеджер",
    r"поговорить с",
    r"хочу поговорить",
    r"помощь.*(человек|специалист)",
    r"connect.*human",
    r"speak.*person",
    r"talk.*someone",
]

# Intent keyword patterns (Russian + English)
INTENT_PATTERNS: dict[str, list[str]] = {
    "migration": [
        r"миграц",
        r"перенос",
        r"перевод",
        r"переезд",
        r"vmware",
        r"migrat",
        r"move.*cloud",
        r"перейти.*облак",
    ],
    "cost_optimization": [
        r"стоимость",
        r"цена",
        r"тариф",
        r"расчёт",
        r"расчет",
        r"сравни",
        r"tco",
        r"cost",
        r"price",
        r"сколько стоит",
        r"бюджет",
        r"экономи",
    ],
    "compliance_check": [
        r"152.?фз",
        r"фстэк",
        r"фстек",
        r"кии",
        r"персональн.*данн",
        r"compliance",
        r"сертификац",
        r"аттестац",
        r"безопасност",
        r"регулятор",
    ],
    "gpu_ai": [
        r"gpu",
        r"видеокарт",
        r"ml\b",
        r"machine.?learning",
        r"нейросет",
        r"обуч.*модел",
        r"inference",
        r"ai.?factory",
        r"искусственн.*интеллект",
    ],
    "new_deployment": [
        r"разверн",
        r"развёрн",
        r"deploy",
        r"новый.*проект",
        r"запуск",
        r"архитектур",
        r"kubernetes",
        r"k8s",
        r"кластер",
        r"серверы",
        r"вм\b",
        r"виртуальн",
        r"облак",
    ],
}


def detect_intent(message: str, context: dict | None = None) -> str:
    """Detect user intent from message text.

    Returns one of: migration, new_deployment, cost_optimization,
    compliance_check, gpu_ai, general_inquiry
    """
    message_lower = message.lower().strip()

    # Check for escalation first
    for pattern in ESCALATION_PATTERNS:
        if re.search(pattern, message_lower):
            return "human_escalation"

    # Check for empty/whitespace
    if not message_lower:
        return "general_inquiry"

    # Score each intent
    scores: dict[str, int] = {}
    for intent, patterns in INTENT_PATTERNS.items():
        score = sum(1 for p in patterns if re.search(p, message_lower))
        if score > 0:
            scores[intent] = score

    if not scores:
        return "general_inquiry"

    # Return highest-scoring intent
    return max(scores, key=scores.get)


def select_agent_type(intent: str) -> str:
    """Map intent to agent type."""
    mapping = {
        "migration": "migration",
        "new_deployment": "architect",
        "cost_optimization": "cost_calculator",
        "compliance_check": "compliance",
        "gpu_ai": "ai_factory",
        "human_escalation": "human_escalation",
        "general_inquiry": "architect",
    }
    return mapping.get(intent, "architect")
