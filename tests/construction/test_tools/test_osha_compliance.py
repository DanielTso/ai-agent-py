"""Tests for the OSHA compliance tool."""

import json

from construction.tools.osha_compliance import (
    OshaComplianceTool,
)


def test_schema():
    """Tool schema has expected properties."""
    tool = OshaComplianceTool()
    assert tool.name == "osha_compliance"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "project_id" in props
    assert "location" in props
    assert set(props["action"]["enum"]) == {
        "osha_300_log",
        "focus_four_check",
        "silica_check",
        "electrical_check",
        "excavation_check",
    }


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = OshaComplianceTool()
    fmt = tool.to_api_format()
    assert fmt["name"] == "osha_compliance"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_osha_300_log():
    """OSHA 300 log returns recordable incidents."""
    tool = OshaComplianceTool()
    result = tool.execute(
        action="osha_300_log", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "osha_300_log" in data
    assert "summary" in data
    records = data["osha_300_log"]
    assert len(records) == 3
    assert data["summary"]["total_recordable"] == 2


def test_focus_four_check():
    """Focus Four check returns hazard status."""
    tool = OshaComplianceTool()
    result = tool.execute(
        action="focus_four_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "focus_four" in data
    checks = data["focus_four"]
    assert "falls" in checks
    assert "struck_by" in checks
    assert "caught_in_between" in checks
    assert "electrocution" in checks
    assert checks["electrocution"]["status"] == "critical"


def test_silica_check():
    """Silica check returns monitoring data."""
    tool = OshaComplianceTool()
    result = tool.execute(
        action="silica_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "silica_monitoring" in data
    assert "standard" in data
    monitoring = data["silica_monitoring"]
    assert len(monitoring) == 2
    assert monitoring[1]["compliant"] is False


def test_silica_check_with_location():
    """Silica check uses provided location."""
    tool = OshaComplianceTool()
    result = tool.execute(
        action="silica_check",
        project_id="PRJ-001",
        location="Level 4",
    )
    data = json.loads(result)
    monitoring = data["silica_monitoring"]
    assert monitoring[0]["location"] == "Level 4"


def test_electrical_check():
    """Electrical check returns GFCI and LOTO data."""
    tool = OshaComplianceTool()
    result = tool.execute(
        action="electrical_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "electrical_compliance" in data
    ec = data["electrical_compliance"]
    assert "gfci_status" in ec
    assert "loto_compliance" in ec
    assert ec["gfci_status"]["non_compliant"] == 3


def test_excavation_check():
    """Excavation check returns active excavation data."""
    tool = OshaComplianceTool()
    result = tool.execute(
        action="excavation_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "excavation_compliance" in data
    ec = data["excavation_compliance"]
    assert len(ec["active_excavations"]) == 2
    assert ec["active_excavations"][0]["compliant"] is True


def test_unknown_action():
    """Unknown action returns error string."""
    tool = OshaComplianceTool()
    result = tool.execute(
        action="invalid", project_id="PRJ-001"
    )
    assert "Error" in result


def test_error_handling():
    """Execute returns error string on exception."""
    tool = OshaComplianceTool()
    original = tool._osha_300_log
    tool._osha_300_log = lambda *a: (_ for _ in ()).throw(
        RuntimeError("DB unavailable")
    )
    result = tool.execute(
        action="osha_300_log", project_id="PRJ-001"
    )
    assert "Error" in result
    assert "DB unavailable" in result
    tool._osha_300_log = original
