"""Tests for the Site Logistics agent."""

import json
from unittest.mock import MagicMock, patch

from construction.agents.site_logistics import (
    SiteLogisticsAgent,
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
    agent = SiteLogisticsAgent(
        settings=_make_settings()
    )
    assert agent.name == "site_logistics"
    assert "site" in agent.description.lower()
    assert agent.schedule == "real_time"


@patch("construction.agents.base.Agent")
def test_system_prompt_set(mock_agent_cls):
    """System prompt contains logistics guidance."""
    agent = SiteLogisticsAgent(
        settings=_make_settings()
    )
    prompt = agent.get_system_prompt()
    assert "crane" in prompt.lower()
    assert "staging" in prompt.lower()
    assert "headcount" in prompt.lower()
    assert "safety" in prompt.lower()
    assert "NOT" in prompt or "not" in prompt.lower()


@patch("construction.agents.base.Agent")
def test_tools_registered(mock_agent_cls):
    """Agent registers site logistics tool."""
    agent = SiteLogisticsAgent(
        settings=_make_settings()
    )
    tool_names = [
        t.name for t in agent._tools._tools.values()
    ]
    assert "site_logistics_query" in tool_names
    assert len(tool_names) == 1


@patch("construction.agents.base.Agent")
async def test_run_returns_agent_event(mock_agent_cls):
    """run() calls chat and returns an AgentEvent."""
    mock_response = json.dumps({
        "crane_conflicts": [],
        "staging_alerts": [],
        "headcount_variance": {},
        "permit_status": [],
    })

    agent = SiteLogisticsAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run(
        context={"project_id": "PRJ-001"}
    )

    agent.chat.assert_called_once()
    assert event.source_agent == "site_logistics"
    assert event.event_type == "site_logistics_status"
    assert event.severity == "info"


@patch("construction.agents.base.Agent")
async def test_run_crane_conflict_warning(mock_agent_cls):
    """run() sets severity=warning when crane conflicts found."""
    mock_response = json.dumps({
        "crane_conflicts": [
            {"crane_id": "TC-01", "conflict": "double-booked"}
        ],
    })

    agent = SiteLogisticsAgent(
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
    agent = SiteLogisticsAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(
        return_value="Site operations running smoothly."
    )

    event = await agent.run()

    assert event.source_agent == "site_logistics"
    assert event.severity == "info"
    assert "raw_response" in event.data
