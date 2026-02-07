"""Tests for the ComplianceVerifier agent."""

from unittest.mock import MagicMock, patch

import pytest

from construction.agents.compliance_verifier import ComplianceVerifier


def _make_settings():
    """Create mock ConstructionSettings."""
    settings = MagicMock()
    settings.anthropic_api_key = "test-key"
    settings.model = "claude-sonnet-4-5-20250929"
    settings.max_tokens = 100
    return settings


@patch("construction.agents.base.Agent")
def test_agent_initialization(mock_agent_cls):
    agent = ComplianceVerifier(settings=_make_settings())
    assert agent.name == "compliance_verifier"
    assert agent.description == "Verify installations against BIM + codes"
    assert agent.schedule == "twice_daily"


@patch("construction.agents.base.Agent")
def test_system_prompt_content(mock_agent_cls):
    agent = ComplianceVerifier(settings=_make_settings())
    prompt = agent.get_system_prompt()
    assert "BIM" in prompt
    assert "compliance" in prompt.lower()
    assert "redundancy path" in prompt
    assert "fire separation" in prompt
    assert "egress" in prompt
    assert "critical" in prompt
    assert "ICC" in prompt
    assert "Uptime Institute" in prompt or "Tier" in prompt


@patch("construction.agents.base.Agent")
def test_tools_registered(mock_agent_cls):
    agent = ComplianceVerifier(settings=_make_settings())
    assert agent._tools.get("bim_query") is not None
    assert agent._tools.get("compliance_database") is not None
    assert agent._tools.get("icc_codes") is not None
    assert agent._tools.get("tier_certification") is not None
    assert len(agent._tools) == 4


@pytest.mark.asyncio
@patch("construction.agents.base.Agent")
async def test_run_default_checks(mock_agent_cls):
    agent = ComplianceVerifier(settings=_make_settings())
    agent.pubsub = None
    agent.shared_memory = None

    event = await agent.run(context={"project_id": "PROJ-TEST"})

    assert event.source_agent == "compliance_verifier"
    assert event.event_type == "compliance_check"
    data = event.data
    assert data["checks_performed"] > 0
    assert "checks" in data
    assert "deviations" in data
    assert "tickets_created" in data
    assert "summary" in data


@pytest.mark.asyncio
@patch("construction.agents.base.Agent")
async def test_run_creates_tickets_for_critical(mock_agent_cls):
    agent = ComplianceVerifier(settings=_make_settings())
    agent.pubsub = None
    agent.shared_memory = None

    event = await agent.run()
    data = event.data

    assert data["critical_count"] > 0
    assert len(data["tickets_created"]) > 0


@pytest.mark.asyncio
@patch("construction.agents.base.Agent")
async def test_run_severity_escalation(mock_agent_cls):
    agent = ComplianceVerifier(settings=_make_settings())
    agent.pubsub = None
    agent.shared_memory = None

    event = await agent.run()

    # Default mock data has critical checks
    assert event.severity == "critical"
    assert event.requires_cross_agent is True
    assert event.target_agent == "critical_path"


@pytest.mark.asyncio
@patch("construction.agents.base.Agent")
async def test_run_with_specific_check_types(mock_agent_cls):
    agent = ComplianceVerifier(settings=_make_settings())
    agent.pubsub = None
    agent.shared_memory = None

    event = await agent.run(context={
        "project_id": "PROJ-001",
        "check_types": ["egress"],
    })

    data = event.data
    # Only egress checks
    for check in data["checks"]:
        assert check["check_type"] == "egress"


@pytest.mark.asyncio
@patch("construction.agents.base.Agent")
async def test_run_data_sources(mock_agent_cls):
    agent = ComplianceVerifier(settings=_make_settings())
    agent.pubsub = None
    agent.shared_memory = None

    event = await agent.run()

    assert len(event.data_sources) == 2
    source_names = {ds.source_name for ds in event.data_sources}
    assert "autodesk_bim360" in source_names
    assert "compliance_database" in source_names


@pytest.mark.asyncio
@patch("construction.agents.base.Agent")
async def test_run_transparency_log(mock_agent_cls):
    agent = ComplianceVerifier(settings=_make_settings())
    agent.pubsub = None
    agent.shared_memory = None

    event = await agent.run()

    assert len(event.transparency_log) > 0
    log_text = " ".join(event.transparency_log)
    assert "compliance check" in log_text
    assert "deviations" in log_text.lower()
