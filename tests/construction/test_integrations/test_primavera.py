"""Tests for PrimaveraClient."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from construction.integrations.primavera import PrimaveraClient


@pytest.fixture
def client():
    c = PrimaveraClient(
        api_url="https://p6.example.com/api",
        api_key="test-key",
        rate_limit_per_second=0,
    )
    return c


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
    assert client.base_url == "https://p6.example.com/api"
    assert client.auth_headers == {"Authorization": "Bearer test-key"}


async def test_get_activities(client):
    data = [{"ObjectId": "1", "Name": "Foundation"}]
    _mock_http(client, data)
    result = await client.get_activities("proj1")
    assert result == data


async def test_get_relationships(client):
    data = [{"PredecessorActivityId": "1", "SuccessorActivityId": "2"}]
    _mock_http(client, data)
    result = await client.get_relationships("proj1")
    assert result == data


async def test_get_resources(client):
    data = [{"ResourceId": "r1", "Name": "Crane Operator"}]
    _mock_http(client, data)
    result = await client.get_resources("proj1")
    assert result == data


async def test_update_activity(client):
    data = {"ObjectId": "1", "Status": "Completed"}
    _mock_http(client, data)
    result = await client.update_activity("1", {"Status": "Completed"})
    assert result == data


async def test_get_critical_path(client):
    data = [{"ObjectId": "3", "IsCritical": True}]
    _mock_http(client, data)
    result = await client.get_critical_path("proj1")
    assert result == data


async def test_error_handling(client):
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
        await client.get_activities("bad-id")
