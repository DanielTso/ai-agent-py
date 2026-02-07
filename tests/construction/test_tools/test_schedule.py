"""Tests for the ScheduleQueryTool."""

import json

from construction.tools.schedule import ScheduleQueryTool


def test_schedule_tool_schema():
    tool = ScheduleQueryTool()
    schema = tool.get_input_schema()
    assert schema["type"] == "object"
    assert "action" in schema["properties"]
    assert "project_id" in schema["properties"]
    assert schema["required"] == ["action", "project_id"]


def test_schedule_tool_api_format():
    tool = ScheduleQueryTool()
    fmt = tool.to_api_format()
    assert fmt["name"] == "schedule_query"
    assert "description" in fmt
    assert fmt["input_schema"]["type"] == "object"


def test_get_critical_path():
    tool = ScheduleQueryTool()
    result = tool.execute(
        action="get_critical_path", project_id="PROJ-001"
    )
    data = json.loads(result)
    assert data["project_id"] == "PROJ-001"
    cp = data["critical_path"]
    assert len(cp["activities"]) == 4
    assert cp["total_duration_days"] == 107
    for act in cp["activities"]:
        assert act["is_critical"] is True
    assert "ACT-001" in cp["float_summary"]


def test_get_activity():
    tool = ScheduleQueryTool()
    result = tool.execute(
        action="get_activity",
        project_id="PROJ-001",
        activity_id="ACT-005",
    )
    data = json.loads(result)
    assert data["project_id"] == "PROJ-001"
    assert data["activity"]["id"] == "ACT-005"
    assert "start_date" in data["activity"]
    assert "total_float" in data["activity"]


def test_get_activity_missing_id():
    tool = ScheduleQueryTool()
    result = tool.execute(
        action="get_activity", project_id="PROJ-001"
    )
    assert "Error" in result
    assert "activity_id" in result


def test_update_activity():
    tool = ScheduleQueryTool()
    result = tool.execute(
        action="update_activity",
        project_id="PROJ-001",
        activity_id="ACT-001",
        data={"end_date": "2026-04-01"},
    )
    data = json.loads(result)
    assert data["status"] == "updated"
    assert "end_date" in data["updated_fields"]


def test_update_activity_missing_id():
    tool = ScheduleQueryTool()
    result = tool.execute(
        action="update_activity",
        project_id="PROJ-001",
        data={"end_date": "2026-04-01"},
    )
    assert "Error" in result


def test_get_float_report():
    tool = ScheduleQueryTool()
    result = tool.execute(
        action="get_float_report", project_id="PROJ-001"
    )
    data = json.loads(result)
    assert data["project_id"] == "PROJ-001"
    report = data["float_report"]
    assert len(report) == 3
    statuses = {r["status"] for r in report}
    assert statuses == {"critical", "healthy", "warning"}


def test_unknown_action():
    tool = ScheduleQueryTool()
    result = tool.execute(
        action="invalid_action", project_id="PROJ-001"
    )
    assert "Error" in result
    assert "invalid_action" in result
