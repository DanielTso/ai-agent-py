"""Tests for the Claims & Dispute agent."""

import json
from unittest.mock import MagicMock, patch

from construction.agents.claims_dispute import (
    ClaimsDisputeAgent,
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
    agent = ClaimsDisputeAgent(
        settings=_make_settings()
    )
    assert agent.name == "claims_dispute"
    assert "claims" in agent.description.lower()
    assert agent.schedule == "continuous"


@patch("construction.agents.base.Agent")
def test_system_prompt_set(mock_agent_cls):
    """System prompt contains claims guidance."""
    agent = ClaimsDisputeAgent(
        settings=_make_settings()
    )
    prompt = agent.get_system_prompt()
    assert "claims" in prompt.lower()
    assert "NEVER" in prompt or "never" in prompt.lower()
    assert "notice" in prompt.lower()
    assert "delay" in prompt.lower()
    assert "TIA" in prompt or "tia" in prompt.lower()


@patch("construction.agents.base.Agent")
def test_tools_registered(mock_agent_cls):
    """Agent registers claims query tool."""
    agent = ClaimsDisputeAgent(
        settings=_make_settings()
    )
    tool_names = [
        t.name for t in agent._tools._tools.values()
    ]
    assert "claims_query" in tool_names
    assert len(tool_names) == 1


@patch("construction.agents.base.Agent")
async def test_run_returns_agent_event(mock_agent_cls):
    """run() calls chat and returns an AgentEvent."""
    mock_response = json.dumps({
        "pending_notices": [],
        "delay_status": {"total_delay_days": 14},
        "new_events": [],
    })

    agent = ClaimsDisputeAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run(
        context={"project_id": "PRJ-001"}
    )

    agent.chat.assert_called_once()
    assert event.source_agent == "claims_dispute"
    assert event.event_type == "claims_status"
    assert event.severity == "info"
    assert event.confidence == 0.90


@patch("construction.agents.base.Agent")
async def test_run_urgent_notice_critical(mock_agent_cls):
    """run() sets severity=critical when notice deadline <= 3 days."""
    mock_response = json.dumps({
        "pending_notices": [
            {
                "id": "NTC-002",
                "days_remaining": 2,
            }
        ],
    })

    agent = ClaimsDisputeAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run()

    assert event.severity == "critical"
    assert event.requires_cross_agent is True
    assert event.target_agent == "critical_path"


@patch("construction.agents.base.Agent")
async def test_run_handles_non_json(mock_agent_cls):
    """run() handles non-JSON responses gracefully."""
    agent = ClaimsDisputeAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(
        return_value="No pending claims activity."
    )

    event = await agent.run()

    assert event.source_agent == "claims_dispute"
    assert event.severity == "info"
    assert "raw_response" in event.data
