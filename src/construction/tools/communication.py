"""Communication drafting tool for reports, RFIs, and notices."""

import json
import uuid
from datetime import UTC, datetime

from ai_agent.tools import Tool


class DraftCommunication(Tool):
    """Draft owner reports, RFI responses, and sub notices."""

    name = "draft_communication"
    description = (
        "Draft owner reports, RFI responses, and"
        " subcontractor notices with appropriate tone."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "owner_report",
                        "rfi_response",
                        "sub_notice",
                        "owner_update",
                    ],
                    "description": "The type of communication to draft",
                },
                "project_id": {
                    "type": "string",
                    "description": "The project ID",
                },
                "context": {
                    "type": "object",
                    "description": (
                        "Context for the draft (topic,"
                        " data, recipients, etc.)"
                    ),
                },
                "tone": {
                    "type": "string",
                    "enum": [
                        "business",
                        "technical",
                        "contractual",
                    ],
                    "description": (
                        "Tone of the communication"
                    ),
                },
            },
            "required": ["action", "project_id", "context"],
        }

    def execute(self, **kwargs) -> str:
        action = kwargs["action"]
        project_id = kwargs["project_id"]
        context = kwargs.get("context", {})
        tone = kwargs.get("tone", "business")
        try:
            if action == "owner_report":
                return self._owner_report(
                    project_id, context, tone
                )
            elif action == "rfi_response":
                return self._rfi_response(
                    project_id, context
                )
            elif action == "sub_notice":
                return self._sub_notice(
                    project_id, context
                )
            elif action == "owner_update":
                return self._owner_update(
                    project_id, context
                )
            else:
                return f"Error: unknown action '{action}'"
        except Exception as exc:
            return f"Error drafting communication: {exc}"

    def _owner_report(
        self,
        project_id: str,
        context: dict,
        tone: str,
    ) -> str:
        period = context.get("period", "2025-Q3")
        return json.dumps(
            {
                "id": str(uuid.uuid4())[:8],
                "report_type": "owner_report",
                "title": (
                    f"Monthly Owner Report — {period}"
                ),
                "body": (
                    f"Project {project_id} — {period}\n\n"
                    "Executive Summary:\n"
                    "The project is tracking 2.67% over"
                    " budget with CPI at 0.987. Schedule"
                    " performance (SPI 0.925) reflects a"
                    " 7-day delay in structural steel"
                    " delivery. Two pending change orders"
                    " totaling $280,000 await approval.\n\n"
                    "Key Accomplishments:\n"
                    "- Completed Level 3 rough-in for"
                    " electrical and mechanical\n"
                    "- Fire suppression CO-2025-001 approved"
                    " and work underway\n"
                    "- LEED documentation 85% complete\n\n"
                    "Concerns:\n"
                    "- Structural steel delivery delayed"
                    " 7 days (port congestion)\n"
                    "- Plumbing crew productivity at 85%"
                    " — below target\n\n"
                    "Next Period Focus:\n"
                    "- Expedite steel delivery alternatives\n"
                    "- Onboard additional plumbing crew\n"
                    "- Submit pending change orders for review"
                ),
                "tone": tone,
                "status": "draft",
                "generated_at": datetime.now(UTC).isoformat(),
                "note": "Mock draft — AI will generate from live data",
            },
            indent=2,
        )

    def _rfi_response(
        self, project_id: str, context: dict
    ) -> str:
        rfi_number = context.get(
            "rfi_number", "RFI-2025-042"
        )
        question = context.get(
            "question",
            "Clarify routing for conduit run C-14 at Level 3",
        )
        return json.dumps(
            {
                "id": str(uuid.uuid4())[:8],
                "rfi_number": rfi_number,
                "question": question,
                "response": (
                    f"Re: {rfi_number}\n\n"
                    "Per review of drawing E-301 Rev C and"
                    " coordination with the mechanical team,"
                    " conduit run C-14 shall be routed above"
                    " the mechanical duct at elevation 12'-6\""
                    " to maintain required clearances per"
                    " NEC 300.11.\n\n"
                    "Reference documents:\n"
                    "- Drawing E-301 Rev C\n"
                    "- Mechanical coordination drawing M-301\n"
                    "- NEC 2023, Section 300.11\n\n"
                    "Please confirm acceptance within 5"
                    " business days."
                ),
                "references": [
                    "Drawing E-301 Rev C",
                    "Drawing M-301",
                    "NEC 2023 Section 300.11",
                ],
                "status": "draft",
                "generated_at": datetime.now(UTC).isoformat(),
                "note": "Mock draft",
            },
            indent=2,
        )

    def _sub_notice(
        self, project_id: str, context: dict
    ) -> str:
        notice_type = context.get("notice_type", "delay")
        recipient = context.get(
            "recipient", "Pacific Steel Corp"
        )
        return json.dumps(
            {
                "id": str(uuid.uuid4())[:8],
                "notice_type": notice_type,
                "recipient": recipient,
                "subject": (
                    f"Notice of {notice_type.title()}"
                    f" — Project {project_id}"
                ),
                "body": (
                    f"Dear {recipient},\n\n"
                    "This letter serves as formal notice"
                    " pursuant to Section 8.3 of the"
                    " Subcontract Agreement dated"
                    " January 15, 2025.\n\n"
                    "You are hereby notified that your"
                    " delivery of structural steel per"
                    " Purchase Order PO-2025-0147 is"
                    " currently 7 calendar days behind"
                    " the contractual delivery date.\n\n"
                    "Per Section 8.3.2, you are required"
                    " to submit a recovery plan within"
                    " 5 business days of receipt of"
                    " this notice.\n\n"
                    "Failure to comply may result in"
                    " liquidated damages as outlined in"
                    " Section 12.1 of the Agreement.\n\n"
                    "Regards,\n"
                    "Project Management Team"
                ),
                "contract_clause": "Section 8.3",
                "status": "draft",
                "generated_at": datetime.now(UTC).isoformat(),
                "note": "Mock draft",
            },
            indent=2,
        )

    def _owner_update(
        self, project_id: str, context: dict
    ) -> str:
        period = context.get("period", "Week of 2025-06-30")
        return json.dumps(
            {
                "id": str(uuid.uuid4())[:8],
                "period": period,
                "executive_summary": (
                    f"Project {project_id} is 42% complete"
                    " overall. CPI 0.987 and SPI 0.925."
                    " One critical path delay on structural"
                    " steel (7 days). Two change orders"
                    " pending ($280K combined). Safety"
                    " record: 45 days without incident."
                ),
                "key_metrics": {
                    "pct_complete": 42.0,
                    "cpi": 0.987,
                    "spi": 0.925,
                    "budget_variance_pct": 2.67,
                    "safety_incident_free_days": 45,
                    "rfi_open": 8,
                    "change_orders_pending": 2,
                },
                "concerns": [
                    "Structural steel 7-day delay",
                    "Plumbing productivity below target (85%)",
                    "2 worker certifications expiring within 30 days",
                ],
                "next_steps": [
                    "Evaluate domestic steel alternatives",
                    "Add plumbing crew from labor pool",
                    "Schedule certification renewals",
                    "Submit CO-002 and CO-003 for approval",
                ],
                "generated_at": datetime.now(UTC).isoformat(),
                "note": "Mock data",
            },
            indent=2,
        )
