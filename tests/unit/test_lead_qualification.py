"""Unit tests for lead qualification — scoring, classification, extraction."""

import pytest

from src.services.lead_qualification import (
    calculate_lead_score,
    classify_lead,
    extract_architecture_summary,
    extract_contact_info,
    extract_tco_data,
)


def _msg(role: str = "user", content: str = "", agent_type: str | None = None, metadata: dict | None = None) -> dict:
    """Helper to create message dict."""
    return {"role": role, "content": content, "agent_type": agent_type, "metadata": metadata or {}}


class TestCalculateLeadScore:
    """Test lead scoring algorithm."""

    def test_empty_conversation_scores_zero(self):
        assert calculate_lead_score([], {}) == 0

    def test_architect_agent_adds_20(self):
        messages = [_msg("assistant", "Here is the architecture", agent_type="architect")]
        assert calculate_lead_score(messages, {}) == 20

    def test_cost_calculator_agent_adds_25(self):
        messages = [_msg("assistant", "TCO comparison", agent_type="cost_calculator")]
        assert calculate_lead_score(messages, {}) == 25

    def test_compliance_agent_adds_15(self):
        messages = [_msg("assistant", "152-FZ info", agent_type="compliance")]
        assert calculate_lead_score(messages, {}) == 15

    def test_multiple_agents_accumulate(self):
        messages = [
            _msg("assistant", "arch", agent_type="architect"),
            _msg("assistant", "cost", agent_type="cost_calculator"),
            _msg("assistant", "compliance", agent_type="compliance"),
        ]
        score = calculate_lead_score(messages, {})
        assert score == 20 + 25 + 15  # 60

    def test_many_user_messages_adds_engagement(self):
        messages = [_msg("user", f"msg {i}") for i in range(12)]
        score = calculate_lead_score(messages, {})
        assert score >= 10  # message_count bonus

    def test_follow_up_questions_bonus(self):
        messages = [_msg("user", "А как насчет масштабирования? Расскажи подробнее")]
        score = calculate_lead_score(messages, {})
        assert score >= 10  # follow_up_bonus

    def test_company_details_bonus(self):
        messages = [_msg("user", "Компания «Газпром Нефть» ищет облако")]
        score = calculate_lead_score(messages, {})
        assert score >= 15  # company_details_bonus

    def test_pricing_interest_bonus(self):
        messages = [_msg("user", "Какие цены на виртуальные машины?")]
        score = calculate_lead_score(messages, {})
        assert score >= 20  # pricing_interest_bonus

    def test_timeline_mention_bonus(self):
        messages = [_msg("user", "Нужно запустить к Q3, сроки жёсткие")]
        score = calculate_lead_score(messages, {})
        assert score >= 15  # timeline_mention_bonus

    def test_browsing_penalty(self):
        messages = [_msg("user", "Просто интересно посмотреть что есть")]
        score = calculate_lead_score(messages, {})
        assert score <= -20  # browsing penalty

    def test_competitor_penalty(self):
        messages = [_msg("user", "Я работаю в Yandex, делаю аналитику рынка")]
        score = calculate_lead_score(messages, {})
        assert score <= -50  # competitor penalty

    def test_high_engagement_qualified_lead(self):
        """Full engagement: multiple agents + company + pricing + timeline."""
        messages = [
            _msg("user", "Компания «ТехноСервис» хочет мигрировать VMware"),
            _msg("assistant", "Architecture plan", agent_type="architect"),
            _msg("user", "Какие цены на 50 VM? Сроки — до конца Q2"),
            _msg("assistant", "TCO comparison", agent_type="cost_calculator"),
            _msg("user", "Нужна сертификация 152-ФЗ"),
            _msg("assistant", "Compliance info", agent_type="compliance"),
            _msg("user", "А как с договором? Расскажи подробнее"),
        ]
        score = calculate_lead_score(messages, {})
        # architect(20) + cost(25) + compliance(15) + company(15) + pricing(20) + timeline(15) + follow_up(10) = 120
        assert score >= 66  # Should be "qualified"


class TestClassifyLead:
    """Test qualification classification thresholds."""

    @pytest.mark.parametrize("score,expected", [
        (-50, "cold"),
        (0, "cold"),
        (10, "cold"),
        (20, "cold"),
        (21, "warm"),
        (30, "warm"),
        (40, "warm"),
        (41, "hot"),
        (55, "hot"),
        (65, "hot"),
        (66, "qualified"),
        (80, "qualified"),
        (150, "qualified"),
    ])
    def test_classification_thresholds(self, score: int, expected: str):
        assert classify_lead(score) == expected


class TestExtractContactInfo:
    """Test contact information extraction from messages."""

    def test_extract_email(self):
        messages = [_msg("user", "Мой email: ivan@technoservice.ru")]
        contact = extract_contact_info(messages)
        assert contact["email"] == "ivan@technoservice.ru"

    def test_extract_phone(self):
        messages = [_msg("user", "Позвоните мне +7 (495) 123 45 67")]
        contact = extract_contact_info(messages)
        assert contact["phone"] is not None
        assert "495" in contact["phone"]

    def test_extract_company(self):
        messages = [_msg("user", "Компания «ТехноСервис» ищет облачного провайдера")]
        contact = extract_contact_info(messages)
        assert contact["company"] is not None
        assert "ТехноСервис" in contact["company"]

    def test_extract_name(self):
        messages = [_msg("user", "Меня зовут Иван Петров, я CTO")]
        contact = extract_contact_info(messages)
        assert contact["name"] is not None
        assert "Иван" in contact["name"]

    def test_no_contact_info(self):
        messages = [_msg("user", "Расскажите про облачные решения")]
        contact = extract_contact_info(messages)
        assert contact["name"] is None
        assert contact["company"] is None
        assert contact["email"] is None
        assert contact["phone"] is None

    def test_empty_messages(self):
        contact = extract_contact_info([])
        assert contact["name"] is None

    def test_ignores_assistant_messages(self):
        messages = [
            _msg("assistant", "email: support@cloud.ru"),
            _msg("user", "Ок, спасибо"),
        ]
        contact = extract_contact_info(messages)
        assert contact["email"] is None  # Only user messages scanned


class TestExtractArchitectureSummary:
    """Test architecture summary extraction."""

    def test_extracts_last_architect_response(self):
        messages = [
            _msg("assistant", "First architecture draft", agent_type="architect"),
            _msg("assistant", "Refined architecture with Kubernetes", agent_type="architect"),
        ]
        summary = extract_architecture_summary(messages)
        assert summary is not None
        assert "Kubernetes" in summary

    def test_no_architect_messages(self):
        messages = [_msg("assistant", "TCO data", agent_type="cost_calculator")]
        assert extract_architecture_summary(messages) is None

    def test_truncates_long_summary(self):
        long_text = "A" * 1200
        messages = [_msg("assistant", long_text, agent_type="architect")]
        summary = extract_architecture_summary(messages)
        assert summary is not None
        assert len(summary) <= 1000


class TestExtractTcoData:
    """Test TCO data extraction."""

    def test_extracts_tco_response(self):
        messages = [
            _msg("assistant", "Cloud.ru: 150K/mo, Yandex: 180K/mo",
                 agent_type="cost_calculator", metadata={"sources": ["pricing.md"]}),
        ]
        tco = extract_tco_data(messages)
        assert tco is not None
        assert "content_preview" in tco
        assert "Cloud.ru" in tco["content_preview"]

    def test_no_cost_calculator_messages(self):
        messages = [_msg("assistant", "arch", agent_type="architect")]
        assert extract_tco_data(messages) is None
