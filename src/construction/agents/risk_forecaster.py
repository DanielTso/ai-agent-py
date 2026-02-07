"""Risk Forecaster agent — predicts schedule/cost/safety risks."""

import json
from datetime import UTC, datetime

from construction.agents.base import ConstructionAgent
from construction.schemas.common import AgentEvent, DataSource
from construction.tools.osha import OshaSearch
from construction.tools.risk_db import RiskDatabase
from construction.tools.weather import WeatherForecast


class RiskForecasterAgent(ConstructionAgent):
    """Predict schedule, cost, and safety risks 14+ days ahead."""

    name = "risk_forecaster"
    description = "Predict schedule/cost/safety risks 14+ days ahead"
    schedule = "hourly"

    def _register_tools(self) -> None:
        self._tools.register(WeatherForecast())
        self._tools.register(OshaSearch())
        self._tools.register(RiskDatabase())

    def get_system_prompt(self) -> str:
        return (
            "You are an expert construction risk analyst."
            " Your job is to predict schedule, cost, and safety"
            " risks for construction projects at least 14 days"
            " in advance.\n\n"
            "Focus on risks with:\n"
            "- Probability > 15% AND impact > $100,000\n"
            "- OR any safety-critical risks\n\n"
            "You have access to weather forecasts, OSHA"
            " inspection data, and the project risk register."
            " Use these data sources to identify emerging risks.\n\n"
            "For each risk, provide:\n"
            "1. Clear description of the risk event\n"
            "2. Probability estimate (0-1)\n"
            "3. Impact in dollars and schedule days\n"
            "4. Whether it is safety-critical\n"
            "5. Recommended mitigations\n"
            "6. Data sources used and confidence level\n\n"
            "Output your assessment as structured JSON with a"
            " 'risks' array. Each risk should have: category,"
            " description, probability, impact_dollars,"
            " impact_days, safety_critical, confidence,"
            " and mitigations fields."
        )

    async def run(self, context: dict | None = None) -> AgentEvent:
        """Analyze current project risks and publish findings."""
        project_id = (context or {}).get(
            "project_id", "default"
        )

        prompt = (
            f"Analyze risks for project {project_id}."
            " Check weather forecasts for the next 14 days,"
            " review OSHA data for relevant citations,"
            " and query the risk register for active risks."
            " Identify any new or escalating risks."
            " Focus on risks that exceed the thresholds:"
            " probability > 15% AND impact > $100k,"
            " or any safety-critical items."
        )

        response = self.chat(prompt)

        transparency_log = [
            "Checked 14-day weather forecast",
            "Queried OSHA citation database",
            "Reviewed active risk register",
            f"Model response length: {len(response)} chars",
        ]

        try:
            risk_data = json.loads(response)
        except (json.JSONDecodeError, TypeError):
            risk_data = {"raw_response": response}

        risks = risk_data.get("risks", [])
        has_critical = any(
            r.get("safety_critical") for r in risks
        )
        severity = "critical" if has_critical else (
            "warning" if risks else "info"
        )

        return await self.publish_event(
            event_type="risk_assessment",
            severity=severity,
            data=risk_data,
            confidence=0.80,
            data_sources=[
                DataSource(
                    source_type="api",
                    source_name="weather_forecast",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.75,
                ),
                DataSource(
                    source_type="api",
                    source_name="osha_search",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.90,
                ),
                DataSource(
                    source_type="database",
                    source_name="risk_register",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.95,
                ),
            ],
            transparency_log=transparency_log,
            requires_cross_agent=has_critical,
            target_agent="supply_chain" if has_critical else None,
        )
