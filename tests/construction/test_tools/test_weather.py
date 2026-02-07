"""Tests for the weather forecast tool."""

import json
from unittest.mock import MagicMock, patch

from construction.tools.weather import WeatherForecast


def test_schema():
    """Tool schema has required fields."""
    tool = WeatherForecast()
    assert tool.name == "weather_forecast"
    schema = tool.get_input_schema()
    assert "latitude" in schema["properties"]
    assert "longitude" in schema["properties"]
    assert "days" in schema["properties"]
    assert "latitude" in schema["required"]
    assert "longitude" in schema["required"]


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = WeatherForecast()
    fmt = tool.to_api_format()
    assert fmt["name"] == "weather_forecast"
    assert "description" in fmt
    assert "input_schema" in fmt


@patch("construction.tools.weather.get_construction_settings")
def test_execute_mock_forecast(mock_settings):
    """Execute returns mock forecast when no API key is set."""
    mock_settings.return_value = MagicMock(openweathermap_api_key="")
    tool = WeatherForecast()
    result = tool.execute(latitude=29.76, longitude=-95.37, days=7)
    data = json.loads(result)
    assert "forecast" in data
    assert len(data["forecast"]) == 7
    assert "note" in data
    assert "Mock" in data["note"]
    # Check forecast day structure
    day = data["forecast"][0]
    assert "temp_high_f" in day
    assert "temp_low_f" in day
    assert "precipitation_probability" in day
    assert "wind_speed_mph" in day
    assert "description" in day


@patch("construction.tools.weather.get_construction_settings")
def test_execute_default_14_days(mock_settings):
    """Execute defaults to 14 days when days not specified."""
    mock_settings.return_value = MagicMock(openweathermap_api_key="")
    tool = WeatherForecast()
    result = tool.execute(latitude=29.76, longitude=-95.37)
    data = json.loads(result)
    assert len(data["forecast"]) == 14
    # Wind advisory alert appears for >= 7 days
    assert len(data["alerts"]) >= 1


@patch("construction.tools.weather.get_construction_settings")
def test_execute_caps_at_14_days(mock_settings):
    """Days parameter is capped at 14."""
    mock_settings.return_value = MagicMock(openweathermap_api_key="")
    tool = WeatherForecast()
    result = tool.execute(latitude=29.76, longitude=-95.37, days=30)
    data = json.loads(result)
    assert len(data["forecast"]) == 14


@patch("construction.tools.weather.get_construction_settings")
@patch("construction.tools.weather.httpx")
def test_execute_live_api(mock_httpx_mod, mock_settings):
    """Execute calls OpenWeatherMap when API key is configured."""
    mock_settings.return_value = MagicMock(
        openweathermap_api_key="test-key-123"
    )
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "daily": [
            {
                "dt": 1700000000,
                "temp": {"max": 80, "min": 60},
                "pop": 0.2,
                "rain": 5.0,
                "wind_speed": 12,
                "wind_gust": 25,
                "weather": [{"description": "scattered clouds"}],
            }
        ],
        "alerts": [],
    }
    mock_resp.raise_for_status = MagicMock()
    mock_httpx_mod.get.return_value = mock_resp

    tool = WeatherForecast()
    result = tool.execute(latitude=29.76, longitude=-95.37, days=1)
    data = json.loads(result)

    assert len(data["forecast"]) == 1
    assert data["forecast"][0]["temp_high_f"] == 80
    mock_httpx_mod.get.assert_called_once()


@patch("construction.tools.weather.get_construction_settings")
def test_execute_live_api_error(mock_settings):
    """Execute returns error string on API failure."""
    mock_settings.return_value = MagicMock(
        openweathermap_api_key="test-key-123"
    )

    with patch(
        "construction.tools.weather.httpx"
    ) as mock_httpx:
        mock_httpx.get.side_effect = Exception("Connection timeout")
        tool = WeatherForecast()
        result = tool.execute(
            latitude=29.76, longitude=-95.37
        )
        assert "Error" in result
        assert "Connection timeout" in result
