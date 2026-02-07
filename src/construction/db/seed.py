"""Seed data for demo/testing."""

import uuid
from datetime import date, timedelta

DEMO_PROJECT_ID = "demo-project-001"

# Stable UUIDs for cross-referencing
_VENDOR_IDS = [str(uuid.uuid4()) for _ in range(12)]
_ACTIVITY_IDS = [str(uuid.uuid4()) for _ in range(25)]


def get_demo_project():
    """Return the demo project definition."""
    return {
        "id": DEMO_PROJECT_ID,
        "name": "Metro Data Center - Tier IV",
        "tier_level": "IV",
        "site_lat": 33.749,
        "site_lon": -84.388,
        "target_start": date(2024, 1, 15),
        "target_end": date(2025, 6, 30),
        "owner": "Metro Digital Infrastructure LLC",
        "contract_value": 85_000_000.0,
    }


def get_demo_risks():
    """Return 12 risk events spanning all categories."""
    return [
        {
            "id": str(uuid.uuid4()),
            "project_id": DEMO_PROJECT_ID,
            "category": "supply",
            "description": (
                "Transformer T-2MVA-01 delayed at Port Kelang"
                " - vessel MV Pacific Star stuck in"
                " congestion; 14-day slip confirmed by"
                " Portcast AIS data"
            ),
            "probability": 0.91,
            "impact_dollars": 7_000_000.0,
            "impact_days": 14,
            "safety_critical": False,
            "confidence": 0.82,
            "status": "active",
        },
        {
            "id": str(uuid.uuid4()),
            "project_id": DEMO_PROJECT_ID,
            "category": "weather",
            "description": (
                "Tropical Storm Andrea forecast to pass"
                " within 100mi of site in 10 days;"
                " sustained winds 45mph expected"
            ),
            "probability": 0.65,
            "impact_dollars": 2_500_000.0,
            "impact_days": 5,
            "safety_critical": True,
            "confidence": 0.70,
            "status": "active",
        },
        {
            "id": str(uuid.uuid4()),
            "project_id": DEMO_PROJECT_ID,
            "category": "labor",
            "description": (
                "Electrical contractor workforce down 30%"
                " due to competing data center project"
                " in adjacent county"
            ),
            "probability": 0.78,
            "impact_dollars": 3_200_000.0,
            "impact_days": 21,
            "safety_critical": False,
            "confidence": 0.85,
            "status": "active",
        },
        {
            "id": str(uuid.uuid4()),
            "project_id": DEMO_PROJECT_ID,
            "category": "safety",
            "description": (
                "Silica dust levels at foundation"
                " excavation zone approaching 50% of"
                " OSHA PEL; trend indicates exceedance"
                " within 2 weeks"
            ),
            "probability": 0.55,
            "impact_dollars": 500_000.0,
            "impact_days": 3,
            "safety_critical": True,
            "confidence": 0.88,
            "status": "active",
        },
        {
            "id": str(uuid.uuid4()),
            "project_id": DEMO_PROJECT_ID,
            "category": "regulatory",
            "description": (
                "Stormwater permit SW-2024-0891 expires"
                " in 30 days; renewal application not"
                " yet submitted to GA EPD"
            ),
            "probability": 0.40,
            "impact_dollars": 1_800_000.0,
            "impact_days": 14,
            "safety_critical": False,
            "confidence": 0.92,
            "status": "active",
        },
        {
            "id": str(uuid.uuid4()),
            "project_id": DEMO_PROJECT_ID,
            "category": "financial",
            "description": (
                "Steel price index up 12% in 60 days;"
                " remaining structural steel procurement"
                " at risk of budget overrun"
            ),
            "probability": 0.72,
            "impact_dollars": 4_100_000.0,
            "impact_days": 0,
            "safety_critical": False,
            "confidence": 0.78,
            "status": "active",
        },
        {
            "id": str(uuid.uuid4()),
            "project_id": DEMO_PROJECT_ID,
            "category": "design",
            "description": (
                "BIM clash detected between HVAC duct"
                " run and structural beam at Level 3"
                " server hall; RFI pending architect"
                " response"
            ),
            "probability": 0.95,
            "impact_dollars": 350_000.0,
            "impact_days": 7,
            "safety_critical": False,
            "confidence": 0.95,
            "status": "active",
        },
        {
            "id": str(uuid.uuid4()),
            "project_id": DEMO_PROJECT_ID,
            "category": "supply",
            "description": (
                "UPS battery modules from Samsung SDI"
                " subject to new DOT shipping"
                " restrictions; customs clearance"
                " delayed 10 days"
            ),
            "probability": 0.60,
            "impact_dollars": 1_200_000.0,
            "impact_days": 10,
            "safety_critical": False,
            "confidence": 0.75,
            "status": "active",
        },
        {
            "id": str(uuid.uuid4()),
            "project_id": DEMO_PROJECT_ID,
            "category": "quality",
            "description": (
                "Concrete batch plant QC reports show"
                " cylinder break strengths trending 8%"
                " below design mix target"
            ),
            "probability": 0.45,
            "impact_dollars": 900_000.0,
            "impact_days": 10,
            "safety_critical": True,
            "confidence": 0.80,
            "status": "active",
        },
        {
            "id": str(uuid.uuid4()),
            "project_id": DEMO_PROJECT_ID,
            "category": "commissioning",
            "description": (
                "Generator load bank testing requires"
                " 2MW temporary power; utility company"
                " has 6-week lead time for connection"
            ),
            "probability": 0.85,
            "impact_dollars": 600_000.0,
            "impact_days": 21,
            "safety_critical": False,
            "confidence": 0.90,
            "status": "active",
        },
        {
            "id": str(uuid.uuid4()),
            "project_id": DEMO_PROJECT_ID,
            "category": "labor",
            "description": (
                "IBEW Local 613 collective bargaining"
                " agreement expires in 45 days; strike"
                " authorization vote scheduled"
            ),
            "probability": 0.25,
            "impact_dollars": 12_000_000.0,
            "impact_days": 30,
            "safety_critical": False,
            "confidence": 0.60,
            "status": "monitoring",
        },
        {
            "id": str(uuid.uuid4()),
            "project_id": DEMO_PROJECT_ID,
            "category": "safety",
            "description": (
                "Heat index forecast to exceed NIOSH"
                " action limit (91F) for 5 consecutive"
                " days next week; outdoor work"
                " restrictions likely"
            ),
            "probability": 0.80,
            "impact_dollars": 400_000.0,
            "impact_days": 3,
            "safety_critical": True,
            "confidence": 0.75,
            "status": "active",
        },
    ]


