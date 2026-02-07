"""Tests for the Orchestrator."""

import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from construction.agents.orchestrator import Orchestrator
from construction.schemas.common import AgentEvent


@pytest.fixture
def mock_settings():
    settings = MagicMock()
    settings.escalation_impact_threshold = 250000.0
    settings.pm_phone_number = "+15559999999"
    settings.dedup_ttl_seconds = 14400
    return settings


@pytest.fixture
def mock_shared_memory():
    mem = AsyncMock()
    mem.check_dedup.return_value = False
    mem.get_active_risks.return_value = [
        ("risk-1", 9.5),
        ("risk-2", 8.2),
        ("risk-3", 7.1),
    ]
    return mem


@pytest.fixture
def mock_pubsub():
    return AsyncMock()


@pytest.fixture
def orchestrator(mock_settings, mock_shared_memory, mock_pubsub):
    return Orchestrator(
        settings=mock_settings,
        shared_memory=mock_shared_memory,
        pubsub=mock_pubsub,
        agents={},
    )


def _make_event(
    source_agent: str,
    event_type: str,
    data: dict | None = None,
    severity: str = "critical",
) -> AgentEvent:
    return AgentEvent(
        event_id=str(uuid.uuid4()),
        source_agent=source_agent,
        event_type=event_type,
        severity=severity,
        timestamp=datetime.now(UTC),
        data=data or {},
        confidence=0.9,
    )


# --- Event handling tests ---


@pytest.mark.asyncio
async def test_supply_chain_critical_delay_triggers_reoptimize(
    orchestrator,
):
    event = _make_event(
        "supply_chain",
        "critical_delay",
        {"impact_dollars": 100000},
    )
    triggers = await orchestrator.handle_event(event)

    assert len(triggers) == 1
    assert triggers[0].target_agent == "critical_path"
    assert triggers[0].target_action == "reoptimize"


@pytest.mark.asyncio
async def test_supply_chain_high_impact_triggers_sms(
    orchestrator,
):
    event = _make_event(
        "supply_chain",
        "critical_delay",
        {"impact_dollars": 500000, "description": "Major delay"},
    )
    triggers = await orchestrator.handle_event(event)

    # Should trigger critical_path reoptimize
    assert any(
        t.target_agent == "critical_path" for t in triggers
    )
    # SMS should have been sent (notification tool called)
    orchestrator.pubsub.publish.assert_called()


@pytest.mark.asyncio
async def test_risk_forecaster_safety_critical_triggers(
    orchestrator,
):
    event = _make_event(
        "risk_forecaster",
        "safety_critical",
        {"safety_critical": True, "description": "Fall hazard"},
    )
    triggers = await orchestrator.handle_event(event)

    assert len(triggers) == 1
    assert triggers[0].target_agent == "compliance"
    assert triggers[0].target_action == "focused_check"
    assert triggers[0].priority == 1
    # SMS escalation should have been triggered
    orchestrator.pubsub.publish.assert_called()


@pytest.mark.asyncio
async def test_compliance_critical_deviation_triggers(
    orchestrator,
):
    event = _make_event(
        "compliance",
        "critical_deviation",
        {"description": "Code violation found"},
    )
    triggers = await orchestrator.handle_event(event)

    assert len(triggers) == 1
    assert triggers[0].target_agent == "risk_forecaster"
    assert triggers[0].target_action == "reassess"


@pytest.mark.asyncio
async def test_document_intelligence_contradiction_triggers(
    orchestrator,
):
    event = _make_event(
        "document_intelligence",
        "contradiction_detected",
        {"description": "Voltage mismatch"},
    )
    triggers = await orchestrator.handle_event(event)

    assert len(triggers) == 1
    assert triggers[0].target_agent == "compliance"
    assert triggers[0].target_action == "focused_check"


@pytest.mark.asyncio
async def test_unrecognized_event_returns_no_triggers(
    orchestrator,
):
    event = _make_event(
        "unknown_agent",
        "unknown_event",
    )
    triggers = await orchestrator.handle_event(event)
    assert triggers == []


