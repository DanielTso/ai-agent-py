"""Tests for the ICC building codes tool."""

import json

from construction.tools.icc_codes import IccCodesTool


def test_schema():
    """Tool schema has expected properties."""
    tool = IccCodesTool()
    assert tool.name == "icc_codes"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "project_id" in props
    assert "occupancy_type" in props
    assert "location" in props
    assert set(props["action"]["enum"]) == {
        "ibc_check",
        "ifc_check",
        "imc_check",
        "ipc_check",
        "iecc_check",
    }


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = IccCodesTool()
    fmt = tool.to_api_format()
    assert fmt["name"] == "icc_codes"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_ibc_check():
    """IBC check returns occupancy and structural data."""
    tool = IccCodesTool()
    result = tool.execute(
        action="ibc_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "occupancy_classification" in data
    assert "construction_type" in data
    assert "height_area_compliance" in data
    assert "accessibility_checks" in data
    assert "structural_requirements" in data
    assert "means_of_egress" in data
    classifications = data["occupancy_classification"]
    assert len(classifications) == 3
    groups = {c["occupancy_group"] for c in classifications}
    assert groups == {"B", "S-1", "F-1"}


def test_ibc_check_with_occupancy():
    """IBC check filters by occupancy type."""
    tool = IccCodesTool()
    result = tool.execute(
        action="ibc_check",
        project_id="PRJ-001",
        occupancy_type="B",
    )
    data = json.loads(result)
    classifications = data["occupancy_classification"]
    assert len(classifications) == 1
    assert classifications[0]["occupancy_group"] == "B"


def test_ifc_check():
    """IFC check returns fire code compliance data."""
    tool = IccCodesTool()
    result = tool.execute(
        action="ifc_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "ifc_compliance" in data
    checks = data["ifc_compliance"]
    assert "fire_access" in checks
    assert "fire_protection_systems" in checks
    assert "hazmat_storage" in checks
    assert "construction_fire_safety" in checks
    assert checks["fire_protection_systems"]["status"] == "warning"
    assert (
        checks["construction_fire_safety"]["code_section"]
        == "IFC Chapter 33"
    )


def test_imc_check():
    """IMC check returns mechanical code compliance data."""
    tool = IccCodesTool()
    result = tool.execute(
        action="imc_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "imc_compliance" in data
    checks = data["imc_compliance"]
    assert "ventilation_rates" in checks
    assert "equipment_compliance" in checks
    assert "ductwork_standards" in checks
    assert "energy_recovery" in checks
    assert checks["ductwork_standards"]["status"] == "warning"


def test_ipc_check():
    """IPC check returns plumbing code compliance data."""
    tool = IccCodesTool()
    result = tool.execute(
        action="ipc_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "ipc_compliance" in data
    checks = data["ipc_compliance"]
    assert "fixture_compliance" in checks
    assert "drainage_system" in checks
    assert "water_supply" in checks
    assert "backflow_prevention" in checks
    assert checks["water_supply"]["status"] == "warning"


def test_iecc_check():
    """IECC check returns energy code compliance data."""
    tool = IccCodesTool()
    result = tool.execute(
        action="iecc_check", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "iecc_compliance" in data
    checks = data["iecc_compliance"]
    assert "envelope_compliance" in checks
    assert "lighting_compliance" in checks
    assert "hvac_efficiency" in checks
    assert "commissioning_requirements" in checks
    assert checks["hvac_efficiency"]["status"] == "warning"
    cx = checks["commissioning_requirements"]
    assert "HVAC" in cx["systems_to_commission"]


def test_unknown_action():
    """Unknown action returns error string."""
    tool = IccCodesTool()
    result = tool.execute(
        action="invalid", project_id="PRJ-001"
    )
    assert "Error" in result


def test_error_handling():
    """Execute returns error string on exception."""
    tool = IccCodesTool()
    original = tool._ibc_check
    tool._ibc_check = lambda *a: (_ for _ in ()).throw(
        RuntimeError("DB unavailable")
    )
    result = tool.execute(
        action="ibc_check", project_id="PRJ-001"
    )
    assert "Error" in result
    assert "DB unavailable" in result
    tool._ibc_check = original
