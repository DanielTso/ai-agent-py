"""Tests for schedule management endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from construction.api.app import app


@pytest.mark.asyncio
async def test_critical_path():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/schedule/critical-path"
        )
        assert response.status_code == 200
        data = response.json()
        assert "activities" in data
        assert data["total_duration_days"] == 120
        assert len(data["activities"]) >= 1


@pytest.mark.asyncio
async def test_simulate():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/schedule/simulate",
            json={
                "project_id": "test-project",
                "iterations": 1000,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["iterations"] == 1000
        assert "p50_completion" in data
        assert "p80_completion" in data
        assert "p95_completion" in data


@pytest.mark.asyncio
async def test_float_report():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/schedule/float-report"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "activity_id" in data[0]
        assert "status" in data[0]
