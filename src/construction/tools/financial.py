"""Financial query tool for budget, EVM, and cash flow."""

import json
from datetime import date

from ai_agent.tools import Tool


class FinancialQuery(Tool):
    """Query project financial data including budget, EVM, and cash flow."""

    name = "financial_query"
    description = (
        "Query project financial data including budget,"
        " earned value, and cash flow."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "budget_status",
                        "earned_value",
                        "cash_flow",
                        "change_orders",
                    ],
                    "description": "The financial query to perform",
                },
                "project_id": {
                    "type": "string",
                    "description": "The project ID",
                },
                "period": {
                    "type": "string",
                    "description": (
                        "Time period for the query (e.g. 2025-Q1)"
                    ),
                },
                "data": {
                    "type": "object",
                    "description": (
                        "Additional data for the query"
                    ),
                },
            },
            "required": ["action", "project_id"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        project_id = kwargs["project_id"]
        try:
            if action == "budget_status":
                return self._budget_status(project_id)
            elif action == "earned_value":
                return self._earned_value(project_id)
            elif action == "cash_flow":
                return self._cash_flow(
                    project_id, kwargs.get("period")
                )
            elif action == "change_orders":
                return self._change_orders(project_id)
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error in financial query: {exc}"

    def _budget_status(self, project_id: str) -> str:
        return json.dumps(
            {
                "project_id": project_id,
                "total_budget": 45_000_000.00,
                "spent_to_date": 18_750_000.00,
                "committed": 12_300_000.00,
                "forecast_at_completion": 46_200_000.00,
                "contingency_remaining": 2_250_000.00,
                "variance_pct": 2.67,
                "note": "Mock data",
            },
            indent=2,
        )

    def _earned_value(self, project_id: str) -> str:
        today = date.today()
        return json.dumps(
            {
                "snapshot_date": today.isoformat(),
                "bcws": 20_000_000.00,
                "bcwp": 18_500_000.00,
                "acwp": 18_750_000.00,
                "cpi": 0.987,
                "spi": 0.925,
                "eac": 45_593_718.34,
                "etc": 26_843_718.34,
                "vac": -593_718.34,
                "tcpi": 1.010,
                "note": "Mock data",
            },
            indent=2,
        )

    def _cash_flow(
        self, project_id: str, period: str | None
    ) -> str:
        periods = [
            {
                "period": "2025-Q1",
                "planned_draw": 5_000_000.00,
                "actual_draw": 4_800_000.00,
                "cumulative_planned": 5_000_000.00,
                "cumulative_actual": 4_800_000.00,
            },
            {
                "period": "2025-Q2",
                "planned_draw": 7_500_000.00,
                "actual_draw": 7_200_000.00,
                "cumulative_planned": 12_500_000.00,
                "cumulative_actual": 12_000_000.00,
            },
            {
                "period": "2025-Q3",
                "planned_draw": 8_000_000.00,
                "actual_draw": 6_750_000.00,
                "cumulative_planned": 20_500_000.00,
                "cumulative_actual": 18_750_000.00,
            },
        ]
        if period:
            periods = [
                p for p in periods if p["period"] == period
            ]
        return json.dumps(
            {"cash_flow": periods, "note": "Mock data"},
            indent=2,
        )

    def _change_orders(self, project_id: str) -> str:
        today = date.today()
        orders = [
            {
                "id": "CO-001",
                "co_number": "CO-2025-001",
                "description": (
                    "Added fire suppression to data center wing"
                ),
                "cost_impact": 320_000.00,
                "schedule_impact_days": 12,
                "status": "approved",
                "submitted_date": "2025-03-15",
                "approved_date": "2025-04-01",
            },
            {
                "id": "CO-002",
                "co_number": "CO-2025-002",
                "description": (
                    "Soil remediation — unexpected contamination"
                ),
                "cost_impact": 185_000.00,
                "schedule_impact_days": 8,
                "status": "pending",
                "submitted_date": today.isoformat(),
                "approved_date": None,
            },
            {
                "id": "CO-003",
                "co_number": "CO-2025-003",
                "description": (
                    "Owner-requested lobby redesign"
                ),
                "cost_impact": 95_000.00,
                "schedule_impact_days": 5,
                "status": "pending",
                "submitted_date": today.isoformat(),
                "approved_date": None,
            },
        ]
        return json.dumps(
            {"change_orders": orders, "note": "Mock data"},
            indent=2,
        )
