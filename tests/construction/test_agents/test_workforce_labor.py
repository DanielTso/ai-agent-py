"""Tests for the Workforce & Labor agent."""

import json
from unittest.mock import MagicMock, patch

from construction.agents.workforce_labor import (
    WorkforceLaborAgent,
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
    agent = WorkforceLaborAgent(settings=_make_settings())
    assert agent.name == "workforce_labor"
    assert "productivity" in agent.description.lower()
    assert agent.schedule == "daily"


@patch("construction.agents.base.Agent")
def test_system_prompt_set(mock_agent_cls):
    """System prompt contains workforce management guidance."""
    agent = WorkforceLaborAgent(settings=_make_settings())
    prompt = agent.get_system_prompt()
    assert "labor" in prompt.lower()
    assert "productivity" in prompt.lower()
    assert "BICSI" in prompt
    assert "NETA" in prompt
    assert "overtime" in prompt.lower()
    assert "fatigue" in prompt.lower()


@patch("construction.agents.base.Agent")
def test_tools_registered(mock_agent_cls):
    """Agent registers the workforce_query tool."""
    agent = WorkforceLaborAgent(settings=_make_settings())
    tool_names = [
        t.name for t in agent._tools._tools.values()
    ]
    assert "workforce_query" in tool_names
    assert len(tool_names) == 1


@patch("construction.agents.base.Agent")
async def test_run_returns_agent_event(mock_agent_cls):
    """run() calls chat and returns an AgentEvent."""
    mock_response = json.dumps({
        "crew_status": [
            {
                "trade": "electrical",
                "headcount": 24,
                "productivity_pct": 92.0,
            }
        ],
        "certification_warnings": [
            {
                "worker_id": "WRK-101",
                "status": "expiring_soon",
            }
        ],
        "labor_gaps": [],
    })

    agent = WorkforceLaborAgent(settings=_make_settings())
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run(
        context={"project_id": "PRJ-001"}
    )

    agent.chat.assert_called_once()
    call_arg = agent.chat.call_args[0][0]
    assert "PRJ-001" in call_arg

    assert event.source_agent == "workforce_labor"
    assert event.event_type == "workforce_status"
    assert event.severity == "warning"
    assert event.confidence == 0.85
    assert len(event.data_sources) == 1
    assert len(event.transparency_log) >= 4


@patch("construction.agents.base.Agent")
async def test_run_critical_labor_gap(mock_agent_cls):
    """run() sets severity=critical for critical labor gaps."""
    mock_response = json.dumps({
        "certification_warnings": [],
        "labor_gaps": [
            {
                "trade": "electrical",
                "gap": 6,
                "critical": True,
            }
        ],
    })

    agent = WorkforceLaborAgent(settings=_make_settings())
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run()

    assert event.severity == "critical"
    assert event.requires_cross_agent is True
    assert event.target_agent == "risk_forecaster"


@patch("construction.agents.base.Agent")
async def test_run_critical_expired_cert(mock_agent_cls):
    """run() sets severity=critical for expired certifications."""
    mock_response = json.dumps({
        "certification_warnings": [
            {
                "worker_id": "WRK-312",
                "status": "expired",
            }
        ],
        "labor_gaps": [],
    })

    agent = WorkforceLaborAgent(settings=_make_settings())
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run()

    assert event.severity == "critical"
    assert event.requires_cross_agent is True


@patch("construction.agents.base.Agent")
async def test_run_handles_non_json_response(mock_agent_cls):
    """run() handles non-JSON responses gracefully."""
    agent = WorkforceLaborAgent(settings=_make_settings())
    agent.chat = MagicMock(
        return_value="All crews performing well. No issues."
    )

    event = await agent.run()

    assert event.source_agent == "workforce_labor"
    assert event.severity == "info"
    assert "raw_response" in event.data
