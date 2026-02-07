"""Tests for workforce management endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from construction.api.app import app


@pytest.mark.asyncio
async def test_get_crews():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/workforce/crews"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["trade"] == "Ironworkers"


@pytest.mark.asyncio
async def test_get_productivity():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/workforce/productivity"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "productivity_index" in data[0]


@pytest.mark.asyncio
async def test_get_certs():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/workforce/certs"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "cert_type" in data[0]


@pytest.mark.asyncio
async def test_get_forecast():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/workforce/forecast"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "gap" in data[0]
