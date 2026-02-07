"""Claims query tool for events, delay analysis, and notices."""

import json
from datetime import date, timedelta

from ai_agent.tools import Tool


class ClaimsQuery(Tool):
    """Query claims and dispute data."""

    name = "claims_query"
    description = (
        "Query claims data including events, delay analysis,"
        " notice tracking, and causation chains."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "events",
                        "delay_analysis",
                        "notices",
                        "causation_chain",
                    ],
                    "description": "The claims action.",
                },
                "project_id": {
                    "type": "string",
                    "description": "The project identifier.",
                },
                "event_id": {
                    "type": "string",
                    "description": "Specific event ID to query.",
                },
            },
            "required": ["action", "project_id"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        project_id = kwargs["project_id"]
        try:
            if action == "events":
                return self._events(project_id)
            elif action == "delay_analysis":
                return self._delay_analysis(project_id)
            elif action == "notices":
                return self._notices(project_id)
            elif action == "causation_chain":
                return self._causation_chain(
                    project_id, kwargs.get("event_id")
                )
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _events(self, project_id: str) -> str:
        today = date.today()
        events = [
            {
                "id": "CLM-001",
                "event_type": "delay",
                "description": (
                    "Owner-directed redesign of lobby caused"
                    " 14-day delay to interior finishes"
                ),
                "event_date": (
                    today - timedelta(days=30)
                ).isoformat(),
                "causation_chain": [
                    "Owner RFI #42",
                    "Arch revision ASK-Rev3",
                    "GC delay to finishes",
                ],
                "notice_required": True,
                "notice_deadline": (
                    today - timedelta(days=23)
                ).isoformat(),
                "notice_sent": True,
                "evidence": [
                    "RFI-042.pdf",
                    "ASK-Rev3.pdf",
                    "daily_log_2025-01-05.pdf",
                ],
                "responsible_party": "Owner",
            },
            {
                "id": "CLM-002",
                "event_type": "differing_condition",
                "description": (
                    "Unexpected rock encountered during"
                    " foundation excavation Zone C"
                ),
                "event_date": (
                    today - timedelta(days=10)
                ).isoformat(),
                "causation_chain": [
                    "Geotech report did not indicate rock",
                    "Additional blasting required",
                ],
                "notice_required": True,
                "notice_deadline": (
                    today + timedelta(days=4)
                ).isoformat(),
                "notice_sent": False,
                "evidence": [
                    "geotech_report_v2.pdf",
                    "site_photos_2025-01-25.zip",
                ],
                "responsible_party": None,
            },
            {
                "id": "CLM-003",
                "event_type": "force_majeure",
                "description": (
                    "Hurricane warning forced 3-day site shutdown"
                ),
                "event_date": (
                    today - timedelta(days=60)
                ).isoformat(),
                "causation_chain": [
                    "NWS hurricane warning",
                    "Site evacuation order",
                    "3-day shutdown",
                ],
                "notice_required": True,
                "notice_deadline": (
                    today - timedelta(days=53)
                ).isoformat(),
                "notice_sent": True,
                "evidence": [
                    "NWS_bulletin.pdf",
                    "daily_logs_shutdown.pdf",
                ],
                "responsible_party": "Force Majeure",
            },
        ]
        return json.dumps(
            {
                "project_id": project_id,
                "claim_events": events,
                "note": "Mock data",
            },
            indent=2,
        )

    def _delay_analysis(self, project_id: str) -> str:
        analyses = [
            {
                "analysis_type": "TIA",
                "affected_activities": [
                    "Interior Finishes — Lobby",
                    "Millwork Install",
                    "Final Paint — Lobby",
                ],
                "critical_delay_days": 14.0,
                "concurrent_delay_days": 3.0,
                "responsible_party": "Owner",
                "narrative": (
                    "Time Impact Analysis shows owner-directed"
                    " lobby redesign added 14 calendar days to"
                    " the critical path. 3 days concurrent with"
                    " GC material procurement delay."
                ),
            },
            {
                "analysis_type": "windows",
                "affected_activities": [
                    "Foundation — Zone C",
                    "SOG — Zone C",
                ],
                "critical_delay_days": 8.0,
                "concurrent_delay_days": 0.0,
                "responsible_party": None,
                "narrative": (
                    "Windows analysis for differing site condition."
                    " Rock removal added 8 working days. No"
                    " concurrent delays identified."
                ),
            },
        ]
        return json.dumps(
            {
                "project_id": project_id,
                "delay_analyses": analyses,
                "note": "Mock data",
            },
            indent=2,
        )

    def _notices(self, project_id: str) -> str:
        today = date.today()
        notices = [
            {
                "id": "NTC-001",
                "notice_type": "delay_claim",
                "contract_clause": "Section 8.3.1",
                "deadline": (
                    today - timedelta(days=23)
                ).isoformat(),
                "sent_date": (
                    today - timedelta(days=25)
                ).isoformat(),
                "recipient": "Owner Representative",
                "status": "acknowledged",
            },
            {
                "id": "NTC-002",
                "notice_type": "differing_condition",
                "contract_clause": "Section 4.3.4",
                "deadline": (
                    today + timedelta(days=4)
                ).isoformat(),
                "sent_date": None,
                "recipient": "Owner Representative",
                "status": "pending",
            },
            {
                "id": "NTC-003",
                "notice_type": "change_directive",
                "contract_clause": "Section 7.2.1",
                "deadline": (
                    today + timedelta(days=1)
                ).isoformat(),
                "sent_date": None,
                "recipient": "Architect",
                "status": "pending",
            },
        ]
        return json.dumps(
            {
                "project_id": project_id,
                "notices": notices,
                "note": "Mock data",
            },
            indent=2,
        )

    def _causation_chain(
        self, project_id: str, event_id: str | None
    ) -> str:
        chain = {
            "events": [
                "Owner RFI #42 — lobby redesign request",
                "Architect revision ASK-Rev3 issued",
                "GC re-sequence interior finishes",
                "14-day critical path delay",
            ],
            "links": [
                {
                    "from": "Owner RFI #42",
                    "to": "Arch revision ASK-Rev3",
                    "type": "caused",
                },
                {
                    "from": "Arch revision ASK-Rev3",
                    "to": "GC re-sequence",
                    "type": "necessitated",
                },
                {
                    "from": "GC re-sequence",
                    "to": "14-day delay",
                    "type": "resulted_in",
                },
            ],
            "root_cause": "Owner-directed design change",
            "contributing_factors": [
                "Late RFI response (12 days vs 7-day SLA)",
                "No pre-purchased millwork materials",
            ],
        }
        return json.dumps(
            {
                "project_id": project_id,
                "event_id": event_id or "CLM-001",
                "causation_chain": chain,
                "note": "Mock data",
            },
            indent=2,
        )