def get_demo_vendors():
    """Return 12 vendors with varied statuses."""
    return [
        {
            "id": _VENDOR_IDS[0],
            "project_id": DEMO_PROJECT_ID,
            "name": "ABB Power Systems",
            "material": "2MVA Dry-Type Transformer (T-2MVA-01)",
            "lead_time_days": 120,
            "current_status": "critical_delay",
            "port_of_origin": "Port Kelang, Malaysia",
            "contact_info": {
                "contact": "Lee Wei Ming",
                "email": "lwm@abb-my.example.com",
                "phone": "+60-12-345-6789",
            },
        },
        {
            "id": _VENDOR_IDS[1],
            "project_id": DEMO_PROJECT_ID,
            "name": "Caterpillar Inc.",
            "material": "2MW Diesel Generator Set (CAT C32)",
            "lead_time_days": 90,
            "current_status": "on_track",
            "port_of_origin": "Lafayette, IN, USA",
            "contact_info": {
                "contact": "Mike Sullivan",
                "email": "msullivan@cat.example.com",
            },
        },
        {
            "id": _VENDOR_IDS[2],
            "project_id": DEMO_PROJECT_ID,
            "name": "Schneider Electric",
            "material": "Medium-Voltage Switchgear (15kV)",
            "lead_time_days": 85,
            "current_status": "on_track",
            "port_of_origin": "Seneca, SC, USA",
            "contact_info": {
                "contact": "Sarah Chen",
                "email": "schen@se.example.com",
            },
        },
        {
            "id": _VENDOR_IDS[3],
            "project_id": DEMO_PROJECT_ID,
            "name": "Samsung SDI",
            "material": "UPS Battery Modules (Li-ion 500kWh)",
            "lead_time_days": 100,
            "current_status": "delayed",
            "port_of_origin": "Ulsan, South Korea",
            "contact_info": {
                "contact": "Park Jun-ho",
                "email": "parkjh@samsungsdi.example.com",
            },
        },
        {
            "id": _VENDOR_IDS[4],
            "project_id": DEMO_PROJECT_ID,
            "name": "Vertiv Group",
            "material": "Precision Cooling Units (Liebert DSE)",
            "lead_time_days": 70,
            "current_status": "on_track",
            "port_of_origin": "Columbus, OH, USA",
            "contact_info": {
                "contact": "Tom Bradley",
                "email": "tbradley@vertiv.example.com",
            },
        },
        {
            "id": _VENDOR_IDS[5],
            "project_id": DEMO_PROJECT_ID,
            "name": "Nucor Steel",
            "material": "Structural Steel (W-shapes, HSS)",
            "lead_time_days": 45,
            "current_status": "price_escalation",
            "port_of_origin": "Berkeley County, SC, USA",
            "contact_info": {
                "contact": "James Whitfield",
                "email": "jwhitfield@nucor.example.com",
            },
        },
        {
            "id": _VENDOR_IDS[6],
            "project_id": DEMO_PROJECT_ID,
            "name": "Rittal Systems",
            "material": "Server Cabinets (42U, 800 units)",
            "lead_time_days": 60,
            "current_status": "on_track",
            "port_of_origin": "Urbana, OH, USA",
            "contact_info": {
                "contact": "Klaus Muller",
                "email": "kmuller@rittal.example.com",
            },
        },
        {
            "id": _VENDOR_IDS[7],
            "project_id": DEMO_PROJECT_ID,
            "name": "Corning Inc.",
            "material": "Fiber Optic Cabling (OM4, 50km)",
            "lead_time_days": 30,
            "current_status": "on_track",
            "port_of_origin": "Hickory, NC, USA",
            "contact_info": {
                "contact": "Amy Rivera",
                "email": "arivera@corning.example.com",
            },
        },
        {
            "id": _VENDOR_IDS[8],
            "project_id": DEMO_PROJECT_ID,
            "name": "ASCO Power Technologies",
            "material": "Automatic Transfer Switches (4000A)",
            "lead_time_days": 75,
            "current_status": "on_track",
            "port_of_origin": "Florham Park, NJ, USA",
            "contact_info": {
                "contact": "David Park",
                "email": "dpark@ascopower.example.com",
            },
        },
        {
            "id": _VENDOR_IDS[9],
            "project_id": DEMO_PROJECT_ID,
            "name": "Trane Technologies",
            "material": "Chiller Plant (1200-ton centrifugal)",
            "lead_time_days": 110,
            "current_status": "on_track",
            "port_of_origin": "Tyler, TX, USA",
            "contact_info": {
                "contact": "Maria Gonzalez",
                "email": "mgonzalez@trane.example.com",
            },
        },
        {
            "id": _VENDOR_IDS[10],
            "project_id": DEMO_PROJECT_ID,
            "name": "Baker Concrete",
            "material": "Ready-Mix Concrete (5000psi, 8000cy)",
            "lead_time_days": 3,
            "current_status": "quality_concern",
            "port_of_origin": "Local - Atlanta, GA",
            "contact_info": {
                "contact": "Steve Baker Jr.",
                "email": "sbaker@bakerconcrete.example.com",
            },
        },
        {
            "id": _VENDOR_IDS[11],
            "project_id": DEMO_PROJECT_ID,
            "name": "Panduit Corp",
            "material": "Cable Management (J-hooks, ladder rack)",
            "lead_time_days": 21,
            "current_status": "on_track",
            "port_of_origin": "Tinley Park, IL, USA",
            "contact_info": {
                "contact": "Rachel Kim",
                "email": "rkim@panduit.example.com",
            },
        },
    ]


