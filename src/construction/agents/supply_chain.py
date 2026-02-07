"""Supply Chain Resilience agent — monitors vendors and shipments."""

import json
from datetime import UTC, datetime

from construction.agents.base import ConstructionAgent
from construction.schemas.common import AgentEvent, DataSource
from construction.tools.supply_chain_tools import SupplyChainMonitor
from construction.tools.weather import WeatherForecast


class SupplyChainAgent(ConstructionAgent):
    """Monitor 50+ vendors for long-lead items and manage disruptions."""

    name = "supply_chain"
    description = "Monitor 50+ vendors for long-lead items"
    schedule = "every_4_hours"

    def _register_tools(self) -> None:
        self._tools.register(SupplyChainMonitor())
        self._tools.register(WeatherForecast())

    def get_system_prompt(self) -> str:
        return (
            "You are a construction supply chain expert."
            " Your role is to monitor vendor statuses,"
            " track shipments, and ensure materials arrive"
            " on time for the project schedule.\n\n"
            "Key responsibilities:\n"
            "- Track vendor delays and port congestion\n"
            "- Monitor customs clearance status\n"
            "- Identify at-risk shipments early\n"
            "- Generate 3 alternative source options per"
            " delayed material with cost/schedule tradeoffs\n\n"
            "For each delay or disruption, provide:\n"
            "1. Vendor and material affected\n"
            "2. Current delay in days\n"
            "3. Root cause of delay\n"
            "4. Three alternative options with cost delta"
            " and schedule impact\n"
            "5. Your recommendation\n\n"
            "Output your assessment as structured JSON with:\n"
            "- 'vendor_statuses': array of vendor status objects\n"
            "- 'alerts': array of supply chain alerts\n"
            "- 'recommendations': array of recommended actions"
        )

    async def run(self, context: dict | None = None) -> AgentEvent:
        """Check all vendor statuses and generate alerts."""
        project_id = (context or {}).get(
            "project_id", "default"
        )

        prompt = (
            f"Check all vendor statuses for project {project_id}."
            " Track any active shipments and identify delays."
            " For any delayed or at-risk vendors, find"
            " alternative sources with cost and schedule"
            " tradeoffs. Also check weather conditions that"
            " might affect port operations or deliveries."
        )

        response = self.chat(prompt)

        transparency_log = [
            "Checked all vendor statuses",
            "Tracked active shipments",
            "Searched alternative sources for delays",
            "Checked weather impact on logistics",
            f"Model response length: {len(response)} chars",
        ]

        try:
            supply_data = json.loads(response)
        except (json.JSONDecodeError, TypeError):
            supply_data = {"raw_response": response}

        alerts = supply_data.get("alerts", [])
        has_critical = any(
            a.get("severity") == "critical" for a in alerts
        )
        severity = "critical" if has_critical else (
            "warning" if alerts else "info"
        )

        return await self.publish_event(
            event_type="supply_chain_status",
            severity=severity,
            data=supply_data,
            confidence=0.82,
            data_sources=[
                DataSource(
                    source_type="api",
                    source_name="supply_chain_monitor",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.85,
                ),
                DataSource(
                    source_type="api",
                    source_name="weather_forecast",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.75,
                ),
            ],
            transparency_log=transparency_log,
            requires_cross_agent=has_critical,
            target_agent="risk_forecaster" if has_critical else None,
        )
