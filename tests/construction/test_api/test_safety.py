"""Tests for safety management endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from construction.api.app import app


@pytest.mark.asyncio
async def test_get_safety_metrics():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/safety/metrics"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["trir"] == 1.8
        assert "dart" in data
        assert "emr" in data


@pytest.mark.asyncio
async def test_get_osha300():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/safety/osha300"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "case_number" in data[0]


@pytest.mark.asyncio
async def test_get_inspections():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/safety/inspections"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "items" in data[0]


@pytest.mark.asyncio
async def test_get_readiness_score():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/safety/readiness-score"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["overall_score"] == 87
        assert "categories" in data


@pytest.mark.asyncio
async def test_get_contractor_profiles():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/safety/contractors"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "emr" in data[0]


@pytest.mark.asyncio
async def test_get_exposure_data():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/safety/exposure"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "hazard" in data[0]
