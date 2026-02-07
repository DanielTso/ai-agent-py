"""Tests for the supply chain monitor tool."""

import json

from construction.tools.supply_chain_tools import SupplyChainMonitor


def test_schema():
    """Tool schema has required fields."""
    tool = SupplyChainMonitor()
    assert tool.name == "supply_chain_monitor"
    schema = tool.get_input_schema()
    props = schema["properties"]
    assert "action" in props
    assert "project_id" in props
    assert "vendor_id" in props
    assert "shipment_id" in props
    assert "material" in props
    assert props["action"]["enum"] == [
        "vendor_status", "track_shipment", "find_alternatives"
    ]
    assert schema["required"] == ["action", "project_id"]


def test_api_format():
    """Tool converts to Anthropic API format correctly."""
    tool = SupplyChainMonitor()
    fmt = tool.to_api_format()
    assert fmt["name"] == "supply_chain_monitor"
    assert "description" in fmt
    assert "input_schema" in fmt


def test_vendor_status_all():
    """vendor_status returns all vendors."""
    tool = SupplyChainMonitor()
    result = tool.execute(
        action="vendor_status", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "vendors" in data
    assert len(data["vendors"]) == 4


def test_vendor_status_by_id():
    """vendor_status filters by vendor_id."""
    tool = SupplyChainMonitor()
    result = tool.execute(
        action="vendor_status",
        project_id="PRJ-001",
        vendor_id="VND-001",
    )
    data = json.loads(result)
    assert len(data["vendors"]) == 1
    assert data["vendors"][0]["id"] == "VND-001"
    assert data["vendors"][0]["name"] == "Pacific Steel Corp"


def test_vendor_status_structure():
    """vendor_status returns expected fields."""
    tool = SupplyChainMonitor()
    result = tool.execute(
        action="vendor_status", project_id="PRJ-001"
    )
    data = json.loads(result)
    vendor = data["vendors"][0]
    assert "id" in vendor
    assert "name" in vendor
    assert "material" in vendor
    assert "lead_time_days" in vendor
    assert "current_status" in vendor
    assert "last_updated" in vendor


def test_track_shipment_all():
    """track_shipment returns all shipments."""
    tool = SupplyChainMonitor()
    result = tool.execute(
        action="track_shipment", project_id="PRJ-001"
    )
    data = json.loads(result)
    assert "shipments" in data
    assert len(data["shipments"]) == 2


def test_track_shipment_by_id():
    """track_shipment filters by shipment_id."""
    tool = SupplyChainMonitor()
    result = tool.execute(
        action="track_shipment",
        project_id="PRJ-001",
        shipment_id="SHP-001",
    )
    data = json.loads(result)
    assert len(data["shipments"]) == 1
    assert data["shipments"][0]["id"] == "SHP-001"


def test_track_shipment_has_milestones():
    """Shipments include milestone data."""
    tool = SupplyChainMonitor()
    result = tool.execute(
        action="track_shipment", project_id="PRJ-001"
    )
    data = json.loads(result)
    ship = data["shipments"][0]
    assert "milestones" in ship
    assert len(ship["milestones"]) >= 1
    ms = ship["milestones"][0]
    assert "description" in ms
    assert "timestamp" in ms


def test_find_alternatives():
    """find_alternatives returns 3 options with cost/schedule."""
    tool = SupplyChainMonitor()
    result = tool.execute(
        action="find_alternatives",
        project_id="PRJ-001",
        material="structural_steel",
    )
    data = json.loads(result)
    assert data["material"] == "structural_steel"
    assert "alternatives" in data
    assert len(data["alternatives"]) == 3
    alt = data["alternatives"][0]
    assert "alt_vendor" in alt
    assert "cost_delta" in alt
    assert "schedule_delta_days" in alt
    assert "recommended" in alt
    assert "confidence" in alt


def test_find_alternatives_without_material():
    """find_alternatives returns error when material is missing."""
    tool = SupplyChainMonitor()
    result = tool.execute(
        action="find_alternatives", project_id="PRJ-001"
    )
    assert "Error" in result
    assert "material is required" in result


def test_unknown_action():
    """Unknown action returns error."""
    tool = SupplyChainMonitor()
    result = tool.execute(
        action="list_all", project_id="PRJ-001"
    )
    assert "Error" in result
    assert "unknown action" in result
