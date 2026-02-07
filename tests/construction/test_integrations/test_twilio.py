"""Tests for TwilioClient."""

from unittest.mock import MagicMock, patch

import pytest

from construction.integrations.twilio_ import TwilioClient


@pytest.fixture
def mock_twilio():
    with patch(
        "construction.integrations.twilio_.TwilioRestClient"
    ) as mock_cls:
        mock_rest = MagicMock()
        mock_cls.return_value = mock_rest
        yield mock_rest


@pytest.fixture
def client(mock_twilio):
    return TwilioClient(
        account_sid="AC_test",
        auth_token="test_token",
        from_number="+15551234567",
    )


def test_init(client):
    assert client.from_number == "+15551234567"


def test_send_sms(client, mock_twilio):
    mock_msg = MagicMock()
    mock_msg.sid = "SM12345"
    mock_msg.status = "queued"
    mock_twilio.messages.create.return_value = mock_msg

    result = client.send_sms("+15559876543", "Hello")
    assert result == {"sid": "SM12345", "status": "queued"}
    mock_twilio.messages.create.assert_called_once_with(
        to="+15559876543",
        from_="+15551234567",
        body="Hello",
    )


def test_send_escalation_sms(client, mock_twilio):
    mock_msg = MagicMock()
    mock_msg.sid = "SM67890"
    mock_msg.status = "queued"
    mock_twilio.messages.create.return_value = mock_msg

    result = client.send_escalation_sms(
        "+15559876543",
        "URGENT: Risk detected",
        callback_url="https://example.com/callback",
    )
    assert result == {"sid": "SM67890", "status": "queued"}
    mock_twilio.messages.create.assert_called_once_with(
        to="+15559876543",
        from_="+15551234567",
        body="URGENT: Risk detected",
        status_callback="https://example.com/callback",
    )


def test_send_escalation_sms_no_callback(client, mock_twilio):
    mock_msg = MagicMock()
    mock_msg.sid = "SM11111"
    mock_msg.status = "queued"
    mock_twilio.messages.create.return_value = mock_msg

    result = client.send_escalation_sms("+15559876543", "Alert")
    assert result == {"sid": "SM11111", "status": "queued"}
    mock_twilio.messages.create.assert_called_once_with(
        to="+15559876543",
        from_="+15551234567",
        body="Alert",
    )
