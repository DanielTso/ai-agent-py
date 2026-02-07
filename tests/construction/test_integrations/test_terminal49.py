"""Tests for Terminal49Client."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from construction.integrations.terminal49 import Terminal49Client


@pytest.fixture
def client():
    return Terminal49Client(
        api_key="test-key", rate_limit_per_second=0
    )


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
    assert client.base_url == "https://api.terminal49.com/v2"
    assert client.auth_headers == {"Authorization": "Token test-key"}


async def test_get_shipments(client):
    data = {"data": [{"id": "s1", "type": "shipment"}]}
    _mock_http(client, data)
    result = await client.get_shipments()
    assert result == [{"id": "s1", "type": "shipment"}]


async def test_get_shipment(client):
    data = {"data": {"id": "s1", "attributes": {"status": "in_transit"}}}
    _mock_http(client, data)
    result = await client.get_shipment("s1")
    assert result == {"id": "s1", "attributes": {"status": "in_transit"}}


async def test_get_milestones(client):
    data = {"data": [{"id": "m1", "type": "transport_event"}]}
    _mock_http(client, data)
    result = await client.get_milestones("s1")
    assert result == [{"id": "m1", "type": "transport_event"}]


async def test_create_tracking(client):
    data = {"data": {"id": "tr1", "type": "tracking_request"}}
    _mock_http(client, data)
    result = await client.create_tracking(
        {"shipping_line": "MAEU", "number": "MSKU123"}
    )
    assert result == {"id": "tr1", "type": "tracking_request"}


async def test_error_handling(client):
    error_response = MagicMock(spec=httpx.Response)
    error_response.status_code = 422

    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.request = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "422", request=MagicMock(), response=error_response
        )
    )
    client._client = mock_hc

    with pytest.raises(httpx.HTTPStatusError):
        await client.create_tracking({})
