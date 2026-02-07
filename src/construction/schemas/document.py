"""Pydantic schemas for document intelligence agent."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class DocumentRef(BaseModel):
    """Reference to a construction document."""

    id: str
    title: str
    doc_type: Literal[
        "rfi", "submittal", "drawing", "spec", "minutes", "report"
    ]
    version: str | None = None
    author: str | None = None
    source_url: str | None = None
    created_at: datetime


class SearchResult(BaseModel):
    """A single search result with relevance scoring."""

    document: DocumentRef
    relevance_score: float = Field(ge=0, le=1)
    snippet: str
    page_number: int | None = None
    section: str | None = None


class SearchRequest(BaseModel):
    """Request to search construction documents."""

    query: str
    project_id: str
    doc_types: list[str] | None = None
    limit: int = 10
    min_relevance: float = 0.5


class SearchResponse(BaseModel):
    """Response from a document search."""

    results: list[SearchResult]
    total_count: int
    query: str
    search_time_ms: float


class Contradiction(BaseModel):
    """A detected contradiction between two documents."""

    id: str
    doc_a: DocumentRef
    doc_b: DocumentRef
    description: str
    severity: Literal["low", "medium", "high", "critical"]
    field_a: str
    field_b: str
    status: Literal[
        "open", "confirmed", "resolved", "false_positive"
    ] = "open"


class IngestRequest(BaseModel):
    """Request to ingest a new document."""

    project_id: str
    title: str
    doc_type: str
    content: str
    metadata: dict | None = None


class IngestResponse(BaseModel):
    """Response from document ingestion."""

    document_id: str
    chunks_created: int
    embedding_generated: bool
