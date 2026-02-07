"""Tests for the SendNotification tool."""

import json

from construction.tools.notifications import SendNotification


def test_notification_schema():
    tool = SendNotification()
    schema = tool.get_input_schema()
    assert schema["type"] == "object"
    assert "method" in schema["properties"]
    assert "recipient" in schema["properties"]
    assert "message" in schema["properties"]
    assert set(schema["required"]) == {
        "method", "recipient", "message",
    }


def test_notification_to_api_format():
    tool = SendNotification()
    fmt = tool.to_api_format()
    assert fmt["name"] == "send_notification"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_notification_sms_send():
    tool = SendNotification()
    result = tool.execute(
        method="sms",
        recipient="+15551234567",
        message="Critical alert: safety issue detected",
    )
    data = json.loads(result)
    assert data["status"] == "sent"
    assert data["method"] == "sms"
    assert data["recipient"] == "+15551234567"
    assert data["truncated"] is False


def test_notification_sms_truncation():
    tool = SendNotification()
    long_message = "A" * 200
    result = tool.execute(
        method="sms",
        recipient="+15551234567",
        message=long_message,
    )
    data = json.loads(result)
    assert data["truncated"] is True
    assert data["message_length"] == 160


def test_notification_email_send():
    tool = SendNotification()
    result = tool.execute(
        method="email",
        recipient="pm@example.com",
        message="Daily brief: 3 threats identified",
        priority="normal",
    )
    data = json.loads(result)
    assert data["status"] == "sent"
    assert data["method"] == "email"
    assert data["recipient"] == "pm@example.com"
    assert data["priority"] == "normal"


def test_notification_priority_handling():
    tool = SendNotification()
    for priority in ("normal", "urgent", "critical"):
        result = tool.execute(
            method="sms",
            recipient="+15551234567",
            message="Test message",
            priority=priority,
        )
        data = json.loads(result)
        assert data["priority"] == priority


def test_notification_unknown_method():
    tool = SendNotification()
    result = tool.execute(
        method="fax",
        recipient="123",
        message="Test",
    )
    assert result.startswith("Error:")
