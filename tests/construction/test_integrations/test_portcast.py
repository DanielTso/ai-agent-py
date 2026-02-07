"""Tests for PortcastClient."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from construction.integrations.portcast import PortcastClient


@pytest.fixture
def client():
    return PortcastClient(api_key="test-key", rate_limit_per_second=0)


def _mock_http(client, json_data):
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
    assert client.base_url == "https://api.portcast.io/api/v1"
    assert client.auth_headers == {"x-api-key": "test-key"}


async def test_track_container(client):
    data = {"container_id": "ABCD1234567", "status": "in_transit"}
    _mock_http(client, data)
    result = await client.track_container("ABCD1234567")
    assert result == data


async def test_get_port_congestion(client):
    data = {"port_code": "USLAX", "congestion_level": "high"}
    _mock_http(client, data)
    result = await client.get_port_congestion("USLAX")
    assert result == data


async def test_get_vessel_position(client):
    data = {"imo": "1234567", "lat": 33.7, "lon": -118.2}
    _mock_http(client, data)
    result = await client.get_vessel_position("1234567")
    assert result == data


async def test_error_handling(client):
    error_response = MagicMock(spec=httpx.Response)
    error_response.status_code = 401

    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.request = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "401", request=MagicMock(), response=error_response
        )
    )
    client._client = mock_hc

    with pytest.raises(httpx.HTTPStatusError):
        await client.track_container("XXXX")
