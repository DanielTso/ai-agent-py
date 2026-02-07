"""Approval workflow API endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

from construction.schemas.common import (
    ApprovalRequest,
    ImpactSummary,
)

router = APIRouter()


class ApprovalAction(BaseModel):
    """Payload for approve/reject actions."""

    notes: str = ""


_MOCK_APPROVAL = ApprovalRequest(
    id="APR-001",
    agent_name="supply_chain",
    action_type="expedite_vendor",
    title="Expedite steel delivery via SteelWorks USA",
    description=(
        "Current vendor delayed 10 days. Alternative"
        " vendor can deliver 5 days sooner at $25K"
        " premium."
    ),
    confidence=85,
    data_sources=[],
    transparency_log=[
        "Checked 3 alternative vendors",
        "Verified schedule impact with critical path",
        "Cost within contingency budget",
    ],
    impact=ImpactSummary(
        cost_delta=25000,
        schedule_delta_days=-5,
        risk_change="reduced",
        description="Net schedule improvement of 5 days",
    ),
    status="pending",
)


@router.get("/", response_model=list[ApprovalRequest])
async def list_approvals():
    """List pending approvals."""
    return [_MOCK_APPROVAL]


@router.get(
    "/{approval_id}", response_model=ApprovalRequest
)
async def get_approval(approval_id: str):
    """Get approval details."""
    approval = _MOCK_APPROVAL.model_copy()
    approval.id = approval_id
    return approval


@router.post(
    "/{approval_id}/approve",
    response_model=ApprovalRequest,
)
async def approve(
    approval_id: str, action: ApprovalAction
):
    """Approve with notes."""
    approval = _MOCK_APPROVAL.model_copy()
    approval.id = approval_id
    approval.status = "approved"
    approval.pm_notes = action.notes or "Approved"
    return approval


@router.post(
    "/{approval_id}/reject",
    response_model=ApprovalRequest,
)
async def reject(
    approval_id: str, action: ApprovalAction
):
    """Reject with notes."""
    approval = _MOCK_APPROVAL.model_copy()
    approval.id = approval_id
    approval.status = "rejected"
    approval.pm_notes = action.notes or "Rejected"
    return approval
