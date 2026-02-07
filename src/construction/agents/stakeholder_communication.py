"""Stakeholder Communication agent — auto-draft reports, RFIs, notices."""

import json
from datetime import UTC, datetime

from construction.agents.base import ConstructionAgent
from construction.schemas.common import AgentEvent, DataSource
from construction.tools.communication import DraftCommunication


class StakeholderCommunicationAgent(ConstructionAgent):
    """Auto-draft owner reports, RFI responses, sub notices with contract refs."""

    name = "stakeholder_communication"
    description = (
        "Auto-draft owner reports, RFI responses,"
        " sub notices with contract refs"
    )
    schedule = "on_demand"

    def _register_tools(self) -> None:
        self._tools.register(DraftCommunication())

    def get_system_prompt(self) -> str:
        return (
            "You are a construction communication expert"
            " specializing in stakeholder correspondence.\n\n"
            "Key responsibilities:\n"
            "- Draft owner reports in a professional"
            " business tone\n"
            "- Prepare RFI responses with technical"
            " accuracy and code references\n"
            "- Draft subcontractor notices in a formal"
            " contractual tone with clause references\n"
            "- Create periodic owner updates with key"
            " metrics and concerns\n\n"
            "Tone guidelines:\n"
            "- Owner communications: business tone,"
            " executive-level summary\n"
            "- Subcontractor notices: contractual tone,"
            " always include contract clause references\n"
            "- RFI responses: technical tone with"
            " drawing and code references\n\n"
            "Important rules:\n"
            "- NEVER make decisions — only draft"
            " communications for PM review\n"
            "- Always include relevant contract clause"
            " references in sub notices\n"
            "- Include data sources and confidence"
            " levels in reports\n"
            "- Flag any communication that references"
            " claims or disputes for legal review\n\n"
            "Output your drafts as structured JSON"
            " matching the requested communication type."
        )

    async def run(self, context: dict | None = None) -> AgentEvent:
        """Draft communications based on the provided context."""
        ctx = context or {}
        project_id = ctx.get("project_id", "default")
        action = ctx.get("action", "owner_update")

        prompt = (
            f"Draft a {action} for project {project_id}."
            f" Context: {json.dumps(ctx)}"
            " Use the appropriate tone and include all"
            " required references. This is a draft for"
            " PM review — do not make any decisions."
        )

        response = self.chat(prompt)

        transparency_log = [
            f"Drafted {action} for project {project_id}",
            f"Context provided: {list(ctx.keys())}",
            "Draft marked for PM review",
            f"Model response length: {len(response)} chars",
        ]

        try:
            draft_data = json.loads(response)
        except (json.JSONDecodeError, TypeError):
            draft_data = {"raw_response": response}

        return await self.publish_event(
            event_type="communication_draft",
            severity="info",
            data=draft_data,
            confidence=0.80,
            data_sources=[
                DataSource(
                    source_type="database",
                    source_name="draft_communication",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.80,
                ),
            ],
            transparency_log=transparency_log,
            requires_cross_agent=False,
        )
