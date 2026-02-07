"""Tests for the BIMQueryTool."""

import json

from construction.tools.bim import BIMQueryTool


def test_bim_tool_schema():
    tool = BIMQueryTool()
    schema = tool.get_input_schema()
    assert schema["type"] == "object"
    assert "action" in schema["properties"]
    assert "project_id" in schema["properties"]
    assert "element_id" in schema["properties"]
    assert schema["required"] == ["action", "project_id"]


def test_bim_tool_api_format():
    tool = BIMQueryTool()
    fmt = tool.to_api_format()
    assert fmt["name"] == "bim_query"
    assert "description" in fmt


def test_query_element():
    tool = BIMQueryTool()
    result = tool.execute(
        action="query_element",
        project_id="PROJ-001",
        element_id="HVAC-301",
    )
    data = json.loads(result)
    assert data["project_id"] == "PROJ-001"
    elem = data["element"]
    assert elem["element_id"] == "HVAC-301"
    assert elem["element_type"] == "HVAC_Duct"
    assert "dimensions" in elem
    assert "spec_reference" in elem


def test_query_element_missing_id():
    tool = BIMQueryTool()
    result = tool.execute(
        action="query_element", project_id="PROJ-001"
    )
    assert "Error" in result
    assert "element_id" in result


def test_check_compliance_all():
    tool = BIMQueryTool()
    result = tool.execute(
        action="check_compliance", project_id="PROJ-001"
    )
    data = json.loads(result)
    checks = data["checks"]
    assert len(checks) == 3
    types = {c["check_type"] for c in checks}
    assert "fire_separation" in types
    assert "redundancy_path" in types
    assert "egress" in types


def test_check_compliance_specific_type():
    tool = BIMQueryTool()
    result = tool.execute(
        action="check_compliance",
        project_id="PROJ-001",
        check_type="fire_separation",
    )
    data = json.loads(result)
    checks = data["checks"]
    assert len(checks) == 1
    assert checks[0]["check_type"] == "fire_separation"
    assert checks[0]["severity"] == "critical"


def test_get_deviations():
    tool = BIMQueryTool()
    result = tool.execute(
        action="get_deviations", project_id="PROJ-001"
    )
    data = json.loads(result)
    devs = data["deviations"]
    assert len(devs) == 2
    assert devs[0]["element_id"] == "WALL-FS-301"
    assert devs[1]["deviation_type"] == "redundancy_missing"


def test_unknown_action():
    tool = BIMQueryTool()
    result = tool.execute(
        action="invalid_action", project_id="PROJ-001"
    )
    assert "Error" in result
    assert "invalid_action" in result
