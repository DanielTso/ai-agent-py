"""Tests for ICCClient."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from construction.integrations.icc_api import ICCClient


@pytest.fixture
def client():
    """Create an ICCClient with rate limiting disabled."""
    return ICCClient(rate_limit_per_second=0)


def _mock_http(client, json_data):
    """Mock the HTTP client on an ICCClient instance."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = json_data
    mock_response.raise_for_status = MagicMock()

    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.request = AsyncMock(return_value=mock_response)
    client._client = mock_hc
    return mock_hc


async def test_init(client):
    """Client initializes with correct base URL."""
    assert client.base_url == "https://api.iccsafe.org/codes/v1"
    assert client.auth_headers == {}


async def test_search_codes(client):
    """Search codes returns results list."""
    data = [
        {"code": "IBC", "section": "903.2", "title": "Sprinklers"}
    ]
    _mock_http(client, data)
    result = await client.search_codes(
        code_type="IBC", keyword="sprinkler"
    )
    assert result == data


async def test_get_code_section(client):
    """Get code section returns section detail."""
    data = {
        "code": "IBC",
        "chapter": "3",
        "section": "302",
        "title": "Occupancy Classification",
    }
    _mock_http(client, data)
    result = await client.get_code_section(
        code="IBC", chapter="3", section="302"
    )
    assert result == data


async def test_get_occupancy_requirements(client):
    """Get occupancy requirements returns list."""
    data = [
        {
            "occupancy_type": "B",
            "description": "Business",
            "sprinkler_required": True,
        }
    ]
    _mock_http(client, data)
    result = await client.get_occupancy_requirements(
        occupancy_type="B"
    )
    assert result == data


async def test_get_structural_requirements(client):
    """Get structural requirements returns list."""
    data = [
        {
            "building_type": "data_center",
            "seismic_category": "D",
        }
    ]
    _mock_http(client, data)
    result = await client.get_structural_requirements(
        building_type="data_center"
    )
    assert result == data


async def test_error_handling(client):
    """HTTP errors propagate correctly."""
    error_response = MagicMock(spec=httpx.Response)
    error_response.status_code = 404

    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.request = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "404", request=MagicMock(), response=error_response
        )
    )
    client._client = mock_hc

    with pytest.raises(httpx.HTTPStatusError):
        await client.get_code_section(
            code="IBC", chapter="99", section="999"
        )
