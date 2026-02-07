"""Document search and ingestion tool using pgvector semantic search."""

import json
import uuid

from ai_agent.tools import Tool


class DocumentSearch(Tool):
    """Semantic search across construction documents."""

    name = "document_search"
    description = (
        "Search construction documents using semantic search."
        " Understands construction ontology"
        " (N+1 vs 2N, etc.)."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "search",
                        "ingest",
                        "detect_contradictions",
                    ],
                    "description": (
                        "Action to perform: search, ingest,"
                        " or detect_contradictions"
                    ),
                },
                "project_id": {
                    "type": "string",
                    "description": "Project identifier",
                },
                "query": {
                    "type": "string",
                    "description": (
                        "Search query (required for search"
                        " and detect_contradictions)"
                    ),
                },
                "doc_type": {
                    "type": "string",
                    "description": "Document type filter",
                },
                "content": {
                    "type": "string",
                    "description": (
                        "Document content (required for ingest)"
                    ),
                },
                "title": {
                    "type": "string",
                    "description": (
                        "Document title (required for ingest)"
                    ),
                },
                "metadata": {
                    "type": "object",
                    "description": "Additional metadata",
                },
            },
            "required": ["action", "project_id"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        try:
            if action == "search":
                return self._mock_search(**kwargs)
            elif action == "ingest":
                return self._mock_ingest(**kwargs)
            elif action == "detect_contradictions":
                return self._mock_detect_contradictions(**kwargs)
            else:
                return f"Error: Unknown action '{action}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _mock_search(self, **kwargs) -> str:
        query = kwargs.get("query", "")
        project_id = kwargs["project_id"]
        doc_type = kwargs.get("doc_type")

        results = [
            {
                "document": {
                    "id": str(uuid.uuid4()),
                    "title": "Electrical Specification Rev C",
                    "doc_type": "spec",
                    "version": "C",
                    "author": "J. Martinez",
                    "source_url": None,
                    "created_at": "2025-06-15T10:00:00Z",
                },
                "relevance_score": 0.94,
                "snippet": (
                    "Section 26 05 00: N+1 redundancy required"
                    " for all critical power distribution"
                    " systems per owner requirements."
                ),
                "page_number": 42,
                "section": "26 05 00",
            },
            {
                "document": {
                    "id": str(uuid.uuid4()),
                    "title": "MEP Coordination Drawing Set",
                    "doc_type": "drawing",
                    "version": "R2",
                    "author": "Smith Engineering",
                    "source_url": None,
                    "created_at": "2025-07-01T14:30:00Z",
                },
                "relevance_score": 0.87,
                "snippet": (
                    "Drawing E-401: Main switchgear room layout"
                    " showing 2N configuration for UPS systems"
                    " with 30-inch maintenance clearance."
                ),
                "page_number": 12,
                "section": "E-401",
            },
            {
                "document": {
                    "id": str(uuid.uuid4()),
                    "title": "RFI-2024-0847: Conduit Routing",
                    "doc_type": "rfi",
                    "version": None,
                    "author": "GC Field Team",
                    "source_url": None,
                    "created_at": "2025-08-20T09:15:00Z",
                },
                "relevance_score": 0.72,
                "snippet": (
                    "Requesting clarification on conduit"
                    " routing from MDP-3 to Panel LP-2A."
                    " Conflict with HVAC ductwork at"
                    " elevation 12'-6\"."
                ),
                "page_number": None,
                "section": None,
            },
        ]

        if doc_type:
            results = [
                r for r in results
                if r["document"]["doc_type"] == doc_type
            ]

        response = {
            "results": results,
            "total_count": len(results),
            "query": query,
            "project_id": project_id,
            "search_time_ms": 127.5,
            "note": (
                "Mock data — production would use"
                " pgvector semantic search"
            ),
        }
        return json.dumps(response, indent=2)

    def _mock_ingest(self, **kwargs) -> str:
        title = kwargs.get("title", "Untitled")
        content = kwargs.get("content", "")

        response = {
            "document_id": str(uuid.uuid4()),
            "title": title,
            "chunks_created": max(1, len(content) // 500),
            "embedding_generated": True,
            "note": (
                "Mock data — production would chunk,"
                " embed, and store in pgvector"
            ),
        }
        return json.dumps(response, indent=2)

    def _mock_detect_contradictions(self, **kwargs) -> str:
        query = kwargs.get("query", "")
        project_id = kwargs["project_id"]

        contradictions = [
            {
                "id": str(uuid.uuid4()),
                "doc_a": {
                    "id": str(uuid.uuid4()),
                    "title": "Electrical Specification Rev C",
                    "doc_type": "spec",
                    "version": "C",
                    "author": "J. Martinez",
                    "source_url": None,
                    "created_at": "2025-06-15T10:00:00Z",
                },
                "doc_b": {
                    "id": str(uuid.uuid4()),
                    "title": "MEP Coordination Drawing Set",
                    "doc_type": "drawing",
                    "version": "R2",
                    "author": "Smith Engineering",
                    "source_url": None,
                    "created_at": "2025-07-01T14:30:00Z",
                },
                "description": (
                    "Spec calls for N+1 redundancy on critical"
                    " power but drawing E-401 shows 2N"
                    " configuration. These are different"
                    " redundancy levels with cost implications."
                ),
                "severity": "high",
                "field_a": (
                    "Section 26 05 00: N+1 redundancy"
                ),
                "field_b": (
                    "Drawing E-401: 2N configuration"
                ),
                "status": "open",
            },
            {
                "id": str(uuid.uuid4()),
                "doc_a": {
                    "id": str(uuid.uuid4()),
                    "title": "Electrical Specification Rev C",
                    "doc_type": "spec",
                    "version": "C",
                    "author": "J. Martinez",
                    "source_url": None,
                    "created_at": "2025-06-15T10:00:00Z",
                },
                "doc_b": {
                    "id": str(uuid.uuid4()),
                    "title": "Meeting Minutes 2025-07-15",
                    "doc_type": "minutes",
                    "version": None,
                    "author": "PM Office",
                    "source_url": None,
                    "created_at": "2025-07-15T16:00:00Z",
                },
                "description": (
                    "Spec requires 480V service entrance"
                    " but meeting minutes reference owner"
                    " request for 277/480V wye configuration."
                    " Voltage mismatch may affect transformer"
                    " sizing."
                ),
                "severity": "critical",
                "field_a": (
                    "Section 26 05 00: 480V service entrance"
                ),
                "field_b": (
                    "Minutes item 7: 277/480V wye"
                ),
                "status": "open",
            },
        ]

        response = {
            "contradictions": contradictions,
            "total_count": len(contradictions),
            "query": query,
            "project_id": project_id,
            "scan_time_ms": 342.8,
            "note": (
                "Mock data — production would use"
                " embeddings to detect semantic conflicts"
            ),
        }
        return json.dumps(response, indent=2)
