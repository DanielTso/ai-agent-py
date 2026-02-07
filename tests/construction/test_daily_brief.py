"""Tests for daily brief generation."""

from datetime import date

import pytest

from construction.agents.orchestrator import Orchestrator
from construction.schemas.orchestrator import DailyBriefOutput


@pytest.mark.asyncio
async def test_daily_brief_generation(
    mock_construction_settings, mock_shared_memory, mock_pubsub
):
    """Test that orchestrator generates a valid daily brief."""
    orchestrator = Orchestrator(
        settings=mock_construction_settings,
        shared_memory=mock_shared_memory,
        pubsub=mock_pubsub,
        agents={},
    )
    brief = await orchestrator.generate_daily_brief(
        "test-project"
    )
    assert isinstance(brief, DailyBriefOutput)
    assert brief.brief_date == date.today()
    assert len(brief.top_threats) <= 3
    assert len(brief.quality_gaps) <= 2


@pytest.mark.asyncio
async def test_daily_brief_includes_threats(
    mock_construction_settings,
    mock_shared_memory,
    mock_pubsub,
):
    """Test that daily brief includes risk data from shared memory."""
    mock_shared_memory.get_active_risks.return_value = [
        ("risk-1", 750000.0),
        ("risk-2", 500000.0),
        ("risk-3", 250000.0),
    ]
    orchestrator = Orchestrator(
        settings=mock_construction_settings,
        shared_memory=mock_shared_memory,
        pubsub=mock_pubsub,
        agents={},
    )
    brief = await orchestrator.generate_daily_brief(
        "test-project"
    )
    assert brief.top_threats is not None
    # Threats should reflect the risk data we provided
    assert brief.top_threats[0].rank == 1


@pytest.mark.asyncio
async def test_daily_brief_full_text_not_empty(
    mock_construction_settings,
    mock_shared_memory,
    mock_pubsub,
):
    """Test that daily brief has non-empty full text."""
    orchestrator = Orchestrator(
        settings=mock_construction_settings,
        shared_memory=mock_shared_memory,
        pubsub=mock_pubsub,
        agents={},
    )
    brief = await orchestrator.generate_daily_brief(
        "test-project"
    )
    assert len(brief.full_text) > 0
    assert "Daily Brief" in brief.full_text
