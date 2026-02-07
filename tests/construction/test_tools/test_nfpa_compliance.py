"""Tests for the NFPA compliance tool."""

import json

from construction.tools.nfpa_compliance import (
    NfpaComplianceTool,
)


def test_schema():
    """Tool schema has expected properties."""
    tool = NfpaComplianceTool()
    assert tool.name == "nfpa_compliance"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "project_id" in props
    assert "location" in props
    assert "article_number" in props
    assert set(props["action"]["enum"]) == {
        "fire_protection_check",
        "nec_article_check",
        "life_safety_check",
        "sprinkler_alarm_check",
        "egress_check",
    }


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = NfpaComplianceTool()
    fmt = tool.to_api_format()
    assert fmt["name"] == "nfpa_compliance"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_fire_protection_check():
    """Fire protection check returns barrier and firestop data."""
    tool = NfpaComplianceTool()
    result = tool.execute(
        action="fire_protection_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "fire_protection" in data
    fp = data["fire_protection"]
    assert "fire_barriers" in fp
    assert "fire_dampers" in fp
    assert "firestop_systems" in fp
    assert fp["firestop_systems"]["status"] == "critical"


def test_nec_article_check():
    """NEC article check returns conductor and grounding data."""
    tool = NfpaComplianceTool()
    result = tool.execute(
        action="nec_article_check",
        project_id="PRJ-001",
        article_number="250",
    )
    data = json.loads(result)
    assert "nec_compliance" in data
    assert data["article_checked"] == "250"
    nc = data["nec_compliance"]
    assert "conductor_sizing" in nc
    assert "overcurrent_protection" in nc
    assert "grounding" in nc
    assert "emergency_systems" in nc
    assert nc["grounding"]["status"] == "critical"


def test_nec_article_check_default():
    """NEC article check defaults to article 210."""
    tool = NfpaComplianceTool()
    result = tool.execute(
        action="nec_article_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert data["article_checked"] == "210"


def test_life_safety_check():
    """Life safety check returns occupant load and exit data."""
    tool = NfpaComplianceTool()
    result = tool.execute(
        action="life_safety_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "life_safety" in data
    ls = data["life_safety"]
    assert "occupant_load" in ls
    assert "exit_capacity" in ls
    assert "travel_distance" in ls
    assert "exit_signs" in ls
    assert "emergency_lighting" in ls
    assert ls["travel_distance"]["compliant"] is False
    assert ls["exit_signs"]["compliant"] is False


def test_sprinkler_alarm_check():
    """Sprinkler and alarm check returns coverage and zone data."""
    tool = NfpaComplianceTool()
    result = tool.execute(
        action="sprinkler_alarm_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "sprinkler_alarm" in data
    sa = data["sprinkler_alarm"]
    assert "sprinkler_coverage" in sa
    assert "water_supply" in sa
    assert "fire_alarm" in sa
    assert sa["fire_alarm"]["status"] == "critical"
    assert sa["water_supply"]["flow_gpm"] == 750


def test_egress_check():
    """Egress check returns corridor and door swing data."""
    tool = NfpaComplianceTool()
    result = tool.execute(
        action="egress_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "egress_compliance" in data
    ec = data["egress_compliance"]
    assert "corridor_width" in ec
    assert "door_swing" in ec
    assert "exit_access" in ec
    assert "exit_discharge" in ec
    assert ec["corridor_width"]["compliant"] is True


def test_egress_check_with_location():
    """Egress check uses provided location."""
    tool = NfpaComplianceTool()
    result = tool.execute(
        action="egress_check",
        project_id="PRJ-001",
        location="Level 4 East Wing",
    )
    data = json.loads(result)
    ec = data["egress_compliance"]
    assert ec["corridor_width"]["location"] == "Level 4 East Wing"


def test_unknown_action():
    """Unknown action returns error string."""
    tool = NfpaComplianceTool()
    result = tool.execute(
        action="invalid", project_id="PRJ-001"
    )
    assert "Error" in result


def test_error_handling():
    """Execute returns error string on exception."""
    tool = NfpaComplianceTool()
    original = tool._fire_protection_check
    tool._fire_protection_check = lambda *a: (_ for _ in ()).throw(
        RuntimeError("DB unavailable")
    )
    result = tool.execute(
        action="fire_protection_check", project_id="PRJ-001"
    )
    assert "Error" in result
    assert "DB unavailable" in result
    tool._fire_protection_check = original
