"""E2E test: Document contradiction detected -> RFI flow."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from construction.agents.orchestrator import Orchestrator
from construction.schemas.common import AgentEvent, DataSource


@pytest.mark.asyncio
async def test_contradiction_to_rfi_flow(
    mock_construction_settings,
    mock_shared_memory,
    mock_pubsub,
):
    """
    Simulate: Document Intelligence detects voltage mismatch
    between drawing and spec.
    Expected cascade:
    1. Compliance runs focused check on affected elements
    """
    contradiction_event = AgentEvent(
        event_id="evt-doc-001",
        source_agent="document_intelligence",
        event_type="contradiction_detected",
        severity="warning",
        timestamp=datetime.now(UTC),
        data={
            "doc_a": {
                "title": "Electrical One-Line Drawing E-101",
                "doc_type": "drawing",
            },
            "doc_b": {
                "title": "Specification Section 26 20 00",
                "doc_type": "spec",
            },
            "contradiction": (
                "Voltage mismatch: Drawing shows 480V,"
                " Spec calls for 277V on Panel LP-3A"
            ),
            "severity": "high",
            "affected_elements": ["LP-3A", "feeder-42"],
        },
        confidence=0.88,
        data_sources=[
            DataSource(
                source_type="document",
                source_name="procore",
                retrieved_at=datetime.now(UTC),
                confidence=0.95,
            ),
        ],
        transparency_log=[
            "Parsed electrical one-line drawing E-101 rev 3",
            "Cross-referenced with Spec Section 26 20 00",
            "Identified voltage discrepancy on Panel LP-3A",
            (
                "Checked previous RFIs for resolution"
                " -- none found"
            ),
        ],
        requires_cross_agent=True,
    )

    mock_agents = {}
    for name in [
        "compliance",
        "stakeholder_communication",
        "claims_dispute",
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
                confidence=0.85,
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
        contradiction_event
    )
    assert len(triggers) > 0

    # Verify compliance is triggered for focused_check
    target_agents = [t.target_agent for t in triggers]
    assert "compliance" in target_agents
