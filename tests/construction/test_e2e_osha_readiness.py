"""E2E test: OSHA inspection readiness check."""

from unittest.mock import MagicMock, patch

import pytest

from construction.agents.safety_compliance import (
    SafetyComplianceAgent,
)
from construction.schemas.common import AgentEvent


@pytest.mark.asyncio
async def test_osha_readiness_check(
    mock_construction_settings,
    mock_shared_memory,
    mock_pubsub,
):
    """Test that Safety Compliance agent can produce an event."""
    with patch(
        "construction.agents.base.Agent"
    ) as mock_agent_cls:
        mock_agent_inst = MagicMock()
        mock_agent_inst.chat.return_value = (
            '{"safety_metrics": {"trir": 1.2},'
            ' "focus_four_status": {},'
            ' "stop_work_recommendations": [],'
            ' "training_alerts": {"expired": []},'
            ' "exposure_monitoring": {"exceedances": []}}'
        )
        mock_agent_cls.return_value = mock_agent_inst

        agent = SafetyComplianceAgent(
            settings=mock_construction_settings,
            shared_memory=mock_shared_memory,
            pubsub=mock_pubsub,
        )

        result = await agent.run(
            {"project_id": "test", "action": "readiness_check"}
        )
        assert isinstance(result, AgentEvent)
        assert result.source_agent == "safety_compliance"
        assert result.event_type == "safety_status"
        assert result.severity == "info"
