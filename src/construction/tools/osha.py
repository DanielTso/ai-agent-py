"""OSHA inspection and citation search tool."""

import json
from datetime import UTC, datetime

from ai_agent.tools import Tool


class OshaSearch(Tool):
    """Search OSHA inspection and citation data."""

    name = "osha_search"
    description = (
        "Search OSHA inspection and citation data for an"
        " establishment or area. Returns inspection details"
        " and violation information."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "establishment": {
                    "type": "string",
                    "description": "Name of the establishment to search",
                },
                "state": {
                    "type": "string",
                    "description": "Two-letter state code (e.g. 'TX')",
                },
                "sic_code": {
                    "type": "string",
                    "description": "SIC code to filter by (e.g. '1542')",
                },
                "date_from": {
                    "type": "string",
                    "description": "Start date filter (YYYY-MM-DD)",
                },
                "date_to": {
                    "type": "string",
                    "description": "End date filter (YYYY-MM-DD)",
                },
            },
        }

    def execute(self, **kwargs) -> str:
        try:
            return self._mock_search(**kwargs)
        except Exception as exc:
            return f"Error searching OSHA data: {exc}"

    def _mock_search(self, **kwargs) -> str:
        establishment = kwargs.get("establishment", "")
        state = kwargs.get("state", "")

        inspections = [
            {
                "inspection_number": "1654321",
                "establishment": establishment or "ABC Construction LLC",
                "state": state or "TX",
                "open_date": "2025-10-15",
                "close_date": "2025-11-20",
                "inspection_type": "Planned",
                "scope": "Complete",
                "violations": [
                    {
                        "citation": "01001",
                        "standard": "1926.0501",
                        "description": (
                            "Fall protection — failure to provide"
                            " guardrail systems on open-sided"
                            " floors above 6 feet"
                        ),
                        "type": "Serious",
                        "penalty": 15625.0,
                        "abatement_date": "2025-12-15",
                    },
                    {
                        "citation": "01002",
                        "standard": "1926.1053",
                        "description": (
                            "Ladders — portable ladder not"
                            " extending 3 feet above upper"
                            " landing surface"
                        ),
                        "type": "Other-than-Serious",
                        "penalty": 1036.0,
                        "abatement_date": "2025-12-01",
                    },
                ],
            },
            {
                "inspection_number": "1654400",
                "establishment": establishment or "ABC Construction LLC",
                "state": state or "TX",
                "open_date": "2025-08-01",
                "close_date": "2025-09-10",
                "inspection_type": "Referral",
                "scope": "Partial",
                "violations": [
                    {
                        "citation": "01001",
                        "standard": "1926.0651",
                        "description": (
                            "Excavations — failure to provide"
                            " cave-in protection for excavation"
                            " deeper than 5 feet"
                        ),
                        "type": "Willful",
                        "penalty": 156259.0,
                        "abatement_date": "2025-09-30",
                    },
                ],
            },
        ]

        result = {
            "inspections": inspections,
            "total_results": len(inspections),
            "query": {
                "establishment": establishment,
                "state": state,
                "sic_code": kwargs.get("sic_code"),
                "date_from": kwargs.get("date_from"),
                "date_to": kwargs.get("date_to"),
            },
            "retrieved_at": datetime.now(UTC).isoformat(),
            "note": "Mock data — production would call OSHA enforcement API",
        }
        return json.dumps(result, indent=2)
