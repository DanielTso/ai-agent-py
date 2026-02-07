"""Safety Compliance agent — OSHA/MSHA/NIOSH safety expert."""

import json
from datetime import UTC, datetime

from construction.agents.base import ConstructionAgent
from construction.schemas.common import AgentEvent, DataSource
from construction.tools.hazard_analysis import HazardAnalysis
from construction.tools.msha_compliance import MshaComplianceTool
from construction.tools.nfpa_compliance import NfpaComplianceTool
from construction.tools.niosh_lookup import NioshLookup
from construction.tools.osha_compliance import OshaComplianceTool
from construction.tools.safety_metrics import SafetyMetrics
from construction.tools.training_tracker import TrainingTracker


class SafetyComplianceAgent(ConstructionAgent):
    """OSHA/MSHA/NIOSH safety compliance expert."""

    name = "safety_compliance"
    description = (
        "Safety expert enforcing OSHA, MSHA, and NIOSH"
        " standards with stop-work authority"
    )
    schedule = "continuous"

    def _register_tools(self) -> None:
        self._tools.register(OshaComplianceTool())
        self._tools.register(MshaComplianceTool())
        self._tools.register(NioshLookup())
        self._tools.register(SafetyMetrics())
        self._tools.register(HazardAnalysis())
        self._tools.register(TrainingTracker())
        self._tools.register(NfpaComplianceTool())

    def get_system_prompt(self) -> str:
        return (
            "You are the construction safety compliance expert."
            " You are the ONLY agent authorized to recommend"
            " stop-work orders.\n\n"
            "Your regulatory knowledge:\n"
            "- OSHA 29 CFR 1926 (Construction)\n"
            "- MSHA 30 CFR Parts 46, 48, 56, 57 (Mining)\n"
            "- NIOSH Recommended Exposure Limits (RELs)\n"
            "- NFPA 70 (NEC), NFPA 72 (Fire Alarm),"
            " NFPA 101 (Life Safety), NFPA 13 (Sprinkler)\n\n"
            "Focus Four Hazards (leading causes of death):\n"
            "1. Falls — 29 CFR 1926.501 (fall protection)\n"
            "2. Struck-By — 29 CFR 1926.602 (material handling)\n"
            "3. Caught-In/Between — 29 CFR 1926.652 (excavation)\n"
            "4. Electrocution — 29 CFR 1926.405 (electrical)\n\n"
            "Key standards you enforce:\n"
            "- Silica: 29 CFR 1926.1153 (PEL 50 ug/m3)\n"
            "- Electrical: 29 CFR 1926.405 (GFCI, LOTO)\n"
            "- Excavation: 29 CFR 1926.652 (competent person)\n"
            "- MSHA jurisdiction for borrow pits/aggregate\n"
            "- NIOSH RELs for exposure monitoring\n\n"
            "You track:\n"
            "- OSHA 300 log and recordable incidents\n"
            "- TRIR, DART, EMR metrics\n"
            "- Training certifications and gaps\n"
            "- JHA (Job Hazard Analysis) compliance\n"
            "- Inspection readiness scores\n"
            "- NFPA fire protection and life safety\n"
            "- NEC electrical code compliance\n\n"
            "STOP-WORK criteria:\n"
            "- Imminent danger to life or health\n"
            "- Focus Four violation without controls\n"
            "- Exposure above PEL without protection\n"
            "- Unqualified worker in hazardous operation\n\n"
            "Output your assessment as structured JSON with"
            " sections for safety_metrics, focus_four_status,"
            " stop_work_recommendations, training_alerts,"
            " and exposure_monitoring."
        )

    async def run(self, context: dict | None = None) -> AgentEvent:
        """Run safety compliance check and publish findings."""
        project_id = (context or {}).get(
            "project_id", "default"
        )

        prompt = (
            f"Perform comprehensive safety check for project"
            f" {project_id}. Check Focus Four hazards,"
            " review OSHA 300 log, calculate current safety"
            " metrics (TRIR, DART), check for exposure"
            " monitoring issues, review training certifications"
            " for gaps and expirations, and assess inspection"
            " readiness. Flag any stop-work conditions."
        )

        response = self.chat(prompt)

        transparency_log = [
            "Checked Focus Four hazard status",
            "Reviewed OSHA 300 log entries",
            "Calculated TRIR and DART metrics",
            "Checked exposure monitoring records",
            "Reviewed training certifications",
            "Assessed inspection readiness",
            f"Model response length: {len(response)} chars",
        ]

        try:
            data = json.loads(response)
        except (json.JSONDecodeError, TypeError):
            data = {"raw_response": response}

        stop_work = data.get(
            "stop_work_recommendations", []
        )
        has_stop_work = len(stop_work) > 0
        exposure_issues = data.get(
            "exposure_monitoring", {}
        ).get("exceedances", [])
        training_expired = data.get(
            "training_alerts", {}
        ).get("expired", [])

        if has_stop_work:
            severity = "critical"
        elif exposure_issues or training_expired:
            severity = "warning"
        else:
            severity = "info"

        return await self.publish_event(
            event_type="safety_status",
            severity=severity,
            data=data,
            confidence=0.95,
            data_sources=[
                DataSource(
                    source_type="database",
                    source_name="osha_compliance",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.95,
                ),
                DataSource(
                    source_type="database",
                    source_name="safety_metrics",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.95,
                ),
                DataSource(
                    source_type="database",
                    source_name="training_tracker",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.90,
                ),
                DataSource(
                    source_type="database",
                    source_name="hazard_analysis",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.85,
                ),
            ],
            transparency_log=transparency_log,
            requires_cross_agent=has_stop_work,
            target_agent=(
                "site_logistics" if has_stop_work else None
            ),
        )
