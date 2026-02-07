"""Tests for financial management endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from construction.api.app import app


@pytest.mark.asyncio
async def test_get_evm():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get("/api/financial/evm")
        assert response.status_code == 200
        data = response.json()
        assert "cpi" in data
        assert "spi" in data
        assert data["cpi"] == 0.94


@pytest.mark.asyncio
async def test_get_cashflow():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/financial/cashflow"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "period" in data[0]


@pytest.mark.asyncio
async def test_get_budget():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/financial/budget"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_budget"] == 20000000
        assert "variance_pct" in data


@pytest.mark.asyncio
async def test_list_change_orders():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/financial/change-orders"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["co_number"] == "CO-2025-001"
