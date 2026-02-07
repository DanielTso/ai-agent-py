"""Tests for the DocumentIntelligenceAgent."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from construction.agents.document_intelligence import (
    DocumentIntelligenceAgent,
)


@pytest.fixture
def mock_settings():
    settings = MagicMock()
    settings.anthropic_api_key = "test-key"
    settings.model = "claude-sonnet-4-5-20250929"
    settings.max_tokens = 100
    return settings


@pytest.fixture
def agent(mock_settings):
    with patch("construction.agents.base.Agent"):
        with patch(
            "construction.agents.base.get_construction_settings",
            return_value=mock_settings,
        ):
            return DocumentIntelligenceAgent(
                settings=mock_settings,
            )


def test_agent_initialization(agent):
    assert agent.name == "document_intelligence"
    assert agent.schedule == "on_demand"


def test_agent_system_prompt(agent):
    prompt = agent.get_system_prompt()
    assert "Document Intelligence" in prompt
    assert "N+1" in prompt
    assert "2N" in prompt
    assert "contradiction" in prompt.lower()
    assert "audit" in prompt.lower()


def test_agent_has_document_search_tool(agent):
    tool = agent._tools.get("document_search")
    assert tool is not None
    assert tool.name == "document_search"


@pytest.mark.asyncio
async def test_agent_run_search(agent):
    agent.pubsub = None
    agent.shared_memory = None

    event = await agent.run(
        context={
            "action": "search",
            "project_id": "proj-001",
            "query": "electrical specs",
        }
    )

    assert event.source_agent == "document_intelligence"
    assert event.event_type == "search_completed"
    assert event.severity == "info"
    assert event.data["action"] == "search"
    assert event.data["query"] == "electrical specs"


@pytest.mark.asyncio
async def test_agent_run_contradiction_detection(agent):
    agent.pubsub = None
    agent.shared_memory = None

    event = await agent.run(
        context={
            "action": "detect_contradictions",
            "project_id": "proj-001",
            "query": "voltage",
        }
    )

    assert event.source_agent == "document_intelligence"
    assert event.event_type == "contradiction_detected"
    assert event.severity == "warning"
    assert event.requires_cross_agent is True
    assert event.target_agent == "compliance"


@pytest.mark.asyncio
async def test_agent_run_default_context(agent):
    agent.pubsub = None
    agent.shared_memory = None

    event = await agent.run()

    assert event.source_agent == "document_intelligence"
    assert event.event_type == "search_completed"


@pytest.mark.asyncio
async def test_agent_run_with_pubsub(agent):
    mock_pubsub = AsyncMock()
    agent.pubsub = mock_pubsub
    agent.shared_memory = AsyncMock()

    event = await agent.run(
        context={
            "action": "search",
            "project_id": "proj-001",
            "query": "test",
        }
    )

    assert event.source_agent == "document_intelligence"
    mock_pubsub.publish.assert_called()
