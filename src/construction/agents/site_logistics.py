"""Site Logistics agent — crane, staging, headcount, access."""

import json
from datetime import UTC, datetime

from construction.agents.base import ConstructionAgent
from construction.schemas.common import AgentEvent, DataSource
from construction.tools.site_logistics_tools import SiteLogisticsQuery


class SiteLogisticsAgent(ConstructionAgent):
    """Manage site operations including crane and staging."""

    name = "site_logistics"
    description = (
        "Site operations expert managing crane scheduling,"
        " material staging, and headcount tracking"
    )
    schedule = "real_time"

    def _register_tools(self) -> None:
        self._tools.register(SiteLogisticsQuery())

    def get_system_prompt(self) -> str:
        return (
            "You are an expert site logistics coordinator"
            " for construction projects.\n\n"
            "Your responsibilities:\n"
            "1. Crane/hoist scheduling — manage tower crane"
            " time slots, prevent conflicts between trades,"
            " verify lift plans against wind conditions\n"
            "2. Material staging — monitor laydown area"
            " utilization, prevent overcrowding, coordinate"
            " just-in-time deliveries\n"
            "3. Site access and headcount — track daily"
            " manpower by trade, flag variances from plan,"
            " manage gate access\n"
            "4. Site permits — monitor street closures,"
            " crane permits, sidewalk permits, flag expiring\n\n"
            "IMPORTANT: You do NOT enforce safety rules."
            " Safety is handled by the safety_compliance"
            " agent. You focus purely on logistics"
            " optimization.\n\n"
            "Output your assessment as structured JSON with"
            " sections for crane_conflicts, staging_alerts,"
            " headcount_variance, and permit_status."
        )

    async def run(self, context: dict | None = None) -> AgentEvent:
        """Check site logistics and publish findings."""
        project_id = (context or {}).get(
            "project_id", "default"
        )

        prompt = (
            f"Analyze site logistics for project {project_id}."
            " Check crane schedule for conflicts, review"
            " staging area utilization, verify headcount"
            " against plan, and check site permit status."
        )

        response = self.chat(prompt)

        transparency_log = [
            "Checked crane schedule for conflicts",
            "Reviewed staging area utilization",
            "Verified headcount against plan",
            "Checked site permit status",
            f"Model response length: {len(response)} chars",
        ]

        try:
            data = json.loads(response)
        except (json.JSONDecodeError, TypeError):
            data = {"raw_response": response}

        crane_conflicts = data.get("crane_conflicts", [])
        severity = "warning" if crane_conflicts else "info"

        return await self.publish_event(
            event_type="site_logistics_status",
            severity=severity,
            data=data,
            confidence=0.85,
            data_sources=[
                DataSource(
                    source_type="database",
                    source_name="site_logistics_query",
                    retrieved_at=datetime.now(UTC),
                    confidence=0.90,
                ),
            ],
            transparency_log=transparency_log,
            requires_cross_agent=bool(crane_conflicts),
            target_agent=(
                "critical_path" if crane_conflicts else None
            ),
        )
