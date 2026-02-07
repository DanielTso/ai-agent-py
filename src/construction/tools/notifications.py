"""Notification tool for SMS and email alerts."""

import json
from datetime import UTC, datetime

from ai_agent.tools import Tool


class SendNotification(Tool):
    """Send SMS or email notifications for critical alerts."""

    name = "send_notification"
    description = (
        "Send SMS or email notifications for critical"
        " alerts and escalations."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "method": {
                    "type": "string",
                    "enum": ["sms", "email"],
                    "description": "Notification method",
                },
                "recipient": {
                    "type": "string",
                    "description": (
                        "Phone number for SMS or email address"
                    ),
                },
                "message": {
                    "type": "string",
                    "description": "Notification message body",
                },
                "priority": {
                    "type": "string",
                    "enum": [
                        "normal",
                        "urgent",
                        "critical",
                    ],
                    "description": "Priority level",
                    "default": "normal",
                },
            },
            "required": ["method", "recipient", "message"],
        }

    def execute(self, **kwargs) -> str:
        method = kwargs["method"]
        try:
            if method == "sms":
                return self._send_sms(**kwargs)
            elif method == "email":
                return self._send_email(**kwargs)
            else:
                return f"Error: Unknown method '{method}'"
        except Exception as exc:
            return f"Error: {exc}"

    def _send_sms(self, **kwargs) -> str:
        recipient = kwargs["recipient"]
        message = kwargs["message"]
        priority = kwargs.get("priority", "normal")

        # SMS has 160 character limit
        truncated = len(message) > 160
        sms_body = message[:160] if truncated else message

        response = {
            "status": "sent",
            "method": "sms",
            "recipient": recipient,
            "message_length": len(sms_body),
            "truncated": truncated,
            "priority": priority,
            "timestamp": datetime.now(UTC).isoformat(),
            "note": (
                "Mock — production would use Twilio client"
            ),
        }
        return json.dumps(response, indent=2)

    def _send_email(self, **kwargs) -> str:
        recipient = kwargs["recipient"]
        message = kwargs["message"]
        priority = kwargs.get("priority", "normal")

        response = {
            "status": "sent",
            "method": "email",
            "recipient": recipient,
            "message_length": len(message),
            "priority": priority,
            "timestamp": datetime.now(UTC).isoformat(),
            "note": (
                "Mock — production would use SMTP/SES"
            ),
        }
        return json.dumps(response, indent=2)
