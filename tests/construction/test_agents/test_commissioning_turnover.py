"""Tests for the Commissioning & Turnover agent."""

import json
from unittest.mock import MagicMock, patch

from construction.agents.commissioning_turnover import (
    CommissioningTurnoverAgent,
)


def _make_settings(**overrides):
    """Create mock ConstructionSettings."""
    defaults = {
        "anthropic_api_key": "fake-key",
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 4096,
        "openweathermap_api_key": "",
    }
    defaults.update(overrides)
    mock = MagicMock()
    for k, v in defaults.items():
        setattr(mock, k, v)
    return mock


@patch("construction.agents.base.Agent")
def test_initialization(mock_agent_cls):
    """Agent initializes with correct name and description."""
    agent = CommissioningTurnoverAgent(
        settings=_make_settings()
    )
    assert agent.name == "commissioning_turnover"
    assert "commissioning" in agent.description.lower()
    assert agent.schedule == "daily"


@patch("construction.agents.base.Agent")
def test_system_prompt_set(mock_agent_cls):
    """System prompt contains commissioning guidance."""
    agent = CommissioningTurnoverAgent(
        settings=_make_settings()
    )
    prompt = agent.get_system_prompt()
    assert "commissioning" in prompt.lower()
    assert "IST" in prompt or "ist" in prompt.lower()
    assert "punch" in prompt.lower()
    assert "turnover" in prompt.lower()
    assert "UPS" in prompt or "generator" in prompt.lower()


@patch("construction.agents.base.Agent")
def test_tools_registered(mock_agent_cls):
    """Agent registers commissioning and schedule tools."""
    agent = CommissioningTurnoverAgent(
        settings=_make_settings()
    )
    tool_names = [
        t.name for t in agent._tools._tools.values()
    ]
    assert "commissioning_query" in tool_names
    assert "schedule_query" in tool_names
    assert len(tool_names) == 2


@patch("construction.agents.base.Agent")
async def test_run_returns_agent_event(mock_agent_cls):
    """run() calls chat and returns an AgentEvent."""
    mock_response = json.dumps({
        "ist_status": {
            "blocked_tests": [],
            "ready_tests": ["IST-002"],
        },
        "punch_blockers": [],
        "turnover_readiness": {"completion_pct": 60},
    })

    agent = CommissioningTurnoverAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run(
        context={"project_id": "PRJ-001"}
    )

    agent.chat.assert_called_once()
    assert event.source_agent == "commissioning_turnover"
    assert event.event_type == "commissioning_status"
    assert event.severity == "info"
    assert event.confidence == 0.85


@patch("construction.agents.base.Agent")
async def test_run_blocked_tests_warning(mock_agent_cls):
    """run() sets severity=warning when tests are blocked."""
    mock_response = json.dumps({
        "ist_status": {
            "blocked_tests": ["IST-003"],
            "ready_tests": [],
        },
    })

    agent = CommissioningTurnoverAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run()

    assert event.severity == "warning"
    assert event.requires_cross_agent is True
    assert event.target_agent == "critical_path"


@patch("construction.agents.base.Agent")
async def test_run_handles_non_json(mock_agent_cls):
    """run() handles non-JSON responses gracefully."""
    agent = CommissioningTurnoverAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(
        return_value="All systems ready for commissioning."
    )

    event = await agent.run()

    assert event.source_agent == "commissioning_turnover"
    assert event.severity == "info"
    assert "raw_response" in event.data
