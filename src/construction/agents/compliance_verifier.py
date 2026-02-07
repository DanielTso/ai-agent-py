"""Compliance Verifier agent — BIM + code compliance checking."""

import json
from datetime import UTC, datetime

from construction.agents.base import ConstructionAgent
from construction.schemas.common import DataSource
from construction.tools.bim import BIMQueryTool
from construction.tools.compliance_db import ComplianceDatabaseTool
from construction.tools.icc_codes import IccCodesTool
from construction.tools.tier_certification import TierCertification


class ComplianceVerifier(ConstructionAgent):
    """Verify installations against BIM models and building codes."""

    name = "compliance_verifier"
    description = "Verify installations against BIM + codes"
    schedule = "twice_daily"

    def _register_tools(self) -> None:
        self._tools.register(BIMQueryTool())
        self._tools.register(ComplianceDatabaseTool())
        self._tools.register(IccCodesTool())
        self._tools.register(TierCertification())

    def get_system_prompt(self) -> str:
        return (
            "You are a BIM and building code compliance"
            " expert for a Tier III data center"
            " construction project.\n\n"
            "RESPONSIBILITIES:\n"
            "1. Check redundancy path continuity for"
            " all critical systems (power, cooling,"
            " network).\n"
            "2. Verify fire separation ratings meet"
            " code requirements.\n"
            "3. Validate egress clearances against"
            " IBC/NFPA standards.\n"
            "4. Compare field installations against"
            " BIM model specifications.\n"
            "5. Create deviation tickets for any"
            " non-conformance with BIM overlay"
            " visualization and severity rating.\n"
            "6. Verify ICC building code compliance"
            " (IBC, IFC, IMC, IPC, IECC).\n"
            "7. Verify Uptime Institute Tier"
            " certification requirements (redundancy,"
            " concurrent maintainability, fault"
            " tolerance).\n\n"
            "SEVERITY CLASSIFICATION:\n"
            "- critical: Tier certification impact,"
            " life safety, or code violation\n"
            "- major: Significant deviation requiring"
            " engineering review\n"
            "- minor: Cosmetic or non-structural"
            " deviation\n"
            "- info: Observation, no action required\n\n"
            "Always provide transparency on what was"
            " checked and data source confidence."
        )

    async def run(self, context: dict | None = None) -> "AgentEvent":  # noqa: F821
        """Run compliance checks and create deviation tickets."""
        ctx = context or {}
        project_id = ctx.get("project_id", "PROJ-001")
        check_types = ctx.get(
            "check_types",
            ["fire_separation", "redundancy_path", "egress"],
        )

        transparency_log = []
        data_sources = []

        # Step 1: Run BIM compliance checks
        bim_tool = self._tools.get("bim_query")
        all_checks = []

        for check_type in check_types:
            result = bim_tool.execute(
                action="check_compliance",
                project_id=project_id,
                check_type=check_type,
            )
            check_data = json.loads(result)
            all_checks.extend(
                check_data.get("checks", [])
            )
            transparency_log.append(
                f"Ran {check_type} compliance check"
                f" via BIM model"
            )

        data_sources.append(DataSource(
            source_type="api",
            source_name="autodesk_bim360",
            retrieved_at=datetime.now(UTC),
            confidence=0.92,
        ))

        # Step 2: Get existing deviations
        deviation_result = bim_tool.execute(
            action="get_deviations",
            project_id=project_id,
        )
        deviation_data = json.loads(deviation_result)
        transparency_log.append(
            "Retrieved existing BIM deviations"
        )

        # Step 3: Create tickets for critical/major issues
        compliance_tool = self._tools.get(
            "compliance_database"
        )
        critical_checks = [
            c for c in all_checks
            if c.get("severity") in ("critical", "major")
        ]
        tickets_created = []

        for check in critical_checks:
            ticket_result = compliance_tool.execute(
                action="create",
                project_id=project_id,
                data={
                    "check_type": check.get("check_type"),
                    "severity": check.get("severity"),
                    "bim_element_id": check.get(
                        "bim_element_id"
                    ),
                    "location": check.get("location"),
                    "description": check.get(
                        "description"
                    ),
                    "measured_value": check.get(
                        "measured_value"
                    ),
                    "required_value": check.get(
                        "required_value"
                    ),
                },
            )
            ticket_data = json.loads(ticket_result)
            tickets_created.append(ticket_data)
            transparency_log.append(
                f"Created ticket {ticket_data['check_id']}"
                f" for {check.get('check_type')}"
                f" ({check.get('severity')})"
            )

        data_sources.append(DataSource(
            source_type="database",
            source_name="compliance_database",
            retrieved_at=datetime.now(UTC),
            confidence=1.0,
        ))

        # Step 4: Get summary
        summary_result = compliance_tool.execute(
            action="get_summary",
            project_id=project_id,
        )
        summary_data = json.loads(summary_result)

        critical_count = len([
            c for c in all_checks
            if c.get("severity") == "critical"
        ])
        major_count = len([
            c for c in all_checks
            if c.get("severity") == "major"
        ])

        event_data = {
            "checks_performed": len(all_checks),
            "checks": all_checks,
            "deviations": deviation_data.get(
                "deviations", []
            ),
            "tickets_created": tickets_created,
            "summary": summary_data,
            "critical_count": critical_count,
            "major_count": major_count,
        }

        severity = "info"
        if major_count > 0:
            severity = "warning"
        if critical_count > 0:
            severity = "critical"

        return await self.publish_event(
            event_type="compliance_check",
            severity=severity,
            data=event_data,
            confidence=0.92,
            data_sources=data_sources,
            transparency_log=transparency_log,
            requires_cross_agent=critical_count > 0,
            target_agent=(
                "critical_path" if critical_count > 0
                else None
            ),
        )
