"""Tests for the ComplianceDatabaseTool."""

import json

from construction.tools.compliance_db import ComplianceDatabaseTool


def test_compliance_db_schema():
    tool = ComplianceDatabaseTool()
    schema = tool.get_input_schema()
    assert schema["type"] == "object"
    assert "action" in schema["properties"]
    assert "project_id" in schema["properties"]
    assert schema["required"] == ["action", "project_id"]


def test_compliance_db_api_format():
    tool = ComplianceDatabaseTool()
    fmt = tool.to_api_format()
    assert fmt["name"] == "compliance_database"
    assert "description" in fmt


def test_query_all():
    tool = ComplianceDatabaseTool()
    result = tool.execute(
        action="query", project_id="PROJ-001"
    )
    data = json.loads(result)
    assert data["project_id"] == "PROJ-001"
    assert len(data["checks"]) == 3


def test_query_with_severity_filter():
    tool = ComplianceDatabaseTool()
    result = tool.execute(
        action="query",
        project_id="PROJ-001",
        filters={"severity": "critical"},
    )
    data = json.loads(result)
    for check in data["checks"]:
        assert check["severity"] == "critical"
    assert len(data["checks"]) == 2


def test_query_with_status_filter():
    tool = ComplianceDatabaseTool()
    result = tool.execute(
        action="query",
        project_id="PROJ-001",
        filters={"status": "in_progress"},
    )
    data = json.loads(result)
    assert len(data["checks"]) == 1
    assert data["checks"][0]["status"] == "in_progress"


def test_query_with_check_type_filter():
    tool = ComplianceDatabaseTool()
    result = tool.execute(
        action="query",
        project_id="PROJ-001",
        filters={"check_type": "egress"},
    )
    data = json.loads(result)
    assert len(data["checks"]) == 1
    assert data["checks"][0]["check_type"] == "egress"


def test_create():
    tool = ComplianceDatabaseTool()
    result = tool.execute(
        action="create",
        project_id="PROJ-001",
        data={
            "check_type": "fire_separation",
            "severity": "critical",
            "description": "New fire separation issue",
        },
    )
    data = json.loads(result)
    assert data["project_id"] == "PROJ-001"
    assert data["status"] == "created"
    assert data["check_id"].startswith("CHK-")


def test_update():
    tool = ComplianceDatabaseTool()
    result = tool.execute(
        action="update",
        project_id="PROJ-001",
        check_id="CHK-001",
        data={"status": "resolved"},
    )
    data = json.loads(result)
    assert data["status"] == "updated"
    assert "status" in data["updated_fields"]


def test_update_missing_check_id():
    tool = ComplianceDatabaseTool()
    result = tool.execute(
        action="update",
        project_id="PROJ-001",
        data={"status": "resolved"},
    )
    assert "Error" in result
    assert "check_id" in result


def test_get_summary():
    tool = ComplianceDatabaseTool()
    result = tool.execute(
        action="get_summary", project_id="PROJ-001"
    )
    data = json.loads(result)
    assert data["project_id"] == "PROJ-001"
    assert data["total_checks"] == 15
    assert data["total_open"] == 5
    assert data["critical_count"] == 2
    assert "by_type" in data


def test_unknown_action():
    tool = ComplianceDatabaseTool()
    result = tool.execute(
        action="bad_action", project_id="PROJ-001"
    )
    assert "Error" in result
    assert "bad_action" in result
