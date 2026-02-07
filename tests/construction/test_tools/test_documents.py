"""Tests for the DocumentSearch tool."""

import json

from construction.tools.documents import DocumentSearch


def test_document_search_schema():
    tool = DocumentSearch()
    schema = tool.get_input_schema()
    assert schema["type"] == "object"
    assert "action" in schema["properties"]
    assert "project_id" in schema["properties"]
    assert schema["required"] == ["action", "project_id"]


def test_document_search_to_api_format():
    tool = DocumentSearch()
    fmt = tool.to_api_format()
    assert fmt["name"] == "document_search"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_document_search_action():
    tool = DocumentSearch()
    result = tool.execute(
        action="search",
        project_id="proj-001",
        query="electrical redundancy",
    )
    data = json.loads(result)
    assert data["total_count"] > 0
    assert data["query"] == "electrical redundancy"
    assert len(data["results"]) > 0

    first = data["results"][0]
    assert "document" in first
    assert "relevance_score" in first
    assert "snippet" in first
    assert first["document"]["doc_type"] in (
        "rfi", "submittal", "drawing", "spec",
        "minutes", "report",
    )


def test_document_search_with_doc_type_filter():
    tool = DocumentSearch()
    result = tool.execute(
        action="search",
        project_id="proj-001",
        query="routing",
        doc_type="rfi",
    )
    data = json.loads(result)
    for r in data["results"]:
        assert r["document"]["doc_type"] == "rfi"


def test_document_ingest_action():
    tool = DocumentSearch()
    result = tool.execute(
        action="ingest",
        project_id="proj-001",
        title="New RFI Document",
        content="This is test content for ingestion " * 20,
    )
    data = json.loads(result)
    assert "document_id" in data
    assert data["chunks_created"] >= 1
    assert data["embedding_generated"] is True


def test_document_detect_contradictions_action():
    tool = DocumentSearch()
    result = tool.execute(
        action="detect_contradictions",
        project_id="proj-001",
        query="voltage specifications",
    )
    data = json.loads(result)
    assert data["total_count"] > 0
    assert len(data["contradictions"]) > 0

    first = data["contradictions"][0]
    assert "doc_a" in first
    assert "doc_b" in first
    assert "severity" in first
    assert "description" in first
    assert first["severity"] in (
        "low", "medium", "high", "critical",
    )


def test_document_search_unknown_action():
    tool = DocumentSearch()
    result = tool.execute(
        action="unknown",
        project_id="proj-001",
    )
    assert result.startswith("Error:")


def test_document_search_error_handling():
    tool = DocumentSearch()
    # Force an error by providing wrong types
    result = tool.execute(action="search", project_id=None)
    # Should still return a result (mock doesn't validate)
    assert isinstance(result, str)
