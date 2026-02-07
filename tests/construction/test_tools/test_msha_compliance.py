"""Tests for the MSHA compliance tool."""

import json

from construction.tools.msha_compliance import (
    MshaComplianceTool,
)


def test_schema():
    """Tool schema has expected properties."""
    tool = MshaComplianceTool()
    assert tool.name == "msha_compliance"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "contractor" in props
    assert "mine_id" in props
    assert "location" in props
    assert set(props["action"]["enum"]) == {
        "contractor_check",
        "violation_search",
        "jurisdiction_check",
    }


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = MshaComplianceTool()
    fmt = tool.to_api_format()
    assert fmt["name"] == "msha_compliance"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_contractor_check():
    """Contractor check returns safety profile."""
    tool = MshaComplianceTool()
    result = tool.execute(
        action="contractor_check",
        contractor="ABC Mining Services",
    )
    data = json.loads(result)
    assert "contractor_profile" in data
    profile = data["contractor_profile"]
    assert profile["contractor"] == "ABC Mining Services"
    assert "violations_last_2y" in profile
    assert "risk_level" in profile


def test_violation_search():
    """Violation search returns violation records."""
    tool = MshaComplianceTool()
    result = tool.execute(
        action="violation_search",
        mine_id="M-9999999",
    )
    data = json.loads(result)
    assert "violations" in data
    assert data["mine_id"] == "M-9999999"
    violations = data["violations"]
    assert len(violations) == 2
    assert "standard" in violations[0]


def test_jurisdiction_check():
    """Jurisdiction check returns OSHA/MSHA determination."""
    tool = MshaComplianceTool()
    result = tool.execute(
        action="jurisdiction_check",
        location="Downtown commercial site",
    )
    data = json.loads(result)
    assert "jurisdiction" in data
    j = data["jurisdiction"]
    assert j["location"] == "Downtown commercial site"
    assert j["osha_jurisdiction"] is True
    assert "rationale" in j


def test_unknown_action():
    """Unknown action returns error string."""
    tool = MshaComplianceTool()
    result = tool.execute(action="invalid")
    assert "Error" in result


def test_error_handling():
    """Execute returns error string on exception."""
    tool = MshaComplianceTool()
    original = tool._contractor_check
    tool._contractor_check = lambda *a: (_ for _ in ()).throw(
        RuntimeError("API error")
    )
    result = tool.execute(
        action="contractor_check",
        contractor="Test",
    )
    assert "Error" in result
    assert "API error" in result
    tool._contractor_check = original
