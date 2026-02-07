"""Tests for the Safety Compliance agent."""

import json
from unittest.mock import MagicMock, patch

from construction.agents.safety_compliance import (
    SafetyComplianceAgent,
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
    agent = SafetyComplianceAgent(
        settings=_make_settings()
    )
    assert agent.name == "safety_compliance"
    assert "safety" in agent.description.lower()
    assert agent.schedule == "continuous"


@patch("construction.agents.base.Agent")
def test_system_prompt_set(mock_agent_cls):
    """System prompt contains safety guidance."""
    agent = SafetyComplianceAgent(
        settings=_make_settings()
    )
    prompt = agent.get_system_prompt()
    assert "OSHA" in prompt
    assert "MSHA" in prompt
    assert "NIOSH" in prompt
    assert "NFPA" in prompt
    assert "Focus Four" in prompt or "focus four" in prompt.lower()
    assert "stop-work" in prompt.lower() or "stop_work" in prompt.lower()
    assert "1926" in prompt


@patch("construction.agents.base.Agent")
def test_tools_registered(mock_agent_cls):
    """Agent registers all 6 safety tools."""
    agent = SafetyComplianceAgent(
        settings=_make_settings()
    )
    tool_names = [
        t.name for t in agent._tools._tools.values()
    ]
    assert "osha_compliance" in tool_names
    assert "msha_compliance" in tool_names
    assert "niosh_lookup" in tool_names
    assert "safety_metrics" in tool_names
    assert "hazard_analysis" in tool_names
    assert "training_tracker" in tool_names
    assert "nfpa_compliance" in tool_names
    assert len(tool_names) == 7


@patch("construction.agents.base.Agent")
async def test_run_returns_agent_event(mock_agent_cls):
    """run() calls chat and returns an AgentEvent."""
    mock_response = json.dumps({
        "safety_metrics": {"trir": 2.16, "dart": 1.08},
        "focus_four_status": {"falls": "compliant"},
        "stop_work_recommendations": [],
        "training_alerts": {"expired": []},
        "exposure_monitoring": {"exceedances": []},
    })

    agent = SafetyComplianceAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run(
        context={"project_id": "PRJ-001"}
    )

    agent.chat.assert_called_once()
    assert event.source_agent == "safety_compliance"
    assert event.event_type == "safety_status"
    assert event.severity == "info"
    assert event.confidence == 0.95
    assert len(event.data_sources) == 4


@patch("construction.agents.base.Agent")
async def test_run_stop_work_critical(mock_agent_cls):
    """run() sets severity=critical when stop-work recommended."""
    mock_response = json.dumps({
        "stop_work_recommendations": [
            {"hazard": "Unguarded floor opening Level 5"}
        ],
        "training_alerts": {"expired": []},
        "exposure_monitoring": {"exceedances": []},
    })

    agent = SafetyComplianceAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run()

    assert event.severity == "critical"
    assert event.requires_cross_agent is True
    assert event.target_agent == "site_logistics"


@patch("construction.agents.base.Agent")
async def test_run_exposure_warning(mock_agent_cls):
    """run() sets severity=warning on exposure exceedances."""
    mock_response = json.dumps({
        "stop_work_recommendations": [],
        "training_alerts": {"expired": []},
        "exposure_monitoring": {
            "exceedances": [
                {"substance": "silica", "level": 55}
            ]
        },
    })

    agent = SafetyComplianceAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run()

    assert event.severity == "warning"


@patch("construction.agents.base.Agent")
async def test_run_training_expired_warning(mock_agent_cls):
    """run() sets severity=warning on expired training."""
    mock_response = json.dumps({
        "stop_work_recommendations": [],
        "training_alerts": {
            "expired": [
                {"worker": "WRK-312", "type": "first_aid"}
            ]
        },
        "exposure_monitoring": {"exceedances": []},
    })

    agent = SafetyComplianceAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(return_value=mock_response)

    event = await agent.run()

    assert event.severity == "warning"


@patch("construction.agents.base.Agent")
async def test_run_handles_non_json(mock_agent_cls):
    """run() handles non-JSON responses gracefully."""
    agent = SafetyComplianceAgent(
        settings=_make_settings()
    )
    agent.chat = MagicMock(
        return_value="Site is safe, no issues found."
    )

    event = await agent.run()

    assert event.source_agent == "safety_compliance"
    assert event.severity == "info"
    assert "raw_response" in event.data
