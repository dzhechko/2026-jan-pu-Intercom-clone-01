"""Unit tests for web chat widget integration.

Tests the widget-related backend functionality:
- Conversation creation with web_widget channel
- Message flow through the widget
- Lead capture from widget conversations
"""

import pytest

from src.api.schemas.conversation import ConversationCreateSchema, MessageCreateSchema
from src.orchestrator.intent import detect_intent, select_agent_type


class TestWidgetConversationSchema:
    """Test that conversation schemas support web_widget channel."""

    def test_web_widget_channel_accepted(self):
        schema = ConversationCreateSchema(
            channel="web_widget",
            channel_user_id="session_abc123",
        )
        assert schema.channel == "web_widget"

    def test_web_widget_with_initial_message(self):
        schema = ConversationCreateSchema(
            channel="web_widget",
            channel_user_id="session_abc123",
            initial_message="Расскажите про Cloud.ru",
        )
        assert schema.initial_message == "Расскажите про Cloud.ru"

    def test_web_widget_without_initial_message(self):
        schema = ConversationCreateSchema(
            channel="web_widget",
            channel_user_id="session_abc123",
        )
        assert schema.initial_message is None

    def test_invalid_channel_rejected(self):
        with pytest.raises(Exception):
            ConversationCreateSchema(
                channel="invalid_channel",
                channel_user_id="session_abc123",
            )


class TestWidgetMessageSchema:
    """Test message schemas for widget use."""

    def test_user_message(self):
        schema = MessageCreateSchema(content="Сколько стоит 10 ВМ?", role="user")
        assert schema.content == "Сколько стоит 10 ВМ?"
        assert schema.role == "user"

    def test_message_max_length(self):
        long_msg = "x" * 10000
        schema = MessageCreateSchema(content=long_msg, role="user")
        assert len(schema.content) == 10000

    def test_message_too_long_rejected(self):
        with pytest.raises(Exception):
            MessageCreateSchema(content="x" * 10001, role="user")

    def test_only_user_role_accepted(self):
        with pytest.raises(Exception):
            MessageCreateSchema(content="test", role="assistant")


class TestWidgetIntentRouting:
    """Test that widget conversations route to correct agents."""

    def test_architecture_question(self):
        intent = detect_intent("Какую архитектуру выбрать для микросервисов?")
        agent = select_agent_type(intent)
        assert agent in ("architect", "migration", "ai_factory")

    def test_cost_question(self):
        intent = detect_intent("Сколько стоит 50 виртуальных машин?")
        agent = select_agent_type(intent)
        assert agent == "cost_calculator"

    def test_compliance_question(self):
        intent = detect_intent("Соответствие 152-ФЗ для персональных данных")
        agent = select_agent_type(intent)
        assert agent == "compliance"

    def test_gpu_question(self):
        intent = detect_intent("Нужны GPU для обучения нейросети")
        agent = select_agent_type(intent)
        assert agent == "ai_factory"

    def test_migration_question(self):
        intent = detect_intent("Как перенести 200 серверов VMware в облако?")
        agent = select_agent_type(intent)
        assert agent == "migration"

    def test_escalation_from_widget(self):
        intent = detect_intent("Хочу поговорить с человеком")
        agent = select_agent_type(intent)
        assert agent == "human_escalation"

    def test_greeting_routes_to_architect(self):
        intent = detect_intent("Привет!")
        agent = select_agent_type(intent)
        assert agent == "architect"
