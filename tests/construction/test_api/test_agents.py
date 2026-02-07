"""Tests for agent management endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from construction.api.app import app


@pytest.mark.asyncio
async def test_get_agent_statuses():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/agents/status"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 13
        names = [a["name"] for a in data]
        assert "risk_forecaster" in names
        assert "supply_chain" in names


@pytest.mark.asyncio
async def test_trigger_agent_run():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/agents/risk_forecaster/run"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["agent_name"] == "risk_forecaster"
        assert data["status"] == "started"


@pytest.mark.asyncio
async def test_get_agent_history():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/agents/risk_forecaster/history"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["status"] == "completed"