def get_demo_schedule_activities():
    """Return 25 activities forming a realistic critical path."""
    start = date(2024, 1, 15)
    activities = [
        # Phase 1: Site Work & Foundation
        {
            "id": _ACTIVITY_IDS[0],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A1000",
            "name": "Site Mobilization & Grading",
            "start_date": start,
            "end_date": start + timedelta(days=21),
            "total_float": 0,
            "is_critical": True,
            "tier_critical": True,
            "predecessors": None,
            "successors": ["A1010", "A1020"],
        },
        {
            "id": _ACTIVITY_IDS[1],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A1010",
            "name": "Foundation Excavation & Piling",
            "start_date": start + timedelta(days=22),
            "end_date": start + timedelta(days=56),
            "total_float": 0,
            "is_critical": True,
            "tier_critical": True,
            "predecessors": ["A1000"],
            "successors": ["A1030"],
        },
        {
            "id": _ACTIVITY_IDS[2],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A1020",
            "name": "Underground Utilities & Storm Drainage",
            "start_date": start + timedelta(days=22),
            "end_date": start + timedelta(days=49),
            "total_float": 7,
            "is_critical": False,
            "tier_critical": False,
            "predecessors": ["A1000"],
            "successors": ["A1030"],
        },
        {
            "id": _ACTIVITY_IDS[3],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A1030",
            "name": "Foundation Mat Pour (5000psi)",
            "start_date": start + timedelta(days=57),
            "end_date": start + timedelta(days=71),
            "total_float": 0,
            "is_critical": True,
            "tier_critical": True,
            "predecessors": ["A1010", "A1020"],
            "successors": ["A2000"],
        },
        # Phase 2: Structural Steel
        {
            "id": _ACTIVITY_IDS[4],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A2000",
            "name": "Structural Steel Erection - Phase 1",
            "start_date": start + timedelta(days=72),
            "end_date": start + timedelta(days=114),
            "total_float": 0,
            "is_critical": True,
            "tier_critical": True,
            "predecessors": ["A1030"],
            "successors": ["A2010", "A2020"],
        },
        {
            "id": _ACTIVITY_IDS[5],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A2010",
            "name": "Metal Deck & Concrete Slab on Deck",
            "start_date": start + timedelta(days=100),
            "end_date": start + timedelta(days=135),
            "total_float": 0,
            "is_critical": True,
            "tier_critical": False,
            "predecessors": ["A2000"],
            "successors": ["A3000"],
        },
        {
            "id": _ACTIVITY_IDS[6],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A2020",
            "name": "Roof Structure & Waterproofing",
            "start_date": start + timedelta(days=115),
            "end_date": start + timedelta(days=142),
            "total_float": 5,
            "is_critical": False,
            "tier_critical": False,
            "predecessors": ["A2000"],
            "successors": ["A3010"],
        },
        # Phase 3: MEP Rough-In
        {
            "id": _ACTIVITY_IDS[7],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A3000",
            "name": "Electrical Rough-In (Bus Duct & Conduit)",
            "start_date": start + timedelta(days=136),
            "end_date": start + timedelta(days=185),
            "total_float": 0,
            "is_critical": True,
            "tier_critical": True,
            "predecessors": ["A2010"],
            "successors": ["A4000", "A4010"],
        },
        {
            "id": _ACTIVITY_IDS[8],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A3010",
            "name": "HVAC Duct & Piping Installation",
            "start_date": start + timedelta(days=143),
            "end_date": start + timedelta(days=192),
            "total_float": 3,
            "is_critical": False,
            "tier_critical": False,
            "predecessors": ["A2020"],
            "successors": ["A4020"],
        },
        {
            "id": _ACTIVITY_IDS[9],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A3020",
            "name": "Fire Suppression (Pre-Action Dry Pipe)",
            "start_date": start + timedelta(days=150),
            "end_date": start + timedelta(days=185),
            "total_float": 10,
            "is_critical": False,
            "tier_critical": True,
            "predecessors": ["A2010"],
            "successors": ["A4020"],
        },
        {
            "id": _ACTIVITY_IDS[10],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A3030",
            "name": "Plumbing & Condensate Drainage",
            "start_date": start + timedelta(days=150),
            "end_date": start + timedelta(days=178),
            "total_float": 15,
            "is_critical": False,
            "tier_critical": False,
            "predecessors": ["A2010"],
            "successors": ["A4020"],
        },
        # Phase 4: Critical Power Infrastructure
        {
            "id": _ACTIVITY_IDS[11],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A4000",
            "name": "Transformer T-2MVA-01 Installation",
            "start_date": start + timedelta(days=186),
            "end_date": start + timedelta(days=200),
            "total_float": 0,
            "is_critical": True,
            "tier_critical": True,
            "predecessors": ["A3000"],
            "successors": ["A4030"],
        },
        {
            "id": _ACTIVITY_IDS[12],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A4010",
            "name": "Generator Set Installation (2x CAT C32)",
            "start_date": start + timedelta(days=186),
            "end_date": start + timedelta(days=207),
            "total_float": 0,
            "is_critical": True,
            "tier_critical": True,
            "predecessors": ["A3000"],
            "successors": ["A4030"],
        },
        {
            "id": _ACTIVITY_IDS[13],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A4020",
            "name": "Chiller Plant & Cooling Tower Install",
            "start_date": start + timedelta(days=193),
            "end_date": start + timedelta(days=228),
            "total_float": 5,
            "is_critical": False,
            "tier_critical": True,
            "predecessors": ["A3010", "A3020", "A3030"],
            "successors": ["A5010"],
        },
        {
            "id": _ACTIVITY_IDS[14],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A4030",
            "name": "UPS & Battery Installation",
            "start_date": start + timedelta(days=208),
            "end_date": start + timedelta(days=228),
            "total_float": 0,
            "is_critical": True,
            "tier_critical": True,
            "predecessors": ["A4000", "A4010"],
            "successors": ["A5000"],
        },
        {
            "id": _ACTIVITY_IDS[15],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A4040",
            "name": "MV Switchgear & ATS Installation",
            "start_date": start + timedelta(days=200),
            "end_date": start + timedelta(days=221),
            "total_float": 7,
            "is_critical": False,
            "tier_critical": True,
            "predecessors": ["A4000"],
            "successors": ["A5000"],
        },
        # Phase 5: Data Hall Fit-Out
        {
            "id": _ACTIVITY_IDS[16],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A5000",
            "name": "Raised Floor & Cable Tray Installation",
            "start_date": start + timedelta(days=229),
            "end_date": start + timedelta(days=256),
            "total_float": 0,
            "is_critical": True,
            "tier_critical": True,
            "predecessors": ["A4030", "A4040"],
            "successors": ["A5020"],
        },
        {
            "id": _ACTIVITY_IDS[17],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A5010",
            "name": "CRAH Units & Cooling Distribution",
            "start_date": start + timedelta(days=229),
            "end_date": start + timedelta(days=249),
            "total_float": 7,
            "is_critical": False,
            "tier_critical": True,
            "predecessors": ["A4020"],
            "successors": ["A5020"],
        },
        {
            "id": _ACTIVITY_IDS[18],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A5020",
            "name": "Server Cabinet & PDU Installation",
            "start_date": start + timedelta(days=257),
            "end_date": start + timedelta(days=285),
            "total_float": 0,
            "is_critical": True,
            "tier_critical": True,
            "predecessors": ["A5000", "A5010"],
            "successors": ["A6000"],
        },
        {
            "id": _ACTIVITY_IDS[19],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A5030",
            "name": "Fiber Optic & Network Cabling",
            "start_date": start + timedelta(days=260),
            "end_date": start + timedelta(days=285),
            "total_float": 5,
            "is_critical": False,
            "tier_critical": True,
            "predecessors": ["A5000"],
            "successors": ["A6000"],
        },
        # Phase 6: Commissioning & Turnover
        {
            "id": _ACTIVITY_IDS[20],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A6000",
            "name": "Tier IV Commissioning - Level 1 (Component)",
            "start_date": start + timedelta(days=286),
            "end_date": start + timedelta(days=314),
            "total_float": 0,
            "is_critical": True,
            "tier_critical": True,
            "predecessors": ["A5020", "A5030"],
            "successors": ["A6010"],
        },
        {
            "id": _ACTIVITY_IDS[21],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A6010",
            "name": "Tier IV Commissioning - Level 2 (System)",
            "start_date": start + timedelta(days=315),
            "end_date": start + timedelta(days=343),
            "total_float": 0,
            "is_critical": True,
            "tier_critical": True,
            "predecessors": ["A6000"],
            "successors": ["A6020"],
        },
        {
            "id": _ACTIVITY_IDS[22],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A6020",
            "name": "Tier IV Commissioning - Level 3 (Integrated)",
            "start_date": start + timedelta(days=344),
            "end_date": start + timedelta(days=379),
            "total_float": 0,
            "is_critical": True,
            "tier_critical": True,
            "predecessors": ["A6010"],
            "successors": ["A6030"],
        },
        {
            "id": _ACTIVITY_IDS[23],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A6030",
            "name": "Generator Load Bank Testing (72hr)",
            "start_date": start + timedelta(days=380),
            "end_date": start + timedelta(days=393),
            "total_float": 0,
            "is_critical": True,
            "tier_critical": True,
            "predecessors": ["A6020"],
            "successors": ["A7000"],
        },
        {
            "id": _ACTIVITY_IDS[24],
            "project_id": DEMO_PROJECT_ID,
            "external_id": "A7000",
            "name": "Substantial Completion & Turnover",
            "start_date": start + timedelta(days=394),
            "end_date": start + timedelta(days=407),
            "total_float": 0,
            "is_critical": True,
            "tier_critical": True,
            "predecessors": ["A6030"],
            "successors": None,
        },
    ]
    return activities


