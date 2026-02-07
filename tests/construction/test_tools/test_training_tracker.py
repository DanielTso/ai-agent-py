"""Tests for the training tracker tool."""

import json

from construction.tools.training_tracker import TrainingTracker


def test_schema():
    """Tool schema has expected properties."""
    tool = TrainingTracker()
    assert tool.name == "training_tracker"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "project_id" in props
    assert "worker_id" in props
    assert "days_ahead" in props
    assert set(props["action"]["enum"]) == {
        "check_certifications",
        "expiring_soon",
        "training_gaps",
    }


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = TrainingTracker()
    fmt = tool.to_api_format()
    assert fmt["name"] == "training_tracker"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_check_certifications():
    """Certifications returns all training records."""
    tool = TrainingTracker()
    result = tool.execute(
        action="check_certifications"
    )
    data = json.loads(result)
    assert "certifications" in data
    certs = data["certifications"]
    assert len(certs) == 5
    statuses = {c["status"] for c in certs}
    assert "valid" in statuses
    assert "expiring" in statuses
    assert "expired" in statuses


def test_check_certifications_filter():
    """Certifications can be filtered by worker."""
    tool = TrainingTracker()
    result = tool.execute(
        action="check_certifications",
        worker_id="WRK-101",
    )
    data = json.loads(result)
    certs = data["certifications"]
    assert len(certs) == 2
    assert all(
        c["worker_id"] == "WRK-101" for c in certs
    )


def test_expiring_soon():
    """Expiring soon returns certs within window."""
    tool = TrainingTracker()
    result = tool.execute(
        action="expiring_soon",
        project_id="PRJ-001",
        days_ahead=30,
    )
    data = json.loads(result)
    assert "expiring_certifications" in data
    expiring = data["expiring_certifications"]
    assert len(expiring) > 0
    for e in expiring:
        assert e["days_until_expiry"] <= 30


def test_training_gaps():
    """Training gaps returns identified gaps."""
    tool = TrainingTracker()
    result = tool.execute(
        action="training_gaps",
        project_id="PRJ-001",
    )
    data = json.loads(result)
    assert "training_gaps" in data
    gaps = data["training_gaps"]
    assert len(gaps) == 3
    urgencies = {g["urgency"] for g in gaps}
    assert "critical" in urgencies
    assert "high" in urgencies


def test_unknown_action():
    """Unknown action returns error string."""
    tool = TrainingTracker()
    result = tool.execute(action="invalid")
    assert "Error" in result


def test_error_handling():
    """Execute returns error string on exception."""
    tool = TrainingTracker()
    original = tool._check_certifications
    tool._check_certifications = lambda *a: (_ for _ in ()).throw(
        RuntimeError("DB unavailable")
    )
    result = tool.execute(
        action="check_certifications"
    )
    assert "Error" in result
    assert "DB unavailable" in result
    tool._check_certifications = original
