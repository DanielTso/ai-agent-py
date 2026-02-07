"""Tests for AutodeskClient."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from construction.integrations.autodesk import AutodeskClient


@pytest.fixture
def client():
    c = AutodeskClient(
        client_id="test-id",
        client_secret="test-secret",
        rate_limit_per_second=0,
    )
    c._access_token = "test-token"
    c._token_expires_at = None
    return c


def _mock_http(client, json_data, status=200):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = status
    mock_response.json.return_value = json_data
    mock_response.raise_for_status = MagicMock()

    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.request = AsyncMock(return_value=mock_response)
    client._client = mock_hc
    return mock_hc


async def test_init():
    c = AutodeskClient(client_id="cid", client_secret="cs")
    assert c.client_id == "cid"
    assert c.base_url == "https://developer.api.autodesk.com"


async def test_get_hubs(client):
    _mock_http(client, {"data": [{"id": "h1", "type": "hubs"}]})
    result = await client.get_hubs()
    assert result == [{"id": "h1", "type": "hubs"}]


async def test_get_projects(client):
    _mock_http(client, {"data": [{"id": "p1", "name": "Proj"}]})
    result = await client.get_projects("h1")
    assert result == [{"id": "p1", "name": "Proj"}]


async def test_get_documents(client):
    _mock_http(client, {"data": [{"id": "d1", "type": "items"}]})
    result = await client.get_documents("p1")
    assert result == [{"id": "d1", "type": "items"}]


async def test_get_issues(client):
    _mock_http(client, {"results": [{"id": "i1", "title": "Issue"}]})
    result = await client.get_issues("p1")
    assert result == [{"id": "i1", "title": "Issue"}]


async def test_get_model_derivative(client):
    data = {"urn": "abc", "status": "success"}
    _mock_http(client, data)
    result = await client.get_model_derivative("abc")
    assert result == data


async def test_create_issue(client):
    data = {"id": "i2", "title": "New Issue"}
    _mock_http(client, data)
    result = await client.create_issue("p1", {"title": "New Issue"})
    assert result == data


@patch("construction.integrations.autodesk.httpx.AsyncClient")
async def test_authenticate_2legged(mock_ac_cls):
    token_resp = MagicMock()
    token_resp.json.return_value = {
        "access_token": "tok",
        "expires_in": 3600,
    }
    token_resp.raise_for_status = MagicMock()

    mock_ac = AsyncMock()
    mock_ac.__aenter__ = AsyncMock(return_value=mock_ac)
    mock_ac.__aexit__ = AsyncMock(return_value=False)
    mock_ac.post = AsyncMock(return_value=token_resp)
    mock_ac_cls.return_value = mock_ac

    c = AutodeskClient(client_id="cid", client_secret="cs")
    result = await c.authenticate_2legged()
    assert result["access_token"] == "tok"
    assert c._access_token == "tok"


@patch("construction.integrations.base_client.asyncio.sleep", new_callable=AsyncMock)
async def test_error_handling_retry(mock_sleep, client):
    error_response = MagicMock(spec=httpx.Response)
    error_response.status_code = 502

    ok_response = MagicMock(spec=httpx.Response)
    ok_response.status_code = 200
    ok_response.json.return_value = {"data": []}
    ok_response.raise_for_status = MagicMock()

    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.request = AsyncMock(
        side_effect=[
            httpx.HTTPStatusError(
                "502", request=MagicMock(), response=error_response
            ),
            ok_response,
        ]
    )
    client._client = mock_hc

    result = await client.get_hubs()
    assert result == []
    assert mock_hc.request.await_count == 2
