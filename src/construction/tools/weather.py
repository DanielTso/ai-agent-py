"""Weather forecast tool using OpenWeatherMap API."""

import json
from datetime import UTC, datetime, timedelta

import httpx

from ai_agent.tools import Tool
from construction.config import get_construction_settings


class WeatherForecast(Tool):
    """Get weather forecast for a construction site location."""

    name = "weather_forecast"
    description = (
        "Get 14-day weather forecast for a location."
        " Returns temperature, precipitation, wind speed,"
        " and severe weather alerts."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "latitude": {
                    "type": "number",
                    "description": "Latitude of the location",
                },
                "longitude": {
                    "type": "number",
                    "description": "Longitude of the location",
                },
                "days": {
                    "type": "integer",
                    "description": "Number of forecast days (max 14)",
                    "default": 14,
                },
            },
            "required": ["latitude", "longitude"],
        }

    def execute(self, **kwargs) -> str:
        latitude = kwargs["latitude"]
        longitude = kwargs["longitude"]
        days = min(kwargs.get("days", 14), 14)

        settings = get_construction_settings()

        if settings.openweathermap_api_key:
            return self._fetch_live(
                latitude, longitude, days, settings.openweathermap_api_key
            )
        return self._mock_forecast(latitude, longitude, days)

    def _fetch_live(
        self,
        lat: float,
        lon: float,
        days: int,
        api_key: str,
    ) -> str:
        try:
            url = (
                "https://api.openweathermap.org/data/3.0/onecall"
                f"?lat={lat}&lon={lon}"
                f"&exclude=minutely,hourly"
                f"&units=imperial&appid={api_key}"
            )
            resp = httpx.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            daily = data.get("daily", [])[:days]
            alerts = data.get("alerts", [])
            forecast = []
            for day in daily:
                forecast.append({
                    "date": datetime.fromtimestamp(
                        day["dt"], tz=UTC
                    ).strftime("%Y-%m-%d"),
                    "temp_high_f": day["temp"]["max"],
                    "temp_low_f": day["temp"]["min"],
                    "precipitation_probability": day.get("pop", 0),
                    "rain_inches": round(
                        day.get("rain", 0) / 25.4, 2
                    ),
                    "wind_speed_mph": day.get("wind_speed", 0),
                    "wind_gust_mph": day.get("wind_gust", 0),
                    "description": day["weather"][0]["description"],
                })

            result = {"forecast": forecast, "alerts": []}
            for alert in alerts:
                result["alerts"].append({
                    "event": alert.get("event", "Unknown"),
                    "start": alert.get("start"),
                    "end": alert.get("end"),
                    "description": alert.get("description", ""),
                })

            return json.dumps(result, indent=2)
        except Exception as exc:
            return f"Error fetching weather: {exc}"

    def _mock_forecast(
        self,
        lat: float,
        lon: float,
        days: int,
    ) -> str:
        now = datetime.now(UTC)
        forecast = []
        for i in range(days):
            day_date = now + timedelta(days=i)
            forecast.append({
                "date": day_date.strftime("%Y-%m-%d"),
                "temp_high_f": 75 + (i % 5) * 2,
                "temp_low_f": 55 + (i % 5),
                "precipitation_probability": 0.1 * (i % 4),
                "rain_inches": 0.0 if i % 4 != 3 else 0.5,
                "wind_speed_mph": 8 + (i % 3) * 3,
                "wind_gust_mph": 15 + (i % 3) * 5,
                "description": "partly cloudy"
                if i % 4 != 3
                else "thunderstorm",
            })

        alerts = []
        if days >= 7:
            alerts.append({
                "event": "Wind Advisory",
                "start": (now + timedelta(days=5)).isoformat(),
                "end": (now + timedelta(days=6)).isoformat(),
                "description": (
                    "Sustained winds 25-35 mph with gusts to 50 mph."
                    " Crane operations may be affected."
                ),
            })

        result = {
            "forecast": forecast,
            "alerts": alerts,
            "note": "Mock data — no API key configured",
        }
        return json.dumps(result, indent=2)
