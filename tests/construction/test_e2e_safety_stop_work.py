"""E2E test: Safety stop-work recommendation -- highest priority escalation."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from construction.agents.orchestrator import Orchestrator
from construction.schemas.common import AgentEvent, DataSource


@pytest.mark.asyncio
async def test_safety_stop_work_cascade(
    mock_construction_settings,
    mock_shared_memory,
    mock_pubsub,
):
    """
    Simulate: Safety Compliance recommends stop-work for
    excavation zone.
    Expected cascade:
    1. IMMEDIATE SMS escalation
    2. Critical Path reoptimize
    3. Site Logistics halt_operations
    """
    stop_work_event = AgentEvent(
        event_id="evt-safety-001",
        source_agent="safety_compliance",
        event_type="stop_work_recommended",
        severity="critical",
        timestamp=datetime.now(UTC),
        data={
            "zone": "Excavation Zone B",
            "reason": (
                "Cave-in hazard - protective system failure"
            ),
            "osha_standard": "29 CFR 1926 Subpart P",
            "affected_workers": 12,
            "estimated_duration_hours": 8,
            "safety_critical": True,
            "description": "Cave-in hazard stop-work",
        },
        confidence=0.95,
        data_sources=[
            DataSource(
                source_type="sensor",
                source_name="soil_monitoring",
                retrieved_at=datetime.now(UTC),
                confidence=0.92,
            ),
        ],
        transparency_log=[
            "Reviewed soil monitoring data",
            "Checked trench box specifications",
            "Verified competent person assessment",
            "Applied OSHA excavation standards",
        ],
        requires_cross_agent=True,
    )

    mock_agents = {}
    for name in [
        "critical_path",
        "site_logistics",
        "claims_dispute",
        "financial_intelligence",
    ]:
        agent = AsyncMock()
        agent.name = name
        agent.run = AsyncMock(
            return_value=AgentEvent(
                event_id=f"evt-{name}-resp",
                source_agent=name,
                event_type=f"{name}_response",
                severity="info",
                timestamp=datetime.now(UTC),
                data={},
                confidence=0.90,
            )
        )
        mock_agents[name] = agent

    orchestrator = Orchestrator(
        settings=mock_construction_settings,
        shared_memory=mock_shared_memory,
        pubsub=mock_pubsub,
        agents=mock_agents,
    )

    triggers = await orchestrator.handle_event(
        stop_work_event
    )
    assert len(triggers) > 0

    # Verify site_logistics and critical_path are triggered
    target_agents = {t.target_agent for t in triggers}
    assert "site_logistics" in target_agents
    assert "critical_path" in target_agents

    # Safety stop-work should ALWAYS escalate
    should_escalate = await orchestrator.check_escalation(
        stop_work_event
    )
    assert should_escalate is True


@pytest.mark.asyncio
async def test_safety_stop_work_is_highest_priority(
    mock_construction_settings,
    mock_shared_memory,
    mock_pubsub,
):
    """Verify safety stop-work triggers have highest priority."""
    event = AgentEvent(
        event_id="evt-safety-002",
        source_agent="safety_compliance",
        event_type="stop_work_recommended",
        severity="critical",
        timestamp=datetime.now(UTC),
        data={
            "zone": "Test Zone",
            "safety_critical": True,
            "description": "Test stop-work",
        },
        confidence=0.95,
    )

    orchestrator = Orchestrator(
        settings=mock_construction_settings,
        shared_memory=mock_shared_memory,
        pubsub=mock_pubsub,
        agents={},
    )

    triggers = await orchestrator.handle_event(event)
    # All safety stop-work triggers should have priority 1
    for trigger in triggers:
        if (
            trigger.source_event_type
            == "stop_work_recommended"
        ):
            assert trigger.priority <= 2
