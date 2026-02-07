"""Workforce management API endpoints."""

from datetime import date

from fastapi import APIRouter

from construction.schemas.workforce import (
    CertificationRecord,
    CrewStatus,
    LaborForecast,
    ProductivityMetric,
)

router = APIRouter()


@router.get("/crews", response_model=list[CrewStatus])
async def get_crews():
    """Crew status by trade."""
    return [
        CrewStatus(
            trade="Ironworkers",
            headcount=24,
            planned_production=1200,
            actual_production=1100,
            productivity_pct=91.7,
            location="Level 3, Zone A",
            overtime_hours=16,
        ),
        CrewStatus(
            trade="Electricians",
            headcount=18,
            planned_production=800,
            actual_production=820,
            productivity_pct=102.5,
            location="Level 2, Zone B",
            overtime_hours=4,
        ),
    ]


@router.get(
    "/productivity",
    response_model=list[ProductivityMetric],
)
async def get_productivity():
    """Productivity metrics."""
    return [
        ProductivityMetric(
            trade="Ironworkers",
            period="2025-W05",
            planned_units=300,
            actual_units=275,
            productivity_index=0.917,
            trend="stable",
        ),
        ProductivityMetric(
            trade="Electricians",
            period="2025-W05",
            planned_units=200,
            actual_units=205,
            productivity_index=1.025,
            trend="improving",
        ),
    ]


@router.get(
    "/certs", response_model=list[CertificationRecord]
)
async def get_certs():
    """Certification status."""
    return [
        CertificationRecord(
            worker_id="W-101",
            worker_name="John Smith",
            cert_type="OSHA30",
            issue_date=date(2023, 6, 15),
            expiry_date=date(2025, 6, 15),
            status="valid",
        ),
        CertificationRecord(
            worker_id="W-102",
            worker_name="Maria Garcia",
            cert_type="NETA",
            issue_date=date(2022, 3, 10),
            expiry_date=date(2025, 3, 10),
            status="expiring_soon",
        ),
    ]


@router.get(
    "/forecast", response_model=list[LaborForecast]
)
async def get_forecast():
    """Labor forecast."""
    return [
        LaborForecast(
            trade="Ironworkers",
            week="2025-W06",
            required_headcount=30,
            available_headcount=24,
            gap=6,
            critical=True,
        ),
        LaborForecast(
            trade="Electricians",
            week="2025-W06",
            required_headcount=18,
            available_headcount=20,
            gap=0,
            critical=False,
        ),
    ]
