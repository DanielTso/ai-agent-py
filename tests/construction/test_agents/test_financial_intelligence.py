"""Tests for the Financial Intelligence agent."""

import json
from unittest.mock import MagicMock, patch

from construction.agents.financial_intelligence import (
    FinancialIntelligenceAgent,
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
    agent = FinancialIntelligenceAgent(
        settings=_make_settings()
    )
    assert agent.name == "financial_intelligence"
    assert "Earned value" in agent.description
    assert agent.schedule == "daily"


@patch("construction.agents.base.Agent")
def test_system_prompt_set(mock_agent_cls):
    """System prompt contains financial analysis guidance."""
    agent = FinancialIntelligenceAgent(
        settings=_make_settings()
    )
    prompt = agent.get_system_prompt()
    assert "financial" in prompt.lower()
    assert "CPI" in prompt
    assert "SPI" in prompt
    assert "EAC" in prompt
    assert "10%" in prompt


@patch("construction.agents.base.Agent")
def test_tools_registered(mock_agent_cls):
    """Agent registers the financial_query tool."""
    agent = FinancialIntelligenceAgent(
        settings=_make_settings()
    )
    tool_names = [
        t.name for t in agent._tools._tools.values()
    ]
    assert "financial_query" in tool_names
    assert len(tool_names) == 1


@patch("construction.agents.base.Agent")
async def test_run_returns_agent_event(mock_agent_cls):
    """run() calls chat and returns an AgentEvent."""
    mock_response = json.dumps({
        "budget_status": {
            "variance_pct": 2.67,
            "on_budget": True,
        },
        "evm_metrics": {"cpi": 0.987, "spi": 0.925},
        "alerts": [
            {
                "severity": "warning",
                "description": "SPI below 0.95",
            }
        ],
    })

    agent = FinancialIntelligenceAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run(
        context={"project_id": "PRJ-001"}
    )

    agent.chat.assert_called_once()
    call_arg = agent.chat.call_args[0][0]
    assert "PRJ-001" in call_arg

    assert event.source_agent == "financial_intelligence"
    assert event.event_type == "financial_analysis"
    assert event.severity == "warning"
    assert event.confidence == 0.88
    assert len(event.data_sources) == 1
    assert len(event.transparency_log) >= 4


@patch("construction.agents.base.Agent")
async def test_run_critical_alert(mock_agent_cls):
    """run() sets severity=critical for critical alerts."""
    mock_response = json.dumps({
        "alerts": [
            {
                "severity": "critical",
                "description": "Budget overrun exceeds 15%",
            }
        ],
    })

    agent = FinancialIntelligenceAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run()

    assert event.severity == "critical"
    assert event.requires_cross_agent is True
    assert event.target_agent == "risk_forecaster"


@patch("construction.agents.base.Agent")
async def test_run_handles_non_json_response(mock_agent_cls):
    """run() handles non-JSON responses gracefully."""
    agent = FinancialIntelligenceAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(
        return_value="Project is on budget. No concerns."
    )

    event = await agent.run()

    assert event.source_agent == "financial_intelligence"
    assert event.severity == "info"
    assert "raw_response" in event.data
