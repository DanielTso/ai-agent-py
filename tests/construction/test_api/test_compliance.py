"""Tests for compliance checking endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from construction.api.app import app


@pytest.mark.asyncio
async def test_list_tickets():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/compliance/tickets"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["id"] == "DT-001"


@pytest.mark.asyncio
async def test_run_compliance_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/compliance/check"
        )
        assert response.status_code == 200
        data = response.json()
        assert "checks" in data
        assert data["total_open"] >= 0


@pytest.mark.asyncio
async def test_compliance_summary():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/compliance/summary"
        )
        assert response.status_code == 200
        data = response.json()
        assert "total_checks" in data
        assert data["total_checks"] == 42
