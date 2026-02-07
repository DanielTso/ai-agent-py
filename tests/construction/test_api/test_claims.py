"""Tests for claims and dispute management endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from construction.api.app import app


@pytest.mark.asyncio
async def test_get_timeline():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/claims/timeline"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["id"] == "CLM-001"


@pytest.mark.asyncio
async def test_get_notices():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/claims/notices"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "notice_type" in data[0]


@pytest.mark.asyncio
async def test_get_delay_analysis():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/claims/delay-analysis"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["method"] == "time_impact_analysis"
        assert data["total_delay_days"] == 45
        assert "delay_events" in data
