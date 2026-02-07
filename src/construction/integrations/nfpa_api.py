"""NFPA codes and NEC (National Electrical Code) API client."""

import logging

from construction.integrations.base_client import BaseAsyncClient

logger = logging.getLogger(__name__)


class NFPAClient(BaseAsyncClient):
    """Client for the NFPA codes and standards API."""

    def __init__(
        self,
        base_url: str = "https://api.nfpa.org/codes/v1",
        **kwargs,
    ):
        super().__init__(base_url=base_url, **kwargs)

    async def search_codes(
        self,
        code_name: str | None = None,
        article: str | None = None,
        keyword: str | None = None,
    ) -> list[dict]:
        """Search NFPA codes with optional filters."""
        params: dict = {}
        if code_name:
            params["code_name"] = code_name
        if article:
            params["article"] = article
        if keyword:
            params["keyword"] = keyword
        resp = await self.get("/codes", params=params)
        return resp.json()

    async def get_code_section(
        self, code: str, section: str
    ) -> dict:
        """Get a specific section of an NFPA code."""
        resp = await self.get(f"/codes/{code}/sections/{section}")
        return resp.json()

    async def get_nec_article(self, article_number: str) -> dict:
        """Get a specific NEC (NFPA 70) article."""
        resp = await self.get(f"/codes/nfpa70/articles/{article_number}")
        return resp.json()

    async def search_violations(self, keyword: str) -> list[dict]:
        """Search NFPA violation records by keyword."""
        resp = await self.get(
            "/violations", params={"keyword": keyword}
        )
        return resp.json()
