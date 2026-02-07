"""Safety metrics tool for TRIR, DART, and EMR calculations."""

import json

from ai_agent.tools import Tool


class SafetyMetrics(Tool):
    """Calculate construction safety metrics."""

    name = "safety_metrics"
    description = (
        "Calculate safety metrics including TRIR,"
        " DART rate, and Experience Modification Rate."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "calculate_trir",
                        "calculate_dart",
                        "calculate_emr",
                    ],
                    "description": "The safety metric to calculate.",
                },
                "project_id": {
                    "type": "string",
                    "description": "The project identifier.",
                },
                "total_recordable_cases": {
                    "type": "integer",
                    "description": "Total recordable cases.",
                },
                "dart_cases": {
                    "type": "integer",
                    "description": (
                        "Days away/restricted/transfer cases."
                    ),
                },
                "hours_worked": {
                    "type": "number",
                    "description": "Total hours worked.",
                },
            },
            "required": ["action"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        try:
            if action == "calculate_trir":
                return self._calculate_trir(
                    kwargs.get("total_recordable_cases", 2),
                    kwargs.get("hours_worked", 185000),
                )
            elif action == "calculate_dart":
                return self._calculate_dart(
                    kwargs.get("dart_cases", 1),
                    kwargs.get("hours_worked", 185000),
                )
            elif action == "calculate_emr":
                return self._calculate_emr(
                    kwargs.get("project_id", "default")
                )
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _calculate_trir(
        self, recordable_cases: int, hours_worked: float
    ) -> str:
        if hours_worked <= 0:
            return json.dumps(
                {"error": "Hours worked must be positive"}
            )
        trir = (recordable_cases * 200000) / hours_worked
        benchmark = 2.5
        return json.dumps(
            {
                "metric": "TRIR",
                "formula": (
                    "(recordable_cases * 200,000)"
                    " / hours_worked"
                ),
                "recordable_cases": recordable_cases,
                "hours_worked": hours_worked,
                "trir": round(trir, 2),
                "industry_benchmark": benchmark,
                "status": (
                    "below_benchmark"
                    if trir < benchmark
                    else "above_benchmark"
                ),
                "note": "Mock data",
            },
            indent=2,
        )

    def _calculate_dart(
        self, dart_cases: int, hours_worked: float
    ) -> str:
        if hours_worked <= 0:
            return json.dumps(
                {"error": "Hours worked must be positive"}
            )
        dart = (dart_cases * 200000) / hours_worked
        benchmark = 1.5
        return json.dumps(
            {
                "metric": "DART",
                "formula": (
                    "(dart_cases * 200,000) / hours_worked"
                ),
                "dart_cases": dart_cases,
                "hours_worked": hours_worked,
                "dart_rate": round(dart, 2),
                "industry_benchmark": benchmark,
                "status": (
                    "below_benchmark"
                    if dart < benchmark
                    else "above_benchmark"
                ),
                "note": "Mock data",
            },
            indent=2,
        )

    def _calculate_emr(self, project_id: str) -> str:
        return json.dumps(
            {
                "metric": "EMR",
                "project_id": project_id,
                "emr": 0.87,
                "industry_average": 1.0,
                "interpretation": (
                    "EMR of 0.87 indicates better-than-average"
                    " safety performance. Workers comp premiums"
                    " are 13% below industry average."
                ),
                "components": {
                    "actual_losses": 125000.00,
                    "expected_losses": 143678.00,
                    "ballast_value": 28000.00,
                },
                "note": "Mock data",
            },
            indent=2,
        )
