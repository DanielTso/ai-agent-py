"""Claims & Dispute agent — records, delay analysis, notices."""

import json
from datetime import UTC, datetime

from construction.agents.base import ConstructionAgent
from construction.schemas.common import AgentEvent, DataSource
from construction.tools.claims import ClaimsQuery


class ClaimsDisputeAgent(ConstructionAgent):
    """Build contemporaneous claims records and track notices."""

    name = "claims_dispute"
    description = (
        "Construction claims expert managing delay analysis,"
        " notice tracking, and contemporaneous records"
    )
    schedule = "continuous"

    def _register_tools(self) -> None:
        self._tools.register(ClaimsQuery())

    def get_system_prompt(self) -> str:
        return (
            "You are an expert construction claims analyst."
            " Your role is to build and maintain contemporaneous"
            " records that protect the project's position.\n\n"
            "IMPORTANT: You NEVER file claims. You only build"
            " the factual record so the PM can make informed"
            " decisions.\n\n"
            "Your responsibilities:\n"
            "1. Contemporaneous record-keeping — capture events"
            " as they happen with dates, descriptions, and"
            " evidence references\n"
            "2. Delay analysis — perform TIA (Time Impact"
            " Analysis) and Windows analysis to quantify"
            " delay responsibility\n"
            "3. Notice tracking — monitor contractual notice"
            " deadlines, flag notices due within 7 days,"
            " track notice status (pending/sent/acknowledged)\n"
            "4. Causation chain — map event-to-impact chains"
            " to establish clear causation for potential claims\n"
            "5. Concurrent delay identification — flag where"
            " multiple parties share delay responsibility\n\n"
            "Output your assessment as structured JSON with"
            " sections for pending_notices, delay_status,"
            " new_events, and causation_chains."
        )

    async def run(self, context: dict | None = None) -> AgentEvent:
        """Check claims status and publish findings."""
        project_id = (context or {}).get(
            "project_id", "default"
        )

        prompt = (
            f"Analyze claims status for project {project_id}."
            " Check for notices approaching deadlines,"
            " review delay analyses for updated impacts,"
            " and identify any new claim events requiring"
            " documentation."
        )

        response = self.chat(prompt)

        transparency_log = [
            "Reviewed pending notice deadlines",
            "Checked delay analysis status",
            "Scanned for new claim-worthy events",
            f"Model response length: {len(response)} chars",
        ]

        try:
            data = json.loads(response)
        except (json.JSONDecodeError, TypeError):
            data = {"raw_response": response}

        urgent_notices = data.get("pending_notices", [])
        has_urgent = any(
            n.get("days_remaining", 99) <= 3
            for n in urgent_notices
        )
        severity = "critical" if has_urgent else (
            "warning" if urgent_notices else "info"
        )

        return await self.publish_event(
            event_type="claims_status",
            severity=severity,
            data=data,
            confidence=0.90,
            data_sources=[
                DataSource(
                    source_type="database",
                    source_name="claims_query",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.95,
                ),
            ],
            transparency_log=transparency_log,
            requires_cross_agent=has_urgent,
            target_agent=(
                "critical_path" if has_urgent else None
            ),
        )