# --- Daily brief tests ---


@pytest.mark.asyncio
async def test_daily_brief_generation(orchestrator):
    brief = await orchestrator.generate_daily_brief("proj-001")

    assert len(brief.top_threats) == 3
    assert len(brief.quality_gaps) == 2
    assert brief.acceleration is not None
    assert "Daily Brief" in brief.full_text
    assert brief.top_threats[0].rank == 1


@pytest.mark.asyncio
async def test_daily_brief_without_shared_memory(
    mock_settings, mock_pubsub
):
    orch = Orchestrator(
        settings=mock_settings,
        shared_memory=None,
        pubsub=mock_pubsub,
        agents={},
    )
    brief = await orch.generate_daily_brief("proj-001")

    assert len(brief.top_threats) == 3
    assert len(brief.quality_gaps) == 2


# --- Escalation check tests ---


@pytest.mark.asyncio
async def test_escalation_check_safety_critical(orchestrator):
    event = _make_event(
        "risk_forecaster",
        "safety_critical",
        {"safety_critical": True, "impact_dollars": 0},
    )
    should_escalate = await orchestrator.check_escalation(
        event
    )
    assert should_escalate is True


@pytest.mark.asyncio
async def test_escalation_check_high_impact(orchestrator):
    event = _make_event(
        "supply_chain",
        "critical_delay",
        {"safety_critical": False, "impact_dollars": 300000},
    )
    should_escalate = await orchestrator.check_escalation(
        event
    )
    assert should_escalate is True


@pytest.mark.asyncio
async def test_escalation_check_low_impact_not_safety(
    orchestrator,
):
    event = _make_event(
        "supply_chain",
        "delay",
        {"safety_critical": False, "impact_dollars": 50000},
    )
    should_escalate = await orchestrator.check_escalation(
        event
    )
    assert should_escalate is False


# --- Dedup tests ---


@pytest.mark.asyncio
async def test_dedup_first_alert_not_duplicate(orchestrator):
    event = _make_event(
        "risk_forecaster",
        "safety_critical",
        {"description": "unique alert"},
    )
    is_dup = await orchestrator.check_dedup(event)
    assert is_dup is False
    orchestrator.shared_memory.mark_dedup.assert_called_once()


@pytest.mark.asyncio
async def test_dedup_second_alert_is_duplicate(orchestrator):
    orchestrator.shared_memory.check_dedup.return_value = True

    event = _make_event(
        "risk_forecaster",
        "safety_critical",
        {"description": "duplicate alert"},
    )
    is_dup = await orchestrator.check_dedup(event)
    assert is_dup is True


@pytest.mark.asyncio
async def test_dedup_without_shared_memory(
    mock_settings, mock_pubsub
):
    orch = Orchestrator(
        settings=mock_settings,
        shared_memory=None,
        pubsub=mock_pubsub,
        agents={},
    )
    event = _make_event("test", "test")
    is_dup = await orch.check_dedup(event)
    assert is_dup is False


# --- Approval processing tests ---


@pytest.mark.asyncio
async def test_process_approval_approved(orchestrator):
    await orchestrator.process_approval(
        approval_id="apr-001",
        approved=True,
        notes="Looks good",
    )
    orchestrator.pubsub.publish.assert_called_once()
    call_args = orchestrator.pubsub.publish.call_args
    assert call_args[0][0] == "channel:approval_updates"


@pytest.mark.asyncio
async def test_process_approval_rejected(orchestrator):
    await orchestrator.process_approval(
        approval_id="apr-002",
        approved=False,
        notes="Need more data",
    )
    # Rejected approvals should NOT publish to approval_updates
    orchestrator.pubsub.publish.assert_not_called()


@pytest.mark.asyncio
async def test_process_approval_without_pubsub(
    mock_settings, mock_shared_memory
):
    orch = Orchestrator(
        settings=mock_settings,
        shared_memory=mock_shared_memory,
        pubsub=None,
        agents={},
    )
    # Should not raise
    await orch.process_approval(
        approval_id="apr-003",
        approved=True,
        notes="OK",
    )
