"""Tests for OSHAClient."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from construction.integrations.osha_api import OSHAClient


@pytest.fixture
def client():
    return OSHAClient(rate_limit_per_second=0)


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
    assert client.base_url == "https://enforcedata.dol.gov/api"
    assert client.auth_headers == {}


async def test_search_inspections(client):
    data = [{"activity_nr": "123456", "estab_name": "ACME"}]
    _mock_http(client, data)
    result = await client.search_inspections(establishment="ACME")
    assert result == data


async def test_search_inspections_with_filters(client):
    data = [{"activity_nr": "789"}]
    mock_hc = _mock_http(client, data)
    await client.search_inspections(
        establishment="Test", state="TX", sic="1542"
    )
    call_kwargs = mock_hc.request.call_args
    params = call_kwargs.kwargs.get("params", {})
    assert params["estab_name"] == "Test"
    assert params["site_state"] == "TX"
    assert params["sic_code"] == "1542"


async def test_get_citations(client):
    data = [{"citation_id": "c1", "standard": "1926.501"}]
    _mock_http(client, data)
    result = await client.get_citations("123456")
    assert result == data


async def test_get_300a_data(client):
    data = [{"year": 2025, "total_injuries": 5}]
    _mock_http(client, data)
    result = await client.get_300a_data("ACME", 2025)
    assert result == data


async def test_search_violations(client):
    data = [{"violation_id": "v1", "description": "Fall protection"}]
    _mock_http(client, data)
    result = await client.search_violations("fall")
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
        await client.get_citations("bad-id")