def get_demo_safety_data():
    """Return safety incidents, metrics, and training records."""
    return {
        "incidents": [
            {
                "project_id": DEMO_PROJECT_ID,
                "osha_classification": "near_miss",
                "severity": "low",
                "location": "Foundation Excavation Zone B",
                "description": (
                    "Unsecured trench box shifted 6 inches during backfill; no workers in trench"
                ),
                "recordable": False,
                "lost_time_days": 0,
                "incident_date": date(2024, 3, 12),
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "osha_classification": "first_aid",
                "severity": "low",
                "location": "Steel Erection - Level 2",
                "description": (
                    "Ironworker laceration to left hand"
                    " from sharp edge on connection plate;"
                    " treated on-site"
                ),
                "recordable": False,
                "lost_time_days": 0,
                "incident_date": date(2024, 5, 8),
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "osha_classification": "recordable",
                "severity": "medium",
                "location": "Mechanical Room A",
                "description": (
                    "Pipefitter strained lower back lifting 60lb valve; missed 2 days of work"
                ),
                "recordable": True,
                "lost_time_days": 2,
                "incident_date": date(2024, 6, 22),
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "osha_classification": "near_miss",
                "severity": "high",
                "location": "Crane Staging Area",
                "description": (
                    "Rigging failure dropped 2-ton steel"
                    " beam from 15ft; exclusion zone was"
                    " properly enforced, no injuries"
                ),
                "recordable": False,
                "lost_time_days": 0,
                "incident_date": date(2024, 7, 15),
            },
        ],
        "metrics": [
            {
                "project_id": DEMO_PROJECT_ID,
                "period": "2024-Q1",
                "trir": 1.8,
                "dart": 0.0,
                "emr": 0.92,
                "near_miss_count": 3,
                "leading_indicators": {
                    "toolbox_talks": 52,
                    "safety_observations": 180,
                    "hazard_reports": 24,
                },
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "period": "2024-Q2",
                "trir": 2.1,
                "dart": 0.7,
                "emr": 0.92,
                "near_miss_count": 5,
                "leading_indicators": {
                    "toolbox_talks": 48,
                    "safety_observations": 165,
                    "hazard_reports": 31,
                },
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "period": "2024-Q3-partial",
                "trir": 1.5,
                "dart": 0.0,
                "emr": 0.92,
                "near_miss_count": 2,
                "leading_indicators": {
                    "toolbox_talks": 26,
                    "safety_observations": 95,
                    "hazard_reports": 18,
                },
            },
        ],
        "training": [
            {
                "project_id": DEMO_PROJECT_ID,
                "worker_id": "W-001",
                "worker_name": "Carlos Mendez",
                "training_type": "OSHA 30-Hour Construction",
                "completion_date": date(2023, 11, 15),
                "expiry": date(2028, 11, 15),
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "worker_id": "W-002",
                "worker_name": "James Patterson",
                "training_type": "Confined Space Entry",
                "completion_date": date(2024, 1, 10),
                "expiry": date(2025, 1, 10),
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "worker_id": "W-003",
                "worker_name": "Robert Chen",
                "training_type": "Fall Protection Competent Person",
                "completion_date": date(2023, 6, 20),
                "expiry": date(2024, 6, 20),
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "worker_id": "W-004",
                "worker_name": "Maria Santos",
                "training_type": "Crane Signal Person",
                "completion_date": date(2024, 2, 1),
                "expiry": date(2025, 2, 1),
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "worker_id": "W-005",
                "worker_name": "David Thompson",
                "training_type": "Silica Competent Person",
                "completion_date": date(2024, 3, 5),
                "expiry": date(2025, 3, 5),
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "worker_id": "W-006",
                "worker_name": "Ahmad Hassan",
                "training_type": "Electrical Safety (NFPA 70E)",
                "completion_date": date(2023, 9, 1),
                "expiry": date(2024, 9, 1),
            },
        ],
    }


