"""Tests for cross-agent trigger chains in the orchestrator."""

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
    severity: str = "warning",
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


# --- Financial triggers ---


@pytest.mark.asyncio
async def test_financial_budget_variance_triggers(
    orchestrator,
):
    """Budget variance >10% triggers critical_path and supply_chain."""
    event = _make_event(
        "financial",
        "budget_variance",
        {"variance_pct": 15.0},
    )
    triggers = await orchestrator.handle_event(event)

    assert len(triggers) == 2
    targets = {t.target_agent for t in triggers}
    assert "critical_path" in targets
    assert "supply_chain" in targets
    assert any(
        t.target_action == "cost_reduction_scan"
        for t in triggers
    )


@pytest.mark.asyncio
async def test_financial_low_variance_no_trigger(
    orchestrator,
):
    """Budget variance <=10% does not trigger."""
    event = _make_event(
        "financial",
        "budget_variance",
        {"variance_pct": 5.0},
    )
    triggers = await orchestrator.handle_event(event)
    assert len(triggers) == 0


# --- Workforce triggers ---


@pytest.mark.asyncio
async def test_workforce_labor_shortage_triggers(
    orchestrator,
):
    """Labor shortage triggers critical_path and site_logistics."""
    event = _make_event(
        "workforce",
        "labor_shortage_detected",
        {"trade": "electrical", "gap": 6},
    )
    triggers = await orchestrator.handle_event(event)

    assert len(triggers) == 2
    targets = {t.target_agent for t in triggers}
    assert "critical_path" in targets
    assert "site_logistics" in targets


# --- Commissioning triggers ---


@pytest.mark.asyncio
async def test_commissioning_prerequisite_blocked_triggers(
    orchestrator,
):
    """Blocked IST prerequisite triggers critical_path and supply_chain."""
    event = _make_event(
        "commissioning_turnover",
        "prerequisite_blocked",
        {"test_id": "IST-003"},
    )
    triggers = await orchestrator.handle_event(event)

    assert len(triggers) == 2
    targets = {t.target_agent for t in triggers}
    assert "critical_path" in targets
    assert "supply_chain" in targets


# --- Environmental triggers ---


@pytest.mark.asyncio
async def test_environmental_permit_violation_triggers(
    orchestrator,
):
    """Permit violation risk triggers compliance and risk_forecaster."""
    event = _make_event(
        "environmental_sustainability",
        "permit_violation_risk",
        {"permit_type": "air"},
    )
    triggers = await orchestrator.handle_event(event)

    assert len(triggers) == 2
    targets = {t.target_agent for t in triggers}
    assert "compliance" in targets
    assert "risk_forecaster" in targets


# --- Site logistics triggers ---


@pytest.mark.asyncio
async def test_site_logistics_crane_conflict_triggers(
    orchestrator,
):
    """Crane conflict triggers critical_path and safety_compliance."""
    event = _make_event(
        "site_logistics",
        "crane_conflict",
        {"crane_id": "TC-01"},
    )
    triggers = await orchestrator.handle_event(event)

    assert len(triggers) == 2
    targets = {t.target_agent for t in triggers}
    assert "critical_path" in targets
    assert "safety_compliance" in targets


# --- Safety triggers (HIGHEST PRIORITY) ---


@pytest.mark.asyncio
async def test_safety_stop_work_triggers(orchestrator):
    """Stop-work triggers SMS, site_logistics halt, and critical_path."""
    event = _make_event(
        "safety_compliance",
        "stop_work_recommended",
        {
            "hazard": "Unguarded floor opening",
            "safety_critical": True,
            "description": "Imminent fall hazard Level 5",
        },
        severity="critical",
    )
    triggers = await orchestrator.handle_event(event)

    assert len(triggers) == 2
    targets = {t.target_agent for t in triggers}
    assert "site_logistics" in targets
    assert "critical_path" in targets
    # All triggers should be priority 1
    assert all(t.priority == 1 for t in triggers)
    # SMS should have been sent
    orchestrator.pubsub.publish.assert_called()


@pytest.mark.asyncio
async def test_safety_contractor_high_risk_triggers(
    orchestrator,
):
    """Contractor high risk triggers supply_chain and risk_forecaster."""
    event = _make_event(
        "safety_compliance",
        "contractor_high_risk",
        {"contractor": "XYZ Corp", "trir": 8.5},
    )
    triggers = await orchestrator.handle_event(event)

    assert len(triggers) == 2
    targets = {t.target_agent for t in triggers}
    assert "supply_chain" in targets
    assert "risk_forecaster" in targets


@pytest.mark.asyncio
async def test_safety_exposure_threshold_triggers(
    orchestrator,
):
    """Exposure threshold exceeded triggers environmental and workforce."""
    event = _make_event(
        "safety_compliance",
        "exposure_threshold_exceeded",
        {"substance": "silica", "level": 55},
    )
    triggers = await orchestrator.handle_event(event)

    assert len(triggers) == 2
    targets = {t.target_agent for t in triggers}
    assert "environmental_sustainability" in targets
    assert "workforce" in targets


@pytest.mark.asyncio
async def test_safety_training_expired_triggers(
    orchestrator,
):
    """Training expired triggers workforce and site_logistics."""
    event = _make_event(
        "safety_compliance",
        "training_expired",
        {"worker_id": "WRK-312", "type": "first_aid"},
    )
    triggers = await orchestrator.handle_event(event)

    assert len(triggers) == 2
    targets = {t.target_agent for t in triggers}
    assert "workforce" in targets
    assert "site_logistics" in targets


# --- Weather/heat triggers ---


@pytest.mark.asyncio
async def test_heat_index_exceeded_triggers(orchestrator):
    """Heat index above NIOSH threshold triggers safety, workforce, logistics."""
    event = _make_event(
        "risk_forecaster",
        "heat_index_exceeded",
        {"heat_index": 105, "threshold": 90},
    )
    triggers = await orchestrator.handle_event(event)

    assert len(triggers) == 3
    targets = {t.target_agent for t in triggers}
    assert "safety_compliance" in targets
    assert "workforce" in targets
    assert "site_logistics" in targets


# --- Priority ordering ---


@pytest.mark.asyncio
async def test_stop_work_has_highest_priority(orchestrator):
    """Stop-work triggers have priority 1 (highest)."""
    event = _make_event(
        "safety_compliance",
        "stop_work_recommended",
        {"safety_critical": True, "description": "Imminent danger"},
        severity="critical",
    )
    triggers = await orchestrator.handle_event(event)

    for t in triggers:
        assert t.priority == 1


@pytest.mark.asyncio
async def test_existing_supply_chain_trigger_still_works(
    orchestrator,
):
    """Original supply chain trigger still functions."""
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
async def test_unrecognized_event_still_returns_empty(
    orchestrator,
):
    """Events from unknown agents return no triggers."""
    event = _make_event(
        "unknown_agent",
        "unknown_event",
    )
    triggers = await orchestrator.handle_event(event)
    assert triggers == []
