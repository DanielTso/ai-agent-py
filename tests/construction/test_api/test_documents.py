"""Tests for document intelligence endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from construction.api.app import app


@pytest.mark.asyncio
async def test_search_documents():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/documents/search",
            json={
                "query": "concrete mix design",
                "project_id": "test-project",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert data["total_count"] >= 1
        assert data["query"] == "concrete mix design"


@pytest.mark.asyncio
async def test_ingest_document():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/documents/ingest",
            json={
                "project_id": "test-project",
                "title": "Test Spec",
                "doc_type": "spec",
                "content": "Test content",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["document_id"] == "DOC-NEW-001"
        assert data["chunks_created"] == 24
        assert data["embedding_generated"] is True


@pytest.mark.asyncio
async def test_list_contradictions():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/documents/contradictions"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["severity"] == "high"
