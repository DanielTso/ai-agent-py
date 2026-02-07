"""Tests for the communication drafting tool."""

import json

from construction.tools.communication import DraftCommunication


def test_schema():
    """Tool schema has required fields."""
    tool = DraftCommunication()
    assert tool.name == "draft_communication"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "project_id" in props
    assert "context" in props
    assert "tone" in props
    assert props["action"]["enum"] == [
        "owner_report",
        "rfi_response",
        "sub_notice",
        "owner_update",
    ]
    assert schema["required"] == [
        "action", "project_id", "context"
    ]


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = DraftCommunication()
    fmt = tool.to_api_format()
    assert fmt["name"] == "draft_communication"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_owner_report():
    """owner_report returns a draft report."""
    tool = DraftCommunication()
    result = tool.execute(
        action="owner_report",
        project_id="PRJ-001",
        context={"period": "2025-Q3"},
        tone="business",
    )
    data = json.loads(result)
    assert data["report_type"] == "owner_report"
    assert "2025-Q3" in data["title"]
    assert len(data["body"]) > 0
    assert data["tone"] == "business"
    assert data["status"] == "draft"


def test_rfi_response():
    """rfi_response returns a draft RFI response."""
    tool = DraftCommunication()
    result = tool.execute(
        action="rfi_response",
        project_id="PRJ-001",
        context={
            "rfi_number": "RFI-2025-042",
            "question": "Clarify conduit routing at Level 3",
        },
    )
    data = json.loads(result)
    assert data["rfi_number"] == "RFI-2025-042"
    assert len(data["response"]) > 0
    assert len(data["references"]) >= 1
    assert data["status"] == "draft"


def test_rfi_response_default_values():
    """rfi_response uses defaults when context is minimal."""
    tool = DraftCommunication()
    result = tool.execute(
        action="rfi_response",
        project_id="PRJ-001",
        context={},
    )
    data = json.loads(result)
    assert data["rfi_number"] == "RFI-2025-042"
    assert data["status"] == "draft"


def test_sub_notice():
    """sub_notice returns a contractual notice draft."""
    tool = DraftCommunication()
    result = tool.execute(
        action="sub_notice",
        project_id="PRJ-001",
        context={
            "notice_type": "delay",
            "recipient": "Pacific Steel Corp",
        },
    )
    data = json.loads(result)
    assert data["notice_type"] == "delay"
    assert data["recipient"] == "Pacific Steel Corp"
    assert "Section 8.3" in data["body"]
    assert data["contract_clause"] == "Section 8.3"
    assert data["status"] == "draft"


def test_owner_update():
    """owner_update returns an executive summary."""
    tool = DraftCommunication()
    result = tool.execute(
        action="owner_update",
        project_id="PRJ-001",
        context={"period": "Week of 2025-06-30"},
    )
    data = json.loads(result)
    assert data["period"] == "Week of 2025-06-30"
    assert len(data["executive_summary"]) > 0
    assert "key_metrics" in data
    assert "concerns" in data
    assert "next_steps" in data
    assert len(data["concerns"]) >= 1
    assert len(data["next_steps"]) >= 1


def test_owner_update_has_metrics():
    """owner_update includes key project metrics."""
    tool = DraftCommunication()
    result = tool.execute(
        action="owner_update",
        project_id="PRJ-001",
        context={},
    )
    data = json.loads(result)
    metrics = data["key_metrics"]
    assert "cpi" in metrics
    assert "spi" in metrics
    assert "pct_complete" in metrics


def test_unknown_action():
    """Unknown action returns error."""
    tool = DraftCommunication()
    result = tool.execute(
        action="email",
        project_id="PRJ-001",
        context={},
    )
    assert "Error" in result
    assert "unknown action" in result
