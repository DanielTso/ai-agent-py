"""Tests for environmental monitoring endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from construction.api.app import app


@pytest.mark.asyncio
async def test_get_permits():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/environmental/permits"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["permit_type"] == "SWPPP"


@pytest.mark.asyncio
async def test_get_leed():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/environmental/leed"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["target_level"] == "Gold"
        assert "categories" in data


@pytest.mark.asyncio
async def test_get_carbon():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/environmental/carbon"
        )
        assert response.status_code == 200
        data = response.json()
        assert "total_embodied_co2_tons" in data
        assert "by_material" in data
