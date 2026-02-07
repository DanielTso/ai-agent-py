"""Tests for the CriticalPathOptimizer agent."""

from unittest.mock import MagicMock, patch

import pytest

from construction.agents.critical_path import CriticalPathOptimizer


def _make_settings():
    """Create mock ConstructionSettings."""
    settings = MagicMock()
    settings.anthropic_api_key = "test-key"
    settings.model = "claude-sonnet-4-5-20250929"
    settings.max_tokens = 100
    return settings


@patch("construction.agents.base.Agent")
def test_agent_initialization(mock_agent_cls):
    agent = CriticalPathOptimizer(settings=_make_settings())
    assert agent.name == "critical_path"
    assert agent.description == "Dynamic resequencing + Monte Carlo simulation"
    assert agent.schedule == "on_demand"


@patch("construction.agents.base.Agent")
def test_system_prompt_content(mock_agent_cls):
    agent = CriticalPathOptimizer(settings=_make_settings())
    prompt = agent.get_system_prompt()
    assert "CPM" in prompt
    assert "Tier" in prompt
    assert "NEVER compromise" in prompt
    assert "Monte Carlo" in prompt
    assert "redundant cooling loops" in prompt


@patch("construction.agents.base.Agent")
def test_tools_registered(mock_agent_cls):
    agent = CriticalPathOptimizer(settings=_make_settings())
    assert agent._tools.get("schedule_query") is not None
    assert agent._tools.get("monte_carlo_simulation") is not None
    assert len(agent._tools) == 2


@pytest.mark.asyncio
@patch("construction.agents.base.Agent")
async def test_run_with_delay_context(mock_agent_cls):
    agent = CriticalPathOptimizer(settings=_make_settings())
    agent.pubsub = None
    agent.shared_memory = None

    context = {
        "project_id": "PROJ-TEST",
        "delay_days": 7,
        "affected_activities": ["ACT-002"],
    }

    event = await agent.run(context=context)

    assert event.source_agent == "critical_path"
    assert event.event_type == "schedule_analysis"
    data = event.data
    assert "critical_path" in data
    assert "monte_carlo" in data
    assert "resequencing_options" in data
    assert data["delay_context"]["delay_days"] == 7
    assert event.requires_cross_agent is True
    assert event.target_agent == "risk_forecaster"


@pytest.mark.asyncio
@patch("construction.agents.base.Agent")
async def test_run_no_delay(mock_agent_cls):
    agent = CriticalPathOptimizer(settings=_make_settings())
    agent.pubsub = None
    agent.shared_memory = None

    event = await agent.run(context={"project_id": "PROJ-001"})

    assert event.severity == "info"
    assert event.requires_cross_agent is False
    data = event.data
    assert "approval_request" not in data


@pytest.mark.asyncio
@patch("construction.agents.base.Agent")
async def test_run_critical_delay(mock_agent_cls):
    agent = CriticalPathOptimizer(settings=_make_settings())
    agent.pubsub = None
    agent.shared_memory = None

    event = await agent.run(context={
        "project_id": "PROJ-001",
        "delay_days": 15,
    })

    assert event.severity == "critical"


@pytest.mark.asyncio
@patch("construction.agents.base.Agent")
async def test_monte_carlo_integration(mock_agent_cls):
    """Verify the agent actually runs Monte Carlo and gets numeric results."""
    agent = CriticalPathOptimizer(settings=_make_settings())
    agent.pubsub = None
    agent.shared_memory = None

    event = await agent.run(context={"project_id": "PROJ-001"})
    mc = event.data["monte_carlo"]

    assert mc["p50"] is not None
    assert mc["p80"] is not None
    assert mc["p95"] is not None
    assert isinstance(mc["confidence"], float)


@pytest.mark.asyncio
@patch("construction.agents.base.Agent")
async def test_run_creates_approval_for_delay(mock_agent_cls):
    agent = CriticalPathOptimizer(settings=_make_settings())
    agent.pubsub = None
    agent.shared_memory = None

    event = await agent.run(context={
        "project_id": "PROJ-001",
        "delay_days": 10,
    })

    data = event.data
    assert "approval_request" in data
    approval = data["approval_request"]
    assert approval["agent_name"] == "critical_path"
    assert approval["action_type"] == "schedule_resequence"
    assert approval["status"] == "pending"
