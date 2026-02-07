"""Document intelligence API endpoints."""

from datetime import UTC, datetime

from fastapi import APIRouter

from construction.schemas.document import (
    Contradiction,
    DocumentRef,
    IngestRequest,
    IngestResponse,
    SearchRequest,
    SearchResponse,
    SearchResult,
)

router = APIRouter()

_MOCK_DOC = DocumentRef(
    id="DOC-001",
    title="Structural Specification Rev C",
    doc_type="spec",
    version="C",
    author="Smith Engineering",
    created_at=datetime(2025, 1, 10, tzinfo=UTC),
)


@router.post("/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """Semantic search across project documents."""
    return SearchResponse(
        results=[
            SearchResult(
                document=_MOCK_DOC,
                relevance_score=0.92,
                snippet=(
                    "Section 3.2: Concrete mix design shall"
                    " achieve 5000 PSI at 28 days."
                ),
                page_number=12,
                section="3.2",
            )
        ],
        total_count=1,
        query=request.query,
        search_time_ms=42.5,
    )


@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(request: IngestRequest):
    """Ingest a new document into the knowledge base."""
    return IngestResponse(
        document_id="DOC-NEW-001",
        chunks_created=24,
        embedding_generated=True,
    )


@router.get(
    "/contradictions", response_model=list[Contradiction]
)
async def list_contradictions():
    """List detected contradictions between documents."""
    return [
        Contradiction(
            id="CONTRA-001",
            doc_a=_MOCK_DOC,
            doc_b=DocumentRef(
                id="DOC-002",
                title="Drawing Set A-101",
                doc_type="drawing",
                version="A",
                created_at=datetime(
                    2025, 1, 12, tzinfo=UTC
                ),
            ),
            description=(
                "Spec calls for 5000 PSI concrete but"
                " drawing note references 4000 PSI"
            ),
            severity="high",
            field_a="concrete_strength: 5000 PSI",
            field_b="concrete_strength: 4000 PSI",
            status="open",
        )
    ]
