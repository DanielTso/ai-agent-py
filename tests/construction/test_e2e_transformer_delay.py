"""E2E test: Transformer delayed 14 days -- full agent cascade."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from construction.agents.orchestrator import Orchestrator
from construction.schemas.common import AgentEvent, DataSource


@pytest.mark.asyncio
async def test_transformer_delay_cascade(
    mock_construction_settings,
    mock_shared_memory,
    mock_pubsub,
):
    """
    Simulate: Supply Chain detects transformer T-2MVA-01
    delayed 14 days.
    Expected cascade:
    1. Critical Path runs reoptimize
    2. Orchestrator escalates (>$250k) via SMS
    """
    delay_event = AgentEvent(
        event_id="evt-transformer-001",
        source_agent="supply_chain",
        event_type="critical_delay",
        severity="critical",
        timestamp=datetime.now(UTC),
        data={
            "vendor": "ABB Power Grids",
            "material": "Transformer T-2MVA-01",
            "delay_days": 14,
            "reason": (
                "Vessel MV Pacific Star stuck at Port Kelang"
            ),
            "impact_dollars": 7000000.0,
            "description": "14-day transformer delay",
            "alternatives": [
                {
                    "vendor": "Schneider Electric",
                    "cost_delta": 45000,
                    "schedule_delta": -12,
                },
                {
                    "vendor": "Eaton",
                    "cost_delta": 12000,
                    "schedule_delta": 0,
                },
                {
                    "vendor": "ABB reroute",
                    "cost_delta": 8500,
                    "schedule_delta": -4,
                },
            ],
        },
        confidence=0.91,
        data_sources=[
            DataSource(
                source_type="api",
                source_name="portcast_api",
                retrieved_at=datetime.now(UTC),
                confidence=0.95,
            ),
        ],
        transparency_log=[
            "Checked vessel AIS position",
            "Confirmed port congestion at Kelang",
            "Verified customs status",
            "Contacted ABB logistics desk",
        ],
        requires_cross_agent=True,
    )

    mock_agents = {}
    for agent_name in [
        "critical_path",
        "financial_intelligence",
        "claims_dispute",
        "safety_compliance",
        "stakeholder_communication",
        "commissioning_turnover",
    ]:
        mock_agent = AsyncMock()
        mock_agent.name = agent_name
        mock_agent.run = AsyncMock(
            return_value=AgentEvent(
                event_id=f"evt-{agent_name}-001",
                source_agent=agent_name,
                event_type=f"{agent_name}_response",
                severity="info",
                timestamp=datetime.now(UTC),
                data={"status": "processed"},
                confidence=0.85,
            )
        )
        mock_agents[agent_name] = mock_agent

    orchestrator = Orchestrator(
        settings=mock_construction_settings,
        shared_memory=mock_shared_memory,
        pubsub=mock_pubsub,
        agents=mock_agents,
    )

    # Process the event
    triggers = await orchestrator.handle_event(delay_event)

    # Verify cross-agent triggers were created
    assert len(triggers) > 0
    # critical_path should be triggered for reoptimize
    target_agents = [t.target_agent for t in triggers]
    assert "critical_path" in target_agents

    # Verify escalation check (>$250k)
    should_escalate = await orchestrator.check_escalation(
        delay_event
    )
    assert should_escalate is True  # $7M > $250k threshold


@pytest.mark.asyncio
async def test_dedup_prevents_duplicate_alerts(
    mock_construction_settings,
    mock_shared_memory,
    mock_pubsub,
):
    """Test that duplicate alerts within 4h TTL are suppressed."""
    mock_shared_memory.check_dedup.return_value = True

    event = AgentEvent(
        event_id="evt-dup-001",
        source_agent="supply_chain",
        event_type="critical_delay",
        severity="critical",
        timestamp=datetime.now(UTC),
        data={"impact_dollars": 500000},
        confidence=0.90,
    )

    orchestrator = Orchestrator(
        settings=mock_construction_settings,
        shared_memory=mock_shared_memory,
        pubsub=mock_pubsub,
        agents={},
    )

    is_dup = await orchestrator.check_dedup(event)
    assert is_dup is True
