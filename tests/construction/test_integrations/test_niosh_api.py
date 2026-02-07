"""Tests for NIOSHClient."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from construction.integrations.niosh_api import NIOSHClient


@pytest.fixture
def client():
    return NIOSHClient(rate_limit_per_second=0)


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
    assert client.base_url == "https://www.cdc.gov/niosh/api"
    assert client.auth_headers == {}


async def test_search_publications(client):
    data = [{"title": "Silica Dust Exposure", "pub_id": "p1"}]
    _mock_http(client, data)
    result = await client.search_publications("silica")
    assert result == data


async def test_get_face_reports(client):
    data = [{"report_id": "f1", "industry": "construction"}]
    _mock_http(client, data)
    result = await client.get_face_reports(industry="construction")
    assert result == data


async def test_get_face_reports_with_state(client):
    data = [{"report_id": "f2", "state": "OH"}]
    mock_hc = _mock_http(client, data)
    await client.get_face_reports(state="OH")
    call_kwargs = mock_hc.request.call_args
    params = call_kwargs.kwargs.get("params", {})
    assert params["state"] == "OH"


async def test_get_rel(client):
    data = {"substance": "silica", "rel_mg_m3": 0.05}
    _mock_http(client, data)
    result = await client.get_rel("silica")
    assert result == data


async def test_get_health_topics(client):
    data = [{"topic": "Hearing Loss"}, {"topic": "Heat Stress"}]
    _mock_http(client, data)
    result = await client.get_health_topics()
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
        await client.search_publications("nonexistent")
