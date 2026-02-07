"""Tests for BaseAsyncClient: retry logic, rate limiting, error handling."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from construction.integrations.base_client import BaseAsyncClient


class ConcreteClient(BaseAsyncClient):
    """Concrete subclass for testing the abstract base."""

    pass


@pytest.fixture
def client():
    return ConcreteClient(
        base_url="https://api.example.com",
        auth_headers={"Authorization": "Bearer test"},
        max_retries=3,
        rate_limit_per_second=0,
        timeout=5.0,
    )


async def test_init(client):
    assert client.base_url == "https://api.example.com"
    assert client.auth_headers == {"Authorization": "Bearer test"}
    assert client.max_retries == 3
    assert client.timeout == 5.0


async def test_init_strips_trailing_slash():
    c = ConcreteClient(base_url="https://api.example.com/")
    assert c.base_url == "https://api.example.com"


async def test_get_client_creates_httpx_client(client):
    hc = await client._get_client()
    assert isinstance(hc, httpx.AsyncClient)
    await client.close()


async def test_successful_get(client):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"ok": True}
    mock_response.raise_for_status = MagicMock()

    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.request = AsyncMock(return_value=mock_response)
    client._client = mock_hc

    resp = await client.get("/test")
    assert resp.json() == {"ok": True}
    mock_hc.request.assert_awaited_once_with("GET", "/test")


async def test_successful_post(client):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 1}
    mock_response.raise_for_status = MagicMock()

    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.request = AsyncMock(return_value=mock_response)
    client._client = mock_hc

    resp = await client.post("/items", json={"name": "x"})
    assert resp.json() == {"id": 1}
    mock_hc.request.assert_awaited_once_with(
        "POST", "/items", json={"name": "x"}
    )


async def test_successful_put(client):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"updated": True}
    mock_response.raise_for_status = MagicMock()

    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.request = AsyncMock(return_value=mock_response)
    client._client = mock_hc

    resp = await client.put("/items/1", json={"name": "y"})
    assert resp.json() == {"updated": True}


@patch("construction.integrations.base_client.asyncio.sleep", new_callable=AsyncMock)
async def test_retry_on_500(mock_sleep, client):
    error_response = MagicMock(spec=httpx.Response)
    error_response.status_code = 500

    ok_response = MagicMock(spec=httpx.Response)
    ok_response.status_code = 200
    ok_response.json.return_value = {"ok": True}
    ok_response.raise_for_status = MagicMock()

    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.request = AsyncMock(
        side_effect=[
            httpx.HTTPStatusError(
                "500", request=MagicMock(), response=error_response
            ),
            ok_response,
        ]
    )
    client._client = mock_hc

    resp = await client.get("/flaky")
    assert resp.json() == {"ok": True}
    assert mock_hc.request.await_count == 2
    mock_sleep.assert_awaited_once_with(1)


@patch("construction.integrations.base_client.asyncio.sleep", new_callable=AsyncMock)
async def test_retry_on_429(mock_sleep, client):
    error_response = MagicMock(spec=httpx.Response)
    error_response.status_code = 429

    ok_response = MagicMock(spec=httpx.Response)
    ok_response.status_code = 200
    ok_response.json.return_value = {"ok": True}
    ok_response.raise_for_status = MagicMock()

    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.request = AsyncMock(
        side_effect=[
            httpx.HTTPStatusError(
                "429", request=MagicMock(), response=error_response
            ),
            ok_response,
        ]
    )
    client._client = mock_hc

    resp = await client.get("/rate-limited")
    assert resp.json() == {"ok": True}


@patch("construction.integrations.base_client.asyncio.sleep", new_callable=AsyncMock)
async def test_retry_on_request_error(mock_sleep, client):
    ok_response = MagicMock(spec=httpx.Response)
    ok_response.status_code = 200
    ok_response.json.return_value = {"ok": True}
    ok_response.raise_for_status = MagicMock()

    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.request = AsyncMock(
        side_effect=[
            httpx.ConnectError("connection refused"),
            ok_response,
        ]
    )
    client._client = mock_hc

    resp = await client.get("/down")
    assert resp.json() == {"ok": True}
    assert mock_hc.request.await_count == 2


@patch("construction.integrations.base_client.asyncio.sleep", new_callable=AsyncMock)
async def test_max_retries_exhausted(mock_sleep, client):
    error_response = MagicMock(spec=httpx.Response)
    error_response.status_code = 503

    exc = httpx.HTTPStatusError(
        "503", request=MagicMock(), response=error_response
    )

    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.request = AsyncMock(side_effect=exc)
    client._client = mock_hc

    with pytest.raises(httpx.HTTPStatusError):
        await client.get("/always-down")
    assert mock_hc.request.await_count == 3


async def test_non_retryable_error_raises_immediately(client):
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
        await client.get("/not-found")
    assert mock_hc.request.await_count == 1


async def test_close(client):
    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.aclose = AsyncMock()
    client._client = mock_hc

    await client.close()
    mock_hc.aclose.assert_awaited_once()


async def test_close_when_already_closed(client):
    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = True
    client._client = mock_hc

    await client.close()  # should not raise


async def test_close_when_no_client(client):
    await client.close()  # should not raise
