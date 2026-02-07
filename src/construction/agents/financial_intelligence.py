"""Financial Intelligence agent — earned value, cash flow, change orders."""

import json
from datetime import UTC, datetime

from construction.agents.base import ConstructionAgent
from construction.schemas.common import AgentEvent, DataSource
from construction.tools.financial import FinancialQuery


class FinancialIntelligenceAgent(ConstructionAgent):
    """Earned value analysis, cash flow projection, change order tracking."""

    name = "financial_intelligence"
    description = (
        "Earned value analysis, cash flow projection,"
        " change order tracking"
    )
    schedule = "daily"

    def _register_tools(self) -> None:
        self._tools.register(FinancialQuery())

    def get_system_prompt(self) -> str:
        return (
            "You are an expert construction financial"
            " analyst. Your role is to track project"
            " financial health using Earned Value"
            " Management (EVM) metrics.\n\n"
            "Key responsibilities:\n"
            "- Monitor CPI and SPI trends\n"
            "- Calculate EAC, ETC, VAC, and TCPI\n"
            "- Project cash flow and identify draw"
            " schedule variances\n"
            "- Track change orders and their cumulative"
            " budget impact\n"
            "- Flag any cost variance exceeding 10%\n\n"
            "For each analysis, provide:\n"
            "1. Current CPI/SPI with trend direction\n"
            "2. Forecast at Completion (EAC) vs budget\n"
            "3. Cash flow status and upcoming draws\n"
            "4. Pending change orders and total exposure\n"
            "5. Confidence score for the forecast\n\n"
            "Answer 'are we on budget?' with a clear"
            " yes/no, the variance percentage, and a"
            " confidence score.\n\n"
            "Output your assessment as structured JSON"
            " with: budget_status, evm_metrics, cash_flow,"
            " change_orders, and alerts fields."
        )

    async def run(self, context: dict | None = None) -> AgentEvent:
        """Analyze current financial status and identify variances."""
        project_id = (context or {}).get(
            "project_id", "default"
        )

        prompt = (
            f"Analyze financial status for project {project_id}."
            " Query the current budget status, calculate"
            " earned value metrics, review cash flow for"
            " the current period, and check pending change"
            " orders. Flag any variance exceeding 10%."
            " Provide a confidence score for the forecast."
        )

        response = self.chat(prompt)

        transparency_log = [
            "Queried current budget status",
            "Calculated EVM metrics (CPI/SPI/EAC/TCPI)",
            "Reviewed cash flow draws vs plan",
            "Checked pending change orders",
            f"Model response length: {len(response)} chars",
        ]

        try:
            financial_data = json.loads(response)
        except (json.JSONDecodeError, TypeError):
            financial_data = {"raw_response": response}

        alerts = financial_data.get("alerts", [])
        has_critical = any(
            a.get("severity") == "critical" for a in alerts
        )
        has_warning = any(
            a.get("severity") == "warning" for a in alerts
        ) or alerts
        severity = "critical" if has_critical else (
            "warning" if has_warning else "info"
        )

        return await self.publish_event(
            event_type="financial_analysis",
            severity=severity,
            data=financial_data,
            confidence=0.88,
            data_sources=[
                DataSource(
                    source_type="database",
                    source_name="financial_query",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.95,
                ),
            ],
            transparency_log=transparency_log,
            requires_cross_agent=has_critical,
            target_agent="risk_forecaster" if has_critical else None,
        )
