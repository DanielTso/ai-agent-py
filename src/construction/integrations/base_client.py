"""Base async HTTP client with retry, rate-limit, and authentication."""

import asyncio
import logging
from abc import ABC
from datetime import UTC, datetime

import httpx

logger = logging.getLogger(__name__)


class BaseAsyncClient(ABC):
    """Base class for all external API integration clients."""

    def __init__(
        self,
        base_url: str,
        auth_headers: dict[str, str] | None = None,
        max_retries: int = 3,
        rate_limit_per_second: float = 10.0,
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.auth_headers = auth_headers or {}
        self.max_retries = max_retries
        self.rate_limit_per_second = rate_limit_per_second
        self.timeout = timeout
        self._last_request_time: datetime | None = None
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=self.auth_headers,
                timeout=self.timeout,
            )
        return self._client

    async def _rate_limit(self):
        if self._last_request_time and self.rate_limit_per_second > 0:
            elapsed = (
                datetime.now(UTC) - self._last_request_time
            ).total_seconds()
            min_interval = 1.0 / self.rate_limit_per_second
            if elapsed < min_interval:
                await asyncio.sleep(min_interval - elapsed)
        self._last_request_time = datetime.now(UTC)

    async def _request(self, method, path, **kwargs) -> httpx.Response:
        client = await self._get_client()
        last_exc = None
        for attempt in range(self.max_retries):
            await self._rate_limit()
            try:
                response = await client.request(method, path, **kwargs)
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code in (429, 500, 502, 503, 504):
                    last_exc = exc
                    wait = 2**attempt
                    logger.warning(
                        "Retry %d/%d after %ds: %s",
                        attempt + 1,
                        self.max_retries,
                        wait,
                        exc,
                    )
                    await asyncio.sleep(wait)
                else:
                    raise
            except httpx.RequestError as exc:
                last_exc = exc
                wait = 2**attempt
                logger.warning(
                    "Retry %d/%d after %ds: %s",
                    attempt + 1,
                    self.max_retries,
                    wait,
                    exc,
                )
                await asyncio.sleep(wait)
        raise last_exc  # type: ignore[misc]

    async def get(self, path, **kwargs):
        return await self._request("GET", path, **kwargs)

    async def post(self, path, **kwargs):
        return await self._request("POST", path, **kwargs)

    async def put(self, path, **kwargs):
        return await self._request("PUT", path, **kwargs)

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()
