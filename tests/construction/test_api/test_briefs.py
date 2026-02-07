"""Tests for daily briefing endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from construction.api.app import app


@pytest.mark.asyncio
async def test_get_latest_brief():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get("/api/briefs/daily")
        assert response.status_code == 200
        data = response.json()
        assert "top_threats" in data
        assert len(data["top_threats"]) == 3
        assert "quality_gaps" in data
        assert len(data["quality_gaps"]) == 2
        assert "acceleration" in data
        assert "full_text" in data


@pytest.mark.asyncio
async def test_get_brief_by_date():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/briefs/2025-02-03"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["brief_date"] == "2025-02-03"
        assert "top_threats" in data
