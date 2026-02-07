"""Tests for MSHAClient."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from construction.integrations.msha_api import MSHAClient


@pytest.fixture
def client():
    return MSHAClient(rate_limit_per_second=0)


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
    assert client.base_url == "https://api.dol.gov/v2/msha"
    assert client.auth_headers == {}


async def test_get_mine_data(client):
    data = {"mine_id": "4601234", "mine_name": "Test Mine"}
    _mock_http(client, data)
    result = await client.get_mine_data("4601234")
    assert result == data


async def test_search_violations(client):
    data = [{"violation_id": "v1", "section": "30 CFR 56.1000"}]
    _mock_http(client, data)
    result = await client.search_violations(mine_id="4601234")
    assert result == data


async def test_search_violations_with_keyword(client):
    data = [{"violation_id": "v2"}]
    mock_hc = _mock_http(client, data)
    await client.search_violations(keyword="ventilation")
    call_kwargs = mock_hc.request.call_args
    params = call_kwargs.kwargs.get("params", {})
    assert params["keyword"] == "ventilation"


async def test_get_inspections(client):
    data = [{"inspection_id": "i1", "mine_id": "4601234"}]
    _mock_http(client, data)
    result = await client.get_inspections("4601234")
    assert result == data


async def test_check_contractor(client):
    data = {"contractor_id": "c1", "status": "compliant"}
    _mock_http(client, data)
    result = await client.check_contractor("c1")
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
        await client.get_mine_data("bad-id")
