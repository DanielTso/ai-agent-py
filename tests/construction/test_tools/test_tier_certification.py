"""Tests for the Uptime Institute tier certification tool."""

import json

from construction.tools.tier_certification import (
    TierCertification,
)


def test_schema():
    """Tool schema has expected properties."""
    tool = TierCertification()
    assert tool.name == "tier_certification"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "project_id" in props
    assert "tier_level" in props
    assert "system" in props
    assert set(props["action"]["enum"]) == {
        "tier_requirements",
        "redundancy_check",
        "concurrent_maintainability",
        "fault_tolerance",
        "certification_status",
    }


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = TierCertification()
    fmt = tool.to_api_format()
    assert fmt["name"] == "tier_certification"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_tier_requirements():
    """Tier requirements returns data for Tier III."""
    tool = TierCertification()
    result = tool.execute(
        action="tier_requirements",
        project_id="DC-001",
    )
    data = json.loads(result)
    assert data["tier_level"] == "III"
    reqs = data["requirements"]
    assert "Concurrently Maintainable" in reqs["name"]
    assert reqs["uptime"] == "99.982%"
    assert "2N" in reqs["power"]["ats"]
    assert "N+1" in reqs["power"]["ups"]


def test_tier_requirements_iv():
    """Tier IV requirements include 2N+1 redundancy."""
    tool = TierCertification()
    result = tool.execute(
        action="tier_requirements",
        project_id="DC-001",
        tier_level="IV",
    )
    data = json.loads(result)
    assert data["tier_level"] == "IV"
    reqs = data["requirements"]
    assert "Fault Tolerant" in reqs["name"]
    assert "2N+1" in reqs["redundancy"]
    assert "2(N+1)" in reqs["power"]["ups"]


def test_redundancy_check():
    """Redundancy check returns all systems."""
    tool = TierCertification()
    result = tool.execute(
        action="redundancy_check",
        project_id="DC-001",
    )
    data = json.loads(result)
    assert data["project_id"] == "DC-001"
    systems = data["systems"]
    assert "power" in systems
    assert "cooling" in systems
    assert "network" in systems
    assert "fire_suppression" in systems
    assert data["overall_status"] == "non_compliant"


def test_redundancy_check_by_system():
    """Redundancy check filters by system."""
    tool = TierCertification()
    result = tool.execute(
        action="redundancy_check",
        project_id="DC-001",
        system="power",
    )
    data = json.loads(result)
    systems = data["systems"]
    assert "power" in systems
    assert "cooling" not in systems
    power = systems["power"]
    assert len(power["components"]) == 4
    assert power["components"][0]["component"] == "UPS"


def test_concurrent_maintainability():
    """Concurrent maintainability returns Tier III data."""
    tool = TierCertification()
    result = tool.execute(
        action="concurrent_maintainability",
        project_id="DC-001",
    )
    data = json.loads(result)
    assert data["project_id"] == "DC-001"
    assert data["tier_iii_concurrent_maintainability"] is True
    power = data["systems"]["power"]
    assert power["concurrently_maintainable"] is True
    ups = power["components"]["ups"]
    assert ups["can_maintain_without_load_transfer"] is True
    assert ups["bypass_capability"] is True
    assert len(ups["isolation_points"]) >= 2


def test_fault_tolerance():
    """Fault tolerance returns Tier IV analysis."""
    tool = TierCertification()
    result = tool.execute(
        action="fault_tolerance",
        project_id="DC-001",
    )
    data = json.loads(result)
    assert data["project_id"] == "DC-001"
    assert data["tier_iv_fault_tolerant"] is False
    power = data["systems"]["power"]
    assert power["fault_tolerant"] is True
    ups = power["single_point_of_failure_analysis"]["ups"]
    assert ups["dual_active_paths"] is True
    assert ups["transfer_time_ms"] <= 12
    cooling = data["systems"]["cooling"]
    assert cooling["fault_tolerant"] is False
    assert len(cooling["findings"]) > 0


def test_certification_status():
    """Certification status returns all phases."""
    tool = TierCertification()
    result = tool.execute(
        action="certification_status",
        project_id="DC-001",
    )
    data = json.loads(result)
    assert data["project_id"] == "DC-001"
    assert data["target_tier"] == "III"
    design = data["design_certification"]
    assert design["status"] == "approved"
    assert design["score"] == 92
    construction = data["construction_certification"]
    assert construction["status"] == "in_progress"
    ops = data["operational_sustainability"]
    assert ops["status"] == "not_started"


def test_unknown_action():
    """Unknown action returns error string."""
    tool = TierCertification()
    result = tool.execute(action="invalid", project_id="DC-001")
    assert "Error" in result


def test_error_handling():
    """Execute returns error string on exception."""
    tool = TierCertification()
    original = tool._tier_requirements
    tool._tier_requirements = lambda *a: (_ for _ in ()).throw(RuntimeError("API unavailable"))
    result = tool.execute(action="tier_requirements", project_id="DC-001")
    assert "Error" in result
    assert "API unavailable" in result
    tool._tier_requirements = original
