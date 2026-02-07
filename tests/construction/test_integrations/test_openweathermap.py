"""Tests for OpenWeatherMapClient."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from construction.integrations.openweathermap import OpenWeatherMapClient


@pytest.fixture
def client():
    return OpenWeatherMapClient(
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
    assert client.api_key == "test-key"
    assert client.base_url == "https://api.openweathermap.org"


async def test_get_current(client):
    data = {"temp": 22.5, "weather": [{"main": "Clear"}]}
    _mock_http(client, data)
    result = await client.get_current(40.7, -74.0)
    assert result == data


async def test_get_forecast(client):
    data = {"list": [{"dt": 1234567890, "main": {"temp": 20}}]}
    _mock_http(client, data)
    result = await client.get_forecast(40.7, -74.0, days=5)
    assert result == data


async def test_get_alerts(client):
    data = {"alerts": [{"event": "Wind Advisory"}]}
    _mock_http(client, data)
    result = await client.get_alerts(40.7, -74.0)
    assert result == data


async def test_params_include_api_key(client):
    params = client._params(lat=1.0, lon=2.0)
    assert params["appid"] == "test-key"
    assert params["units"] == "metric"
    assert params["lat"] == 1.0


async def test_error_handling(client):
    error_response = MagicMock(spec=httpx.Response)
    error_response.status_code = 401

    mock_hc = AsyncMock(spec=httpx.AsyncClient)
    mock_hc.is_closed = False
    mock_hc.request = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "401", request=MagicMock(), response=error_response
        )
    )
    client._client = mock_hc

    with pytest.raises(httpx.HTTPStatusError):
        await client.get_current(0, 0)
