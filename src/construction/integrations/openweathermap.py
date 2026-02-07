"""OpenWeatherMap API client."""

import logging

from construction.integrations.base_client import BaseAsyncClient

logger = logging.getLogger(__name__)


class OpenWeatherMapClient(BaseAsyncClient):
    """Client for the OpenWeatherMap API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.openweathermap.org",
        **kwargs,
    ):
        super().__init__(base_url=base_url, **kwargs)
        self.api_key = api_key

    def _params(self, **extra) -> dict:
        """Build query params with the API key included."""
        return {"appid": self.api_key, "units": "metric", **extra}

    async def get_forecast(
        self, lat: float, lon: float, days: int = 14
    ) -> dict:
        """Get weather forecast for a location.

        The free tier provides 5-day / 3-hour forecasts; the cnt
        parameter limits the number of 3-hour blocks returned.
        """
        cnt = min(days * 8, 40)  # max 40 blocks (5 days)
        resp = await self.get(
            "/data/2.5/forecast",
            params=self._params(lat=lat, lon=lon, cnt=cnt),
        )
        return resp.json()

    async def get_current(self, lat: float, lon: float) -> dict:
        """Get current weather for a location."""
        resp = await self.get(
            "/data/2.5/weather",
            params=self._params(lat=lat, lon=lon),
        )
        return resp.json()

    async def get_alerts(self, lat: float, lon: float) -> dict:
        """Get weather alerts via the One Call API."""
        resp = await self.get(
            "/data/3.0/onecall",
            params=self._params(
                lat=lat, lon=lon, exclude="minutely,hourly,daily"
            ),
        )
        return resp.json()
