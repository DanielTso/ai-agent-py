"""Tests for the Agent class."""

from unittest.mock import MagicMock, patch

from ai_agent.agent import Agent
from ai_agent.config import Settings


def make_settings(**overrides) -> Settings:
    defaults = {
        "anthropic_api_key": "test-key",
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 100,
    }
    defaults.update(overrides)
    return Settings(**defaults)


def test_agent_chat():
    settings = make_settings()

    with patch("ai_agent.agent.Anthropic") as mock_cls:
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Hello back!")]
        mock_client.messages.create.return_value = mock_response

        agent = Agent(settings=settings)
        result = agent.chat("Hello")

        assert result == "Hello back!"
        assert len(agent.conversation) == 2
        assert agent.conversation[0] == {"role": "user", "content": "Hello"}
        assert agent.conversation[1] == {"role": "assistant", "content": "Hello back!"}


def test_agent_reset():
    settings = make_settings()

    with patch("ai_agent.agent.Anthropic"):
        agent = Agent(settings=settings)
        agent.conversation = [{"role": "user", "content": "test"}]
        agent.reset()
        assert agent.conversation == []
