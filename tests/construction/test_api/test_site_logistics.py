"""Tests for site logistics management endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from construction.api.app import app


@pytest.mark.asyncio
async def test_get_crane_schedule():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/site-logistics/crane"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "time_slots" in data[0]


@pytest.mark.asyncio
async def test_get_staging_zones():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/site-logistics/staging"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "capacity_pct" in data[0]


@pytest.mark.asyncio
async def test_get_headcount():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/site-logistics/headcount"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 156
        assert "by_trade" in data
