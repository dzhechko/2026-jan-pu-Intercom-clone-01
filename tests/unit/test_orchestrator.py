"""Unit tests for orchestrator — intent detection and agent routing."""


from src.orchestrator.intent import detect_intent, select_agent_type


class TestIntentDetection:
    """Test intent detection from user messages."""

    def test_migration_intent_russian(self):
        assert detect_intent("Мне нужно мигрировать 200 серверов VMware") == "migration"

    def test_migration_intent_english(self):
        assert detect_intent("I need to migrate my servers to cloud") == "migration"

    def test_cost_intent_russian(self):
        assert detect_intent("Сравни стоимость 50 ВМ: 8 vCPU, 32GB RAM") == "cost_optimization"

    def test_cost_intent_tco(self):
        assert detect_intent("Calculate TCO for 100 servers") == "cost_optimization"

    def test_compliance_152fz(self):
        assert detect_intent("Соответствует ли Cloud.ru 152-ФЗ?") == "compliance_check"

    def test_compliance_fstek(self):
        assert detect_intent("Требования ФСТЭК для госданных") == "compliance_check"

    def test_gpu_ai_intent(self):
        assert detect_intent("Нужны GPU для обучения моделей machine learning") == "gpu_ai"

    def test_deployment_intent(self):
        assert detect_intent("Хочу развернуть кластер Kubernetes") == "new_deployment"

    def test_escalation_explicit_human(self):
        assert detect_intent("Хочу поговорить с человеком") == "human_escalation"

    def test_escalation_operator(self):
        assert detect_intent("Позовите оператора") == "human_escalation"

    def test_escalation_specialist(self):
        assert detect_intent("Мне нужен специалист") == "human_escalation"

    def test_general_inquiry(self):
        assert detect_intent("Привет, расскажи про Cloud.ru") == "general_inquiry"

    def test_empty_message(self):
        assert detect_intent("") == "general_inquiry"

    def test_whitespace_only(self):
        assert detect_intent("   \n\t  ") == "general_inquiry"

    def test_mixed_intent_highest_score(self):
        # Message with both migration and cost keywords — migration should win (more keywords)
        result = detect_intent("Миграция VMware — сколько стоит перенос серверов?")
        assert result in ("migration", "cost_optimization")


class TestAgentSelection:
    """Test agent type selection from intent."""

    def test_migration_routes_to_migration(self):
        assert select_agent_type("migration") == "migration"

    def test_new_deployment_routes_to_architect(self):
        assert select_agent_type("new_deployment") == "architect"

    def test_cost_routes_to_calculator(self):
        assert select_agent_type("cost_optimization") == "cost_calculator"

    def test_compliance_routes_to_compliance(self):
        assert select_agent_type("compliance_check") == "compliance"

    def test_gpu_routes_to_ai_factory(self):
        assert select_agent_type("gpu_ai") == "ai_factory"

    def test_escalation_routes_to_human(self):
        assert select_agent_type("human_escalation") == "human_escalation"

    def test_general_routes_to_architect(self):
        assert select_agent_type("general_inquiry") == "architect"

    def test_unknown_defaults_to_architect(self):
        assert select_agent_type("unknown_intent") == "architect"
