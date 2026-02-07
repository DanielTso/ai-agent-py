"""Tests for the Environmental & Sustainability agent."""

import json
from unittest.mock import MagicMock, patch

from construction.agents.environmental_sustainability import (
    EnvironmentalSustainabilityAgent,
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
    agent = EnvironmentalSustainabilityAgent(
        settings=_make_settings()
    )
    assert agent.name == "environmental_sustainability"
    assert "environmental" in agent.description.lower()
    assert agent.schedule == "daily"


@patch("construction.agents.base.Agent")
def test_system_prompt_set(mock_agent_cls):
    """System prompt contains environmental guidance."""
    agent = EnvironmentalSustainabilityAgent(
        settings=_make_settings()
    )
    prompt = agent.get_system_prompt()
    assert "SWPPP" in prompt or "swppp" in prompt.lower()
    assert "LEED" in prompt or "leed" in prompt.lower()
    assert "carbon" in prompt.lower()
    assert "permit" in prompt.lower()
    assert "EPA" in prompt or "epa" in prompt.lower()


@patch("construction.agents.base.Agent")
def test_tools_registered(mock_agent_cls):
    """Agent registers environmental and weather tools."""
    agent = EnvironmentalSustainabilityAgent(
        settings=_make_settings()
    )
    tool_names = [
        t.name for t in agent._tools._tools.values()
    ]
    assert "environmental_query" in tool_names
    assert "weather_forecast" in tool_names
    assert "epa_compliance" in tool_names
    assert len(tool_names) == 3


@patch("construction.agents.base.Agent")
async def test_run_returns_agent_event(mock_agent_cls):
    """run() calls chat and returns an AgentEvent."""
    mock_response = json.dumps({
        "permit_alerts": [],
        "leed_status": {"total_points": 13.0},
        "carbon_tracking": {"on_target": True},
        "swppp_compliance": {"compliant": True},
    })

    agent = EnvironmentalSustainabilityAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run(
        context={"project_id": "PRJ-001"}
    )

    agent.chat.assert_called_once()
    assert event.source_agent == "environmental_sustainability"
    assert event.event_type == "environmental_status"
    assert event.severity == "info"


@patch("construction.agents.base.Agent")
async def test_run_permit_violation_critical(mock_agent_cls):
    """run() sets severity=critical on violation risk."""
    mock_response = json.dumps({
        "permit_alerts": [
            {"permit_type": "air", "risk": "violation"}
        ],
    })

    agent = EnvironmentalSustainabilityAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run()

    assert event.severity == "critical"
    assert event.requires_cross_agent is True
    assert event.target_agent == "compliance"


@patch("construction.agents.base.Agent")
async def test_run_handles_non_json(mock_agent_cls):
    """run() handles non-JSON responses gracefully."""
    agent = EnvironmentalSustainabilityAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(
        return_value="All permits current."
    )

    event = await agent.run()

    assert event.source_agent == "environmental_sustainability"
    assert event.severity == "info"
    assert "raw_response" in event.data
