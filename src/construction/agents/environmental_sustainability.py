"""Environmental & Sustainability agent — permits, LEED, carbon."""

import json
from datetime import UTC, datetime

from construction.agents.base import ConstructionAgent
from construction.schemas.common import AgentEvent, DataSource
from construction.tools.environmental import EnvironmentalQuery
from construction.tools.epa_compliance import EpaComplianceTool
from construction.tools.weather import WeatherForecast


class EnvironmentalSustainabilityAgent(ConstructionAgent):
    """Monitor environmental compliance and sustainability."""

    name = "environmental_sustainability"
    description = (
        "Environmental compliance expert managing SWPPP,"
        " LEED credits, carbon footprint, and permits"
    )
    schedule = "daily"

    def _register_tools(self) -> None:
        self._tools.register(EnvironmentalQuery())
        self._tools.register(WeatherForecast())
        self._tools.register(EpaComplianceTool())

    def get_system_prompt(self) -> str:
        return (
            "You are an expert environmental compliance and"
            " sustainability manager for construction projects.\n\n"
            "Your responsibilities:\n"
            "1. SWPPP compliance — monitor stormwater pollution"
            " prevention, ensure weekly inspections, track"
            " corrective actions. Rain events >0.5 inches"
            " require 24-hour post-storm inspection.\n"
            "2. LEED credit tracking — monitor points earned vs"
            " available, flag at-risk credits, ensure"
            " documentation is complete\n"
            "3. Carbon footprint — track Scope 1/2/3 emissions"
            " against targets, identify reduction opportunities\n"
            "4. Permit management — monitor permit expiry dates,"
            " flag permits expiring within 30 days, ensure"
            " conditions are being met\n"
            "5. Weather-driven environmental risk — when rain is"
            " forecast, check erosion controls; when wind is"
            " forecast, check dust controls\n"
            "6. EPA compliance — NPDES discharge permits, CAA"
            " air quality, RCRA hazardous waste, NEPA review"
            " status, stormwater CGP compliance\n\n"
            "Output your assessment as structured JSON with"
            " sections for permit_alerts, leed_status,"
            " carbon_tracking, and swppp_compliance."
        )

    async def run(self, context: dict | None = None) -> AgentEvent:
        """Check environmental compliance and publish findings."""
        project_id = (context or {}).get(
            "project_id", "default"
        )

        prompt = (
            f"Analyze environmental compliance for project {project_id}."
            " Check permit status for any expiring permits,"
            " review LEED credit tracking for at-risk credits,"
            " verify SWPPP inspection compliance, and check"
            " weather forecast for environmental risk triggers."
        )

        response = self.chat(prompt)

        transparency_log = [
            "Checked environmental permit status",
            "Reviewed LEED credit tracking",
            "Verified SWPPP inspection schedule",
            "Checked weather forecast for env risk",
            f"Model response length: {len(response)} chars",
        ]

        try:
            data = json.loads(response)
        except (json.JSONDecodeError, TypeError):
            data = {"raw_response": response}

        permit_alerts = data.get("permit_alerts", [])
        has_violation_risk = any(
            a.get("risk") == "violation"
            for a in permit_alerts
        )
        severity = "critical" if has_violation_risk else (
            "warning" if permit_alerts else "info"
        )

        return await self.publish_event(
            event_type="environmental_status",
            severity=severity,
            data=data,
            confidence=0.85,
            data_sources=[
                DataSource(
                    source_type="api",
                    source_name="environmental_query",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.90,
                ),
                DataSource(
                    source_type="api",
                    source_name="weather_forecast",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.75,
                ),
            ],
            transparency_log=transparency_log,
            requires_cross_agent=has_violation_risk,
            target_agent=(
                "compliance" if has_violation_risk else None
            ),
        )
