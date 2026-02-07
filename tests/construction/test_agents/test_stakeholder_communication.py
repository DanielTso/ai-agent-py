"""Tests for the Stakeholder Communication agent."""

import json
from unittest.mock import MagicMock, patch

from construction.agents.stakeholder_communication import (
    StakeholderCommunicationAgent,
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
    agent = StakeholderCommunicationAgent(
        settings=_make_settings()
    )
    assert agent.name == "stakeholder_communication"
    assert "owner reports" in agent.description.lower()
    assert agent.schedule == "on_demand"


@patch("construction.agents.base.Agent")
def test_system_prompt_set(mock_agent_cls):
    """System prompt contains communication guidance."""
    agent = StakeholderCommunicationAgent(
        settings=_make_settings()
    )
    prompt = agent.get_system_prompt()
    assert "communication" in prompt.lower()
    assert "owner" in prompt.lower()
    assert "contractual" in prompt.lower()
    assert "NEVER make decisions" in prompt
    assert "contract clause" in prompt.lower()


@patch("construction.agents.base.Agent")
def test_tools_registered(mock_agent_cls):
    """Agent registers the draft_communication tool."""
    agent = StakeholderCommunicationAgent(
        settings=_make_settings()
    )
    tool_names = [
        t.name for t in agent._tools._tools.values()
    ]
    assert "draft_communication" in tool_names
    assert len(tool_names) == 1


@patch("construction.agents.base.Agent")
async def test_run_returns_agent_event(mock_agent_cls):
    """run() calls chat and returns an AgentEvent."""
    mock_response = json.dumps({
        "report_type": "owner_update",
        "title": "Weekly Update",
        "body": "Project on track.",
        "status": "draft",
    })

    agent = StakeholderCommunicationAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run(
        context={
            "project_id": "PRJ-001",
            "action": "owner_update",
        }
    )

    agent.chat.assert_called_once()
    call_arg = agent.chat.call_args[0][0]
    assert "PRJ-001" in call_arg
    assert "owner_update" in call_arg

    assert event.source_agent == "stakeholder_communication"
    assert event.event_type == "communication_draft"
    assert event.severity == "info"
    assert event.confidence == 0.80
    assert len(event.data_sources) == 1
    assert len(event.transparency_log) >= 3


@patch("construction.agents.base.Agent")
async def test_run_default_action(mock_agent_cls):
    """run() defaults to owner_update when no action specified."""
    mock_response = json.dumps({"status": "draft"})

    agent = StakeholderCommunicationAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(return_value=mock_response)

    await agent.run()

    call_arg = agent.chat.call_args[0][0]
    assert "owner_update" in call_arg


@patch("construction.agents.base.Agent")
async def test_run_handles_non_json_response(mock_agent_cls):
    """run() handles non-JSON responses gracefully."""
    agent = StakeholderCommunicationAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(
        return_value="Draft report attached for review."
    )

    event = await agent.run()

    assert event.source_agent == "stakeholder_communication"
    assert event.severity == "info"
    assert "raw_response" in event.data


@patch("construction.agents.base.Agent")
async def test_run_no_cross_agent(mock_agent_cls):
    """Communication agent never triggers cross-agent events."""
    mock_response = json.dumps({"status": "draft"})

    agent = StakeholderCommunicationAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run()

    assert event.requires_cross_agent is False
    assert event.target_agent is None
