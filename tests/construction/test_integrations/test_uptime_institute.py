"""Tests for UptimeInstituteClient."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from construction.integrations.uptime_institute import (
    UptimeInstituteClient,
)


@pytest.fixture
def client():
    return UptimeInstituteClient(rate_limit_per_second=0)


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
    """Client initializes with default base URL."""
    assert client.base_url == ("https://api.uptimeinstitute.com/v1")
    assert client.auth_headers == {}


async def test_init_with_api_key():
    """Client sets auth header when API key provided."""
    client = UptimeInstituteClient(api_key="test-key", rate_limit_per_second=0)
    assert client.auth_headers == {"Authorization": "Bearer test-key"}


async def test_get_tier_requirements(client):
    """Get tier requirements returns expected data."""
    data = {
        "tier": "III",
        "requirements": {"uptime": "99.982%"},
    }
    _mock_http(client, data)
    result = await client.get_tier_requirements("III")
    assert result == data


async def test_check_tier_compliance(client):
    """Check tier compliance returns compliance data."""
    data = {
        "project_id": "DC-001",
        "compliant": True,
    }
    mock_hc = _mock_http(client, data)
    result = await client.check_tier_compliance("DC-001", "III")
    assert result == data
    call_kwargs = mock_hc.request.call_args
    params = call_kwargs.kwargs.get("params", {})
    assert params["tier"] == "III"


async def test_get_design_documents(client):
    """Get design documents returns project docs."""
    data = {
        "project_id": "DC-001",
        "documents": [{"name": "SLD-001"}],
    }
    _mock_http(client, data)
    result = await client.get_design_documents("DC-001")
    assert result == data


async def test_get_certification_status(client):
    """Get certification status returns status data."""
    data = {
        "project_id": "DC-001",
        "status": "in_progress",
    }
    _mock_http(client, data)
    result = await client.get_certification_status("DC-001")
    assert result == data


async def test_error_handling(client):
    """HTTP errors are raised to the caller."""
    error_response = MagicMock(spec=httpx.Response)
    error_response.status_code = 404

    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.request = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "404",
            request=MagicMock(),
            response=error_response,
        )
    )
    client._client = mock_hc

    with pytest.raises(httpx.HTTPStatusError):
        await client.get_tier_requirements("III")
