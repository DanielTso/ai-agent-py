"""Tests for EPAClient."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from construction.integrations.epa_api import EPAClient


@pytest.fixture
def client():
    """Create an EPAClient with rate limiting disabled."""
    return EPAClient(rate_limit_per_second=0)


def _mock_http(client, json_data):
    """Replace the internal httpx client with a mock."""
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
    assert client.base_url == "https://api.epa.gov/echo/v1"
    assert client.auth_headers == {}


async def test_search_facilities(client):
    """Search facilities returns results."""
    data = [
        {
            "facility_id": "110070604174",
            "facility_name": "ACME Construction",
        }
    ]
    _mock_http(client, data)
    result = await client.search_facilities(name="ACME")
    assert result == data


async def test_search_facilities_with_filters(client):
    """Search facilities passes all filter params."""
    data = [{"facility_id": "999"}]
    mock_hc = _mock_http(client, data)
    await client.search_facilities(
        name="Test", state="TX", zip_code="78701"
    )
    call_kwargs = mock_hc.request.call_args
    params = call_kwargs.kwargs.get("params", {})
    assert params["facility_name"] == "Test"
    assert params["state_code"] == "TX"
    assert params["zip_code"] == "78701"


async def test_get_compliance_history(client):
    """Get compliance history returns data."""
    data = {
        "facility_id": "110070604174",
        "quarters_in_violation": 2,
    }
    _mock_http(client, data)
    result = await client.get_compliance_history(
        "110070604174"
    )
    assert result == data


async def test_get_violations(client):
    """Get violations returns list of violations."""
    data = [
        {
            "violation_id": "v1",
            "program": "CWA",
            "description": "Effluent limit exceedance",
        }
    ]
    _mock_http(client, data)
    result = await client.get_violations("110070604174")
    assert result == data


async def test_get_npdes_permits(client):
    """Get NPDES permits returns permit list."""
    data = [
        {
            "permit_id": "TX0045123",
            "status": "active",
        }
    ]
    _mock_http(client, data)
    result = await client.get_npdes_permits("110070604174")
    assert result == data


async def test_get_air_quality(client):
    """Get air quality returns data for zip code."""
    data = {"aqi": 55, "parameter": "PM2.5"}
    _mock_http(client, data)
    result = await client.get_air_quality("78701")
    assert result == data


async def test_get_air_quality_with_parameter(client):
    """Get air quality passes parameter filter."""
    data = {"aqi": 42, "parameter": "PM10"}
    mock_hc = _mock_http(client, data)
    await client.get_air_quality("78701", parameter="PM10")
    call_kwargs = mock_hc.request.call_args
    params = call_kwargs.kwargs.get("params", {})
    assert params["zip_code"] == "78701"
    assert params["parameter"] == "PM10"


async def test_error_handling(client):
    """HTTP errors propagate as exceptions."""
    error_response = MagicMock(spec=httpx.Response)
    error_response.status_code = 404

    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.request = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "404",
            request=MagicMock(),
            response=error_response,
        )
    )
    client._client = mock_hc

    with pytest.raises(httpx.HTTPStatusError):
        await client.get_violations("bad-id")
