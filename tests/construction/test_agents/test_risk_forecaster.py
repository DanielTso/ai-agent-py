"""Tests for the Risk Forecaster agent."""

import json
from unittest.mock import MagicMock, patch

from construction.agents.risk_forecaster import RiskForecasterAgent


def _make_settings(**overrides):
    """Create mock ConstructionSettings."""
    defaults = {
        "anthropic_api_key": "fake-key",
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 4096,
        "openweathermap_api_key": "",
        "risk_probability_threshold": 0.15,
        "risk_impact_threshold": 100000.0,
    }
    defaults.update(overrides)
    mock = MagicMock()
    for k, v in defaults.items():
        setattr(mock, k, v)
    return mock


@patch("construction.agents.base.Agent")
def test_initialization(mock_agent_cls):
    """Agent initializes with correct name and description."""
    agent = RiskForecasterAgent(settings=_make_settings())
    assert agent.name == "risk_forecaster"
    assert agent.description == "Predict schedule/cost/safety risks 14+ days ahead"
    assert agent.schedule == "hourly"


@patch("construction.agents.base.Agent")
def test_system_prompt_set(mock_agent_cls):
    """System prompt contains risk analysis guidance."""
    agent = RiskForecasterAgent(settings=_make_settings())
    prompt = agent.get_system_prompt()
    assert "risk analyst" in prompt.lower()
    assert "15%" in prompt or "Probability > 15%" in prompt
    assert "$100,000" in prompt or "$100k" in prompt
    assert "safety-critical" in prompt.lower() or "safety" in prompt.lower()


@patch("construction.agents.base.Agent")
def test_tools_registered(mock_agent_cls):
    """Agent registers weather, OSHA, and risk database tools."""
    agent = RiskForecasterAgent(settings=_make_settings())
    tool_names = [
        t.name for t in agent._tools._tools.values()
    ]
    assert "weather_forecast" in tool_names
    assert "osha_search" in tool_names
    assert "risk_database" in tool_names
    assert len(tool_names) == 3


@patch("construction.agents.base.Agent")
async def test_run_returns_agent_event(mock_agent_cls):
    """run() calls chat and returns an AgentEvent."""
    mock_response = json.dumps({
        "risks": [
            {
                "category": "weather",
                "description": "Storm approaching site",
                "probability": 0.4,
                "impact_dollars": 200000,
                "impact_days": 3,
                "safety_critical": False,
                "confidence": 0.75,
            }
        ]
    })

    agent = RiskForecasterAgent(settings=_make_settings())
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run(context={"project_id": "PRJ-001"})

    agent.chat.assert_called_once()
    call_arg = agent.chat.call_args[0][0]
    assert "PRJ-001" in call_arg

    assert event.source_agent == "risk_forecaster"
    assert event.event_type == "risk_assessment"
    assert event.severity == "warning"
    assert event.confidence == 0.80
    assert len(event.data_sources) == 3
    assert len(event.transparency_log) >= 3


@patch("construction.agents.base.Agent")
async def test_run_critical_safety_risk(mock_agent_cls):
    """run() sets severity=critical when safety_critical risk found."""
    mock_response = json.dumps({
        "risks": [
            {
                "category": "safety",
                "description": "Crane near power lines",
                "probability": 0.2,
                "impact_dollars": 1000000,
                "impact_days": 30,
                "safety_critical": True,
                "confidence": 0.9,
            }
        ]
    })

    agent = RiskForecasterAgent(settings=_make_settings())
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run()

    assert event.severity == "critical"
    assert event.requires_cross_agent is True
    assert event.target_agent == "supply_chain"


@patch("construction.agents.base.Agent")
async def test_run_handles_non_json_response(mock_agent_cls):
    """run() handles non-JSON responses gracefully."""
    agent = RiskForecasterAgent(settings=_make_settings())
    agent.chat = MagicMock(
        return_value="No significant risks identified at this time."
    )

    event = await agent.run()

    assert event.source_agent == "risk_forecaster"
    assert event.severity == "info"
    assert "raw_response" in event.data
