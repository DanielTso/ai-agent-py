"""Tests for approval workflow endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from construction.api.app import app


@pytest.mark.asyncio
async def test_list_approvals():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get("/api/approvals/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["status"] == "pending"


@pytest.mark.asyncio
async def test_get_approval():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/approvals/APR-001"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "APR-001"
        assert "impact" in data


@pytest.mark.asyncio
async def test_approve():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/approvals/APR-001/approve",
            json={"notes": "Looks good, proceed"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "approved"
        assert data["pm_notes"] == "Looks good, proceed"


@pytest.mark.asyncio
async def test_reject():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/approvals/APR-001/reject",
            json={"notes": "Too expensive"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "rejected"
        assert data["pm_notes"] == "Too expensive"
