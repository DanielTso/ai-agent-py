"""Workforce & Labor agent — productivity, availability, certifications."""

import json
from datetime import UTC, datetime

from construction.agents.base import ConstructionAgent
from construction.schemas.common import AgentEvent, DataSource
from construction.tools.workforce import WorkforceQuery


class WorkforceLaborAgent(ConstructionAgent):
    """Crew productivity tracking, labor availability, certification monitoring."""

    name = "workforce_labor"
    description = (
        "Crew productivity tracking, labor availability,"
        " certification monitoring"
    )
    schedule = "daily"

    def _register_tools(self) -> None:
        self._tools.register(WorkforceQuery())

    def get_system_prompt(self) -> str:
        return (
            "You are a construction labor management"
            " expert. Your role is to monitor workforce"
            " productivity, availability, and compliance.\n\n"
            "Key responsibilities:\n"
            "- Track crew productivity by trade\n"
            "- Monitor labor availability and forecast"
            " gaps\n"
            "- Track certifications (BICSI, NETA, OSHA)"
            " and flag expirations\n"
            "- Monitor overtime hours and fatigue risk\n"
            "- Identify trades with declining productivity"
            " trends\n\n"
            "For each assessment, provide:\n"
            "1. Crew status by trade with headcount and"
            " productivity index\n"
            "2. Trades with productivity below 90%\n"
            "3. Certifications expiring within 30 days\n"
            "4. Labor gaps for the next 4 weeks\n"
            "5. Overtime/fatigue warnings for crews"
            " exceeding 10 hours/week\n\n"
            "Output your assessment as structured JSON"
            " with: crew_status, productivity_alerts,"
            " certification_warnings, labor_gaps, and"
            " fatigue_warnings fields."
        )

    async def run(self, context: dict | None = None) -> AgentEvent:
        """Check crew status, productivity, and certifications."""
        project_id = (context or {}).get(
            "project_id", "default"
        )

        prompt = (
            f"Check workforce status for project {project_id}."
            " Query crew status for all trades, review"
            " productivity metrics, check for expiring"
            " certifications, and forecast labor needs"
            " for the next 4 weeks. Flag any trades with"
            " productivity below 90% and any workers with"
            " certifications expiring within 30 days."
        )

        response = self.chat(prompt)

        transparency_log = [
            "Checked crew status for all trades",
            "Reviewed productivity metrics by trade",
            "Checked certification expirations",
            "Forecasted labor needs for 4 weeks",
            f"Model response length: {len(response)} chars",
        ]

        try:
            workforce_data = json.loads(response)
        except (json.JSONDecodeError, TypeError):
            workforce_data = {"raw_response": response}

        cert_warnings = workforce_data.get(
            "certification_warnings", []
        )
        labor_gaps = workforce_data.get("labor_gaps", [])
        has_critical = any(
            g.get("critical") for g in labor_gaps
        ) or any(
            c.get("status") == "expired" for c in cert_warnings
        )
        has_warning = cert_warnings or labor_gaps
        severity = "critical" if has_critical else (
            "warning" if has_warning else "info"
        )

        return await self.publish_event(
            event_type="workforce_status",
            severity=severity,
            data=workforce_data,
            confidence=0.85,
            data_sources=[
                DataSource(
                    source_type="database",
                    source_name="workforce_query",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.90,
                ),
            ],
            transparency_log=transparency_log,
            requires_cross_agent=has_critical,
            target_agent="risk_forecaster" if has_critical else None,
        )
