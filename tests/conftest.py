"""Shared pytest fixtures."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from ai_agent.config import Settings


@pytest.fixture
def mock_settings():
    return Settings(
        anthropic_api_key="test-key",
        model="claude-sonnet-4-5-20250929",
        max_tokens=100,
    )


@pytest.fixture
def mock_construction_settings():
    settings = MagicMock()
    settings.anthropic_api_key = "test-key"
    settings.model = "claude-sonnet-4-5-20250929"
    settings.max_tokens = 8192
    settings.database_url = (
        "postgresql+asyncpg://test:test@localhost/test"
    )
    settings.redis_url = "redis://localhost:6379/0"
    settings.escalation_impact_threshold = 250000.0
    settings.pm_phone_number = "+15559999999"
    settings.dedup_ttl_seconds = 14400
    return settings


@pytest.fixture
def mock_shared_memory():
    mem = AsyncMock()
    mem.get_active_risks.return_value = []
    mem.get_vendor_alerts.return_value = []
    mem.get_pending_approvals.return_value = []
    mem.get_budget_status.return_value = {}
    mem.get_safety_readiness.return_value = 85.0
    mem.get_trir_current.return_value = 1.2
    mem.check_dedup.return_value = False
    return mem


@pytest.fixture
def mock_pubsub():
    ps = AsyncMock()
    ps.publish = AsyncMock()
    return ps