def get_demo_financial_data():
    """Return budget items, earned value snapshots, and change orders."""
    return {
        "budget_items": [
            {
                "project_id": DEMO_PROJECT_ID,
                "category": "Site Work",
                "description": "Grading, excavation, utilities",
                "planned_cost": 4_500_000.0,
                "actual_cost": 4_650_000.0,
                "forecast_cost": 4_650_000.0,
                "variance": -150_000.0,
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "category": "Structural",
                "description": ("Foundation, steel, concrete"),
                "planned_cost": 12_000_000.0,
                "actual_cost": 8_400_000.0,
                "forecast_cost": 13_440_000.0,
                "variance": -1_440_000.0,
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "category": "Electrical",
                "description": ("Power distribution, lighting, controls"),
                "planned_cost": 18_000_000.0,
                "actual_cost": 9_200_000.0,
                "forecast_cost": 19_800_000.0,
                "variance": -1_800_000.0,
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "category": "Mechanical",
                "description": "HVAC, plumbing, fire protection",
                "planned_cost": 15_000_000.0,
                "actual_cost": 7_100_000.0,
                "forecast_cost": 15_200_000.0,
                "variance": -200_000.0,
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "category": "Critical Power",
                "description": ("Generators, UPS, transformers, ATS"),
                "planned_cost": 22_000_000.0,
                "actual_cost": 5_500_000.0,
                "forecast_cost": 23_100_000.0,
                "variance": -1_100_000.0,
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "category": "Data Hall Fit-Out",
                "description": ("Raised floor, cabinets, cabling"),
                "planned_cost": 8_500_000.0,
                "actual_cost": 0.0,
                "forecast_cost": 8_500_000.0,
                "variance": 0.0,
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "category": "Commissioning",
                "description": ("Tier IV commissioning & testing"),
                "planned_cost": 3_000_000.0,
                "actual_cost": 0.0,
                "forecast_cost": 3_200_000.0,
                "variance": -200_000.0,
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "category": "General Conditions",
                "description": ("PM, supervision, insurance, bonds"),
                "planned_cost": 2_000_000.0,
                "actual_cost": 1_100_000.0,
                "forecast_cost": 2_100_000.0,
                "variance": -100_000.0,
            },
        ],
        "earned_value": [
            {
                "project_id": DEMO_PROJECT_ID,
                "snapshot_date": date(2024, 3, 31),
                "bcws": 12_750_000.0,
                "bcwp": 12_200_000.0,
                "acwp": 12_800_000.0,
                "cpi": 0.953,
                "spi": 0.957,
                "eac": 89_200_000.0,
                "etc_": 76_400_000.0,
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "snapshot_date": date(2024, 6, 30),
                "bcws": 29_750_000.0,
                "bcwp": 27_800_000.0,
                "acwp": 29_500_000.0,
                "cpi": 0.942,
                "spi": 0.934,
                "eac": 90_200_000.0,
                "etc_": 60_700_000.0,
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "snapshot_date": date(2024, 8, 15),
                "bcws": 38_250_000.0,
                "bcwp": 35_950_000.0,
                "acwp": 38_100_000.0,
                "cpi": 0.944,
                "spi": 0.940,
                "eac": 90_100_000.0,
                "etc_": 52_000_000.0,
            },
        ],
        "change_orders": [
            {
                "project_id": DEMO_PROJECT_ID,
                "co_number": "CO-001",
                "description": (
                    "Additional piling at grid lines G-H due to unexpected rock formation"
                ),
                "cost_impact": 680_000.0,
                "schedule_impact_days": 5,
                "status": "approved",
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "co_number": "CO-002",
                "description": (
                    "Owner-directed upgrade from N+1 to 2N cooling redundancy in Hall A"
                ),
                "cost_impact": 2_100_000.0,
                "schedule_impact_days": 14,
                "status": "approved",
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "co_number": "CO-003",
                "description": ("Structural reinforcement for heavier-than-spec generator sets"),
                "cost_impact": 340_000.0,
                "schedule_impact_days": 0,
                "status": "approved",
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "co_number": "CO-004",
                "description": (
                    "Transformer T-2MVA-01 air freight expediting from alternate supplier (pending)"
                ),
                "cost_impact": 450_000.0,
                "schedule_impact_days": -7,
                "status": "pending_approval",
            },
            {
                "project_id": DEMO_PROJECT_ID,
                "co_number": "CO-005",
                "description": ("Steel price escalation claim per contract clause 14.3"),
                "cost_impact": 1_850_000.0,
                "schedule_impact_days": 0,
                "status": "under_review",
            },
        ],
    }


