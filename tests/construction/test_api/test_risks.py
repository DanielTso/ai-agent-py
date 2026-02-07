"""Tests for risk management endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from construction.api.app import app


@pytest.mark.asyncio
async def test_list_risks():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get("/api/risks/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["id"] == "RISK-001"
        assert "risk_score" in data[0]


@pytest.mark.asyncio
async def test_create_risk():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/risks/",
            json={
                "project_id": "test-project",
                "timeframe_days": 14,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "RISK-001"


@pytest.mark.asyncio
async def test_get_heatmap():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get("/api/risks/heatmap")
        assert response.status_code == 200
        data = response.json()
        assert "cells" in data
        assert len(data["cells"]) >= 1


@pytest.mark.asyncio
async def test_assess_risks():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/risks/assess",
            json={
                "project_id": "test-project",
                "timeframe_days": 7,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "risks" in data
        assert "heatmap" in data
        assert "generated_at" in data
