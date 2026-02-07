"""Tests for the Supply Chain Resilience agent."""

import json
from unittest.mock import MagicMock, patch

from construction.agents.supply_chain import SupplyChainAgent


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
    agent = SupplyChainAgent(settings=_make_settings())
    assert agent.name == "supply_chain"
    assert agent.description == "Monitor 50+ vendors for long-lead items"
    assert agent.schedule == "every_4_hours"


@patch("construction.agents.base.Agent")
def test_system_prompt_set(mock_agent_cls):
    """System prompt contains supply chain guidance."""
    agent = SupplyChainAgent(settings=_make_settings())
    prompt = agent.get_system_prompt()
    assert "supply chain" in prompt.lower()
    assert "vendor" in prompt.lower()
    assert "alternative" in prompt.lower()
    assert "3" in prompt  # 3 alternatives per delay


@patch("construction.agents.base.Agent")
def test_tools_registered(mock_agent_cls):
    """Agent registers supply_chain_monitor and weather tools."""
    agent = SupplyChainAgent(settings=_make_settings())
    tool_names = [
        t.name for t in agent._tools._tools.values()
    ]
    assert "supply_chain_monitor" in tool_names
    assert "weather_forecast" in tool_names
    assert len(tool_names) == 2


@patch("construction.agents.base.Agent")
async def test_run_returns_agent_event(mock_agent_cls):
    """run() calls chat and returns an AgentEvent."""
    mock_response = json.dumps({
        "vendor_statuses": [
            {
                "id": "VND-001",
                "name": "Pacific Steel",
                "status": "delayed",
            }
        ],
        "alerts": [
            {
                "vendor_id": "VND-001",
                "severity": "warning",
                "description": "7-day delay on structural steel",
            }
        ],
    })

    agent = SupplyChainAgent(settings=_make_settings())
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run(context={"project_id": "PRJ-001"})

    agent.chat.assert_called_once()
    call_arg = agent.chat.call_args[0][0]
    assert "PRJ-001" in call_arg

    assert event.source_agent == "supply_chain"
    assert event.event_type == "supply_chain_status"
    assert event.severity == "warning"
    assert event.confidence == 0.82
    assert len(event.data_sources) == 2
    assert len(event.transparency_log) >= 3


@patch("construction.agents.base.Agent")
async def test_run_critical_alert(mock_agent_cls):
    """run() sets severity=critical when critical alerts found."""
    mock_response = json.dumps({
        "alerts": [
            {
                "vendor_id": "VND-001",
                "severity": "critical",
                "description": "Vendor declared force majeure",
            }
        ],
    })

    agent = SupplyChainAgent(settings=_make_settings())
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run()

    assert event.severity == "critical"
    assert event.requires_cross_agent is True
    assert event.target_agent == "risk_forecaster"


@patch("construction.agents.base.Agent")
async def test_run_handles_non_json_response(mock_agent_cls):
    """run() handles non-JSON responses gracefully."""
    agent = SupplyChainAgent(settings=_make_settings())
    agent.chat = MagicMock(
        return_value="All vendors on track. No issues detected."
    )

    event = await agent.run()

    assert event.source_agent == "supply_chain"
    assert event.severity == "info"
    assert "raw_response" in event.data