def get_demo_daily_brief():
    """Return a sample daily brief."""
    return {
        "project_id": DEMO_PROJECT_ID,
        "brief_date": date(2024, 8, 15),
        "top_threats": [
            {
                "rank": 1,
                "title": ("Transformer T-2MVA-01 delayed 14 days at Port Kelang"),
                "agent_source": "supply_chain",
                "impact": ("$7M impact, 14-day schedule slip on critical path"),
                "confidence": 0.82,
                "action_required": (
                    "APPROVE/REJECT CO-004: Air freight"
                    " expedite from Siemens alternate"
                    " ($450k, recovers 7 days)"
                ),
            },
            {
                "rank": 2,
                "title": ("Electrical workforce down 30%"),
                "agent_source": "workforce_labor",
                "impact": ("$3.2M impact, 21-day slip risk on electrical rough-in"),
                "confidence": 0.85,
                "action_required": (
                    "Authorize premium overtime rates and"
                    " contact IBEW Local 613 for"
                    " supplemental manpower"
                ),
            },
            {
                "rank": 3,
                "title": ("Tropical Storm Andrea approaching within 100mi"),
                "agent_source": "risk_forecaster",
                "impact": ("$2.5M impact, 5-day work stoppage if Cat 1+"),
                "confidence": 0.70,
                "action_required": (
                    "Activate severe weather protocol; secure materials and crane by Friday"
                ),
            },
        ],
        "quality_gaps": [
            {
                "rank": 1,
                "title": ("Concrete strength trending 8% below target"),
                "agent_source": "compliance_verifier",
                "severity": "high",
                "location": "Foundation Mat - Grid A-D",
            },
            {
                "rank": 2,
                "title": ("BIM clash HVAC vs structural beam at Level 3"),
                "agent_source": "document_intelligence",
                "severity": "medium",
                "location": "Server Hall - Level 3",
            },
        ],
        "acceleration": {
            "title": ("Fast-track raised floor installation via dual-crew overlap"),
            "agent_source": "critical_path",
            "potential_savings_days": 8,
            "cost": 180_000.0,
            "description": (
                "Deploy two raised-floor crews working"
                " opposite ends of Hall A"
                " simultaneously; requires 2nd material"
                " staging zone. Net recovery: 8 days on"
                " critical path at $180k premium."
            ),
        },
        "full_text": (
            "Daily Brief -- 2024-08-15\n"
            "========================================\n\n"
            "TOP 3 THREATS:\n"
            "  1. Transformer T-2MVA-01 delayed 14 days"
            " at Port Kelang (supply_chain)"
            " -- Impact: $7M, 14 days\n"
            "  2. Electrical workforce down 30%"
            " (workforce_labor)"
            " -- Impact: $3.2M, 21 days\n"
            "  3. Tropical Storm Andrea approaching"
            " (risk_forecaster)"
            " -- Impact: $2.5M, 5 days\n\n"
            "QUALITY GAPS:\n"
            "  1. Concrete strength trending 8% below"
            " target -- Severity: high"
            " @ Foundation Mat\n"
            "  2. BIM clash HVAC vs structural beam"
            " -- Severity: medium"
            " @ Server Hall Level 3\n\n"
            "ACCELERATION OPPORTUNITY:\n"
            "  Fast-track raised floor via dual-crew"
            " -- 8 days @ $180,000"
        ),
    }


def seed_all():
    """Return all demo data as a dict."""
    return {
        "project": get_demo_project(),
        "risks": get_demo_risks(),
        "vendors": get_demo_vendors(),
        "activities": get_demo_schedule_activities(),
        "safety": get_demo_safety_data(),
        "financial": get_demo_financial_data(),
        "daily_brief": get_demo_daily_brief(),
    }
