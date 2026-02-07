"""Twilio SMS client for escalation notifications."""

import logging

from twilio.rest import Client as TwilioRestClient

logger = logging.getLogger(__name__)


class TwilioClient:
    """SMS client using the Twilio SDK."""

    def __init__(
        self,
        account_sid: str,
        auth_token: str,
        from_number: str,
    ):
        self.from_number = from_number
        self._client = TwilioRestClient(account_sid, auth_token)

    def send_sms(self, to: str, body: str) -> dict:
        """Send an SMS message.

        Returns a dict with message sid and status.
        """
        message = self._client.messages.create(
            to=to,
            from_=self.from_number,
            body=body,
        )
        logger.info("SMS sent to %s: sid=%s", to, message.sid)
        return {"sid": message.sid, "status": message.status}

    def send_escalation_sms(
        self,
        to: str,
        body: str,
        callback_url: str | None = None,
    ) -> dict:
        """Send an escalation SMS with optional status callback.

        Returns a dict with message sid and status.
        """
        kwargs: dict = {
            "to": to,
            "from_": self.from_number,
            "body": body,
        }
        if callback_url:
            kwargs["status_callback"] = callback_url
        message = self._client.messages.create(**kwargs)
        logger.info(
            "Escalation SMS sent to %s: sid=%s", to, message.sid
        )
        return {"sid": message.sid, "status": message.status}
