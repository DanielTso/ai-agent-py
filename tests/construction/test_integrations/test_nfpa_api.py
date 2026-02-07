"""Tests for NFPAClient."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from construction.integrations.nfpa_api import NFPAClient


@pytest.fixture
def client():
    return NFPAClient(rate_limit_per_second=0)


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
    """Client initializes with correct base URL."""
    assert client.base_url == "https://api.nfpa.org/codes/v1"
    assert client.auth_headers == {}


async def test_search_codes(client):
    """Search codes returns matching results."""
    data = [{"code": "NFPA 101", "title": "Life Safety Code"}]
    _mock_http(client, data)
    result = await client.search_codes(code_name="NFPA 101")
    assert result == data


async def test_search_codes_with_filters(client):
    """Search codes passes all filter parameters."""
    data = [{"code": "NFPA 70", "article": "250"}]
    mock_hc = _mock_http(client, data)
    await client.search_codes(
        code_name="NFPA 70", article="250", keyword="grounding"
    )
    call_kwargs = mock_hc.request.call_args
    params = call_kwargs.kwargs.get("params", {})
    assert params["code_name"] == "NFPA 70"
    assert params["article"] == "250"
    assert params["keyword"] == "grounding"


async def test_get_code_section(client):
    """Get code section returns section details."""
    data = {
        "code": "NFPA 101",
        "section": "7.3",
        "title": "Capacity of Means of Egress",
    }
    _mock_http(client, data)
    result = await client.get_code_section("NFPA 101", "7.3")
    assert result == data


async def test_get_nec_article(client):
    """Get NEC article returns article details."""
    data = {
        "article": "250",
        "title": "Grounding and Bonding",
        "code": "NFPA 70",
    }
    _mock_http(client, data)
    result = await client.get_nec_article("250")
    assert result == data


async def test_search_violations(client):
    """Search violations returns matching records."""
    data = [
        {
            "violation_id": "v1",
            "description": "Missing fire damper",
        }
    ]
    _mock_http(client, data)
    result = await client.search_violations("fire damper")
    assert result == data


async def test_error_handling(client):
    """HTTP errors propagate as expected."""
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
        await client.get_nec_article("999")
