"""Tests for ProcoreClient."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from construction.integrations.procore import ProcoreClient


@pytest.fixture
def client():
    c = ProcoreClient(
        client_id="test-id",
        client_secret="test-secret",
        rate_limit_per_second=0,
    )
    c._access_token = "test-token"
    c._token_expires_at = None  # skip refresh
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
    c = ProcoreClient(client_id="cid", client_secret="cs")
    assert c.client_id == "cid"
    assert c.client_secret == "cs"
    assert c.base_url == "https://api.procore.com/rest/v1.0"


async def test_get_projects(client):
    data = [{"id": 1, "name": "Project A"}]
    _mock_http(client, data)
    result = await client.get_projects()
    assert result == data


async def test_get_documents(client):
    data = [{"id": 10, "filename": "plans.pdf"}]
    _mock_http(client, data)
    result = await client.get_documents(1)
    assert result == data


async def test_get_rfis(client):
    data = [{"id": 100, "subject": "Clarification"}]
    _mock_http(client, data)
    result = await client.get_rfis(1)
    assert result == data


async def test_get_submittals(client):
    data = [{"id": 200, "title": "Steel samples"}]
    _mock_http(client, data)
    result = await client.get_submittals(1)
    assert result == data


async def test_create_rfi(client):
    data = {"id": 101, "subject": "New RFI"}
    _mock_http(client, data)
    result = await client.create_rfi(1, {"subject": "New RFI"})
    assert result == data


async def test_update_submittal(client):
    data = {"id": 200, "status": "approved"}
    _mock_http(client, data)
    result = await client.update_submittal(1, 200, {"status": "approved"})
    assert result == data


@patch("construction.integrations.procore.httpx.AsyncClient")
async def test_authenticate(mock_ac_cls):
    token_resp = MagicMock()
    token_resp.json.return_value = {
        "access_token": "abc",
        "refresh_token": "xyz",
        "expires_in": 7200,
    }
    token_resp.raise_for_status = MagicMock()

    mock_ac = AsyncMock()
    mock_ac.__aenter__ = AsyncMock(return_value=mock_ac)
    mock_ac.__aexit__ = AsyncMock(return_value=False)
    mock_ac.post = AsyncMock(return_value=token_resp)
    mock_ac_cls.return_value = mock_ac

    c = ProcoreClient(client_id="cid", client_secret="cs")
    result = await c.authenticate("auth-code")
    assert result["access_token"] == "abc"
    assert c._access_token == "abc"
    assert c._refresh_token == "xyz"


@patch("construction.integrations.base_client.asyncio.sleep", new_callable=AsyncMock)
async def test_error_handling_retry(mock_sleep, client):
    error_response = MagicMock(spec=httpx.Response)
    error_response.status_code = 503

    ok_response = MagicMock(spec=httpx.Response)
    ok_response.status_code = 200
    ok_response.json.return_value = []
    ok_response.raise_for_status = MagicMock()

    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.request = AsyncMock(
        side_effect=[
            httpx.HTTPStatusError(
                "503", request=MagicMock(), response=error_response
            ),
            ok_response,
        ]
    )
    client._client = mock_hc

    result = await client.get_projects()
    assert result == []
    assert mock_hc.request.await_count == 2
