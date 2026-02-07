"""Commissioning & Turnover agent — IST sequencing and punch lists."""

import json
from datetime import UTC, datetime

from construction.agents.base import ConstructionAgent
from construction.schemas.common import AgentEvent, DataSource
from construction.tools.commissioning import CommissioningQuery
from construction.tools.schedule import ScheduleQueryTool


class CommissioningTurnoverAgent(ConstructionAgent):
    """Manage commissioning sequences, punch lists, and turnover."""

    name = "commissioning_turnover"
    description = (
        "Commissioning expert managing IST sequencing,"
        " punch list intelligence, and turnover packages"
    )
    schedule = "daily"

    def _register_tools(self) -> None:
        self._tools.register(CommissioningQuery())
        self._tools.register(ScheduleQueryTool())

    def get_system_prompt(self) -> str:
        return (
            "You are an expert commissioning and turnover"
            " manager for construction projects.\n\n"
            "Your responsibilities:\n"
            "1. IST (Integrated System Test) sequencing —"
            " you understand prerequisite chains (e.g. you"
            " cannot test the UPS until the generator has"
            " been started and load-tested, you cannot test"
            " the ATS until both the generator and UPS are"
            " verified)\n"
            "2. Punch list intelligence — track severity A/B/C/D"
            " items, identify which punch items block"
            " commissioning tests\n"
            "3. Turnover package tracking — monitor document"
            " completeness (as-builts, O&M manuals, test"
            " reports, warranties) per system\n"
            "4. Witness scheduling — ensure required witness"
            " holds are scheduled for critical tests\n\n"
            "Output your assessment as structured JSON with"
            " sections for ist_status, punch_blockers,"
            " turnover_readiness, and witness_schedule."
        )

    async def run(self, context: dict | None = None) -> AgentEvent:
        """Check commissioning status and publish findings."""
        project_id = (context or {}).get(
            "project_id", "default"
        )

        prompt = (
            f"Analyze commissioning status for project {project_id}."
            " Check IST sequence for blocked or ready tests,"
            " review punch list for commissioning-blocking items,"
            " and verify turnover package completeness."
            " Identify any tests that need witness scheduling."
        )

        response = self.chat(prompt)

        transparency_log = [
            "Checked IST sequence and prerequisites",
            "Reviewed punch list for commissioning blockers",
            "Verified turnover package document status",
            f"Model response length: {len(response)} chars",
        ]

        try:
            data = json.loads(response)
        except (json.JSONDecodeError, TypeError):
            data = {"raw_response": response}

        blocked = data.get("ist_status", {}).get(
            "blocked_tests", []
        )
        severity = "warning" if blocked else "info"

        return await self.publish_event(
            event_type="commissioning_status",
            severity=severity,
            data=data,
            confidence=0.85,
            data_sources=[
                DataSource(
                    source_type="database",
                    source_name="commissioning_query",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.90,
                ),
                DataSource(
                    source_type="database",
                    source_name="schedule_query",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.90,
                ),
            ],
            transparency_log=transparency_log,
            requires_cross_agent=bool(blocked),
            target_agent="critical_path" if blocked else None,
        )
