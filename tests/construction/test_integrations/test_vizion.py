"""Tests for VizionClient."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from construction.integrations.vizion import VizionClient


@pytest.fixture
def client():
    return VizionClient(api_key="test-key", rate_limit_per_second=0)


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
    assert client.base_url == "https://api.vizionapi.com/api/v2"
    assert client.auth_headers == {"X-API-Key": "test-key"}


async def test_get_container(client):
    data = {"container_id": "CONT123", "status": "delivered"}
    _mock_http(client, data)
    result = await client.get_container("CONT123")
    assert result == data


async def test_get_eta(client):
    data = {"container_id": "CONT123", "eta": "2026-03-15T10:00:00Z"}
    _mock_http(client, data)
    result = await client.get_eta("CONT123")
    assert result == data


async def test_list_containers(client):
    data = [{"container_id": "C1"}, {"container_id": "C2"}]
    _mock_http(client, data)
    result = await client.list_containers()
    assert result == data


async def test_error_handling(client):
    error_response = MagicMock(spec=httpx.Response)
    error_response.status_code = 403

    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.request = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "403", request=MagicMock(), response=error_response
        )
    )
    client._client = mock_hc

    with pytest.raises(httpx.HTTPStatusError):
        await client.get_container("BAD")
