"""Base agent class and agent loader."""

from dataclasses import dataclass, field
from pathlib import Path

from src.core.logging import get_logger

logger = get_logger(__name__)

PROMPTS_DIR = Path(__file__).parent.parent.parent / "prompts"

AGENT_TYPES = ("architect", "cost_calculator", "compliance", "migration", "ai_factory", "human_escalation")


@dataclass
class AgentDefinition:
    agent_type: str
    name: str
    description: str
    system_prompt: str
    rag_collections: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    confidence_threshold: float = 0.6
    max_turns: int = 20


def load_agent_prompt(agent_type: str) -> str:
    prompt_file = PROMPTS_DIR / f"{agent_type}.md"
    if not prompt_file.exists():
        logger.warning("agent_prompt_not_found", agent_type=agent_type, path=str(prompt_file))
        return f"You are a {agent_type} agent. Help the user with their cloud consulting needs."
    return prompt_file.read_text(encoding="utf-8")


def parse_agent_config(agent_type: str, prompt_text: str) -> AgentDefinition:
    """Parse agent config from markdown prompt file."""
    name = agent_type.replace("_", " ").title()
    description = ""

    # Extract description from first paragraph after header
    lines = prompt_text.strip().split("\n")
    for line in lines[1:]:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            description = stripped
            break

    return AgentDefinition(
        agent_type=agent_type,
        name=name,
        description=description,
        system_prompt=prompt_text,
    )


def get_agent_definition(agent_type: str) -> AgentDefinition:
    if agent_type not in AGENT_TYPES:
        raise ValueError(f"Unknown agent type: {agent_type}. Valid types: {AGENT_TYPES}")
    prompt_text = load_agent_prompt(agent_type)
    return parse_agent_config(agent_type, prompt_text)
