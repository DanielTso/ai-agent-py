"""Tests for the commissioning query tool."""

import json

from construction.tools.commissioning import CommissioningQuery


def test_schema():
    """Tool schema has expected properties."""
    tool = CommissioningQuery()
    assert tool.name == "commissioning_query"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "project_id" in props
    assert "system" in props
    assert set(props["action"]["enum"]) == {
        "ist_sequence",
        "punch_list",
        "turnover_status",
        "schedule_witness",
    }


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = CommissioningQuery()
    fmt = tool.to_api_format()
    assert fmt["name"] == "commissioning_query"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_ist_sequence():
    """IST sequence returns mock test data."""
    tool = CommissioningQuery()
    result = tool.execute(
        action="ist_sequence", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "ist_sequence" in data
    tests = data["ist_sequence"]
    assert len(tests) == 4
    assert tests[0]["test_id"] == "IST-001"
    assert tests[2]["status"] == "blocked"


def test_punch_list():
    """Punch list returns items with severity levels."""
    tool = CommissioningQuery()
    result = tool.execute(
        action="punch_list", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "punch_items" in data
    assert "summary" in data
    items = data["punch_items"]
    assert len(items) == 3
    assert items[0]["severity"] == "B"
    assert items[1]["commissioning_impact"] is True


def test_turnover_status():
    """Turnover status returns package data."""
    tool = CommissioningQuery()
    result = tool.execute(
        action="turnover_status", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "turnover_packages" in data
    pkgs = data["turnover_packages"]
    assert len(pkgs) == 3
    assert pkgs[1]["status"] == "ready"
    assert pkgs[1]["completion_pct"] == 100.0


def test_schedule_witness():
    """Witness scheduling returns confirmation."""
    tool = CommissioningQuery()
    result = tool.execute(
        action="schedule_witness",
        project_id="PRJ-001",
        data={"test_id": "IST-002", "date": "2025-07-15"},
    )
    data = json.loads(result)
    assert data["status"] == "scheduled"
    assert data["test_id"] == "IST-002"


def test_unknown_action():
    """Unknown action returns error string."""
    tool = CommissioningQuery()
    result = tool.execute(
        action="invalid", project_id="PRJ-001"
    )
    assert "Error" in result


def test_error_handling():
    """Execute returns error string on exception."""
    tool = CommissioningQuery()
    original = tool._ist_sequence
    tool._ist_sequence = lambda *a: (_ for _ in ()).throw(
        RuntimeError("DB unavailable")
    )
    result = tool.execute(
        action="ist_sequence", project_id="PRJ-001"
    )
    assert "Error" in result
    assert "DB unavailable" in result
    tool._ist_sequence = original
