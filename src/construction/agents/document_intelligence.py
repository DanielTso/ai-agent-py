"""Document Intelligence agent — semantic search across construction docs."""

import uuid
from datetime import UTC, datetime

from construction.agents.base import ConstructionAgent
from construction.schemas.common import AgentEvent, DataSource
from construction.tools.documents import DocumentSearch


class DocumentIntelligenceAgent(ConstructionAgent):
    """Semantic search across 10k+ docs with construction ontology."""

    name = "document_intelligence"
    description = (
        "Semantic search across 10k+ docs with"
        " construction ontology"
    )
    schedule = "on_demand"

    def _register_tools(self) -> None:
        self._tools.register(DocumentSearch())

    def get_system_prompt(self) -> str:
        return (
            "You are a Construction Document Intelligence expert."
            " You have access to all project documents including"
            " RFIs, submittals, drawings, specifications, meeting"
            " minutes, and reports.\n\n"
            "Your capabilities:\n"
            "- Semantic search across 10,000+ documents\n"
            "- Understanding of construction ontology:"
            " N+1 redundancy vs 2N configurations,"
            " CSI MasterFormat divisions, NEC/IBC code"
            " references\n"
            "- Auto-detection of contradictions between"
            " documents (e.g., drawing vs spec voltage"
            " mismatch, conflicting redundancy levels)\n"
            "- Source-traced answers: every response"
            " includes document version, date, and"
            " author for full audit trail\n\n"
            "When answering questions:\n"
            "1. Always cite the source document with"
            " version, date, and author\n"
            "2. Flag any contradictions you detect"
            " between documents\n"
            "3. Note the confidence level of your"
            " findings\n"
            "4. Highlight any documents that may be"
            " superseded by newer versions"
        )

    async def run(
        self, context: dict | None = None
    ) -> AgentEvent:
        """Run document search or contradiction detection."""
        context = context or {}
        action = context.get("action", "search")
        project_id = context.get("project_id", "")
        query = context.get("query", "")

        tool = self._tools.get("document_search")
        if not tool:
            return await self._error_event(
                "document_search tool not registered"
            )

        result = tool.execute(
            action=action,
            project_id=project_id,
            query=query,
        )

        event_type = (
            "contradiction_detected"
            if action == "detect_contradictions"
            else "search_completed"
        )
        severity = (
            "warning"
            if action == "detect_contradictions"
            else "info"
        )

        return await self.publish_event(
            event_type=event_type,
            severity=severity,
            data={
                "action": action,
                "query": query,
                "project_id": project_id,
                "result": result,
            },
            confidence=0.85,
            data_sources=[
                DataSource(
                    source_type="database",
                    source_name="pgvector_documents",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.85,
                ),
            ],
            transparency_log=[
                f"Action: {action}",
                f"Query: {query}",
                f"Project: {project_id}",
            ],
            requires_cross_agent=(
                action == "detect_contradictions"
            ),
            target_agent=(
                "compliance"
                if action == "detect_contradictions"
                else None
            ),
        )

    async def _error_event(self, message: str) -> AgentEvent:
        """Create an error event."""
        return AgentEvent(
            event_id=str(uuid.uuid4()),
            source_agent=self.name,
            event_type="error",
            severity="warning",
            timestamp=datetime.now(UTC),
            data={"error": message},
            confidence=1.0,
        )
