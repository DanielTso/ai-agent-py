"""Critical Path Optimizer agent — dynamic resequencing + Monte Carlo."""

import json
import uuid
from datetime import UTC, datetime

from construction.agents.base import ConstructionAgent
from construction.schemas.common import ApprovalRequest, DataSource, ImpactSummary
from construction.tools.monte_carlo import MonteCarloSimulationTool
from construction.tools.schedule import ScheduleQueryTool


class CriticalPathOptimizer(ConstructionAgent):
    """Dynamic resequencing + Monte Carlo simulation agent."""

    name = "critical_path"
    description = "Dynamic resequencing + Monte Carlo simulation"
    schedule = "on_demand"

    def _register_tools(self) -> None:
        self._tools.register(ScheduleQueryTool())
        self._tools.register(MonteCarloSimulationTool())

    def get_system_prompt(self) -> str:
        return (
            "You are an expert CPM (Critical Path Method)"
            " scheduler for a Tier III data center"
            " construction project.\n\n"
            "CRITICAL CONSTRAINTS:\n"
            "- NEVER compromise Tier certification"
            " requirements. You cannot parallelize"
            " redundant cooling loops, redundant power"
            " paths, or any system that requires"
            " sequential commissioning for Tier"
            " certification.\n"
            "- All resequencing proposals must preserve"
            " concurrently maintainable infrastructure"
            " paths.\n\n"
            "RESPONSIBILITIES:\n"
            "1. Analyze the critical path and identify"
            " float consumption trends.\n"
            "2. Run Monte Carlo simulations to assess"
            " schedule risk.\n"
            "3. Propose resequencing options that"
            " accelerate the schedule without violating"
            " Tier constraints.\n"
            "4. Output schedule deltas with float"
            " consumption and commissioning impact.\n\n"
            "Always provide transparency on data sources"
            " and confidence levels. Request PM approval"
            " for any schedule change that consumes"
            " more than 20% of remaining float."
        )

    async def run(self, context: dict | None = None) -> "AgentEvent":  # noqa: F821
        """Analyze schedule and propose resequencing."""
        ctx = context or {}
        project_id = ctx.get("project_id", "PROJ-001")
        delay_days = ctx.get("delay_days", 0)
        affected_activities = ctx.get(
            "affected_activities", []
        )

        transparency_log = []
        data_sources = []

        # Step 1: Get critical path
        schedule_tool = self._tools.get("schedule_query")
        cp_result = schedule_tool.execute(
            action="get_critical_path",
            project_id=project_id,
        )
        cp_data = json.loads(cp_result)
        transparency_log.append(
            "Retrieved critical path from P6 schedule"
        )
        data_sources.append(DataSource(
            source_type="api",
            source_name="primavera_p6",
            retrieved_at=datetime.now(UTC),
            confidence=0.95,
        ))

        # Step 2: Get float report
        float_result = schedule_tool.execute(
            action="get_float_report",
            project_id=project_id,
        )
        float_data = json.loads(float_result)
        transparency_log.append(
            "Retrieved float report for all activities"
        )

        # Step 3: Run Monte Carlo simulation
        mc_tool = self._tools.get("monte_carlo_simulation")
        mc_result = mc_tool.execute(
            project_id=project_id,
            iterations=10000,
        )
        mc_data = json.loads(mc_result)
        transparency_log.append(
            f"Ran Monte Carlo simulation with"
            f" {mc_data['iterations']} iterations"
        )
        data_sources.append(DataSource(
            source_type="simulation",
            source_name="monte_carlo",
            retrieved_at=datetime.now(UTC),
            confidence=mc_data.get("confidence", 0.5),
        ))

        # Step 4: Analyze resequencing options
        critical_activities = cp_data.get(
            "critical_path", {}
        ).get("activities", [])
        tier_critical = [
            a for a in critical_activities
            if a.get("tier_critical")
        ]
        non_tier_critical = [
            a for a in critical_activities
            if not a.get("tier_critical")
        ]

        resequencing_options = []
        for activity in non_tier_critical:
            resequencing_options.append({
                "activity_id": activity["id"],
                "activity_name": activity["name"],
                "potential_savings_days": min(
                    delay_days, 5
                ),
                "tier_impact": "none",
                "commissioning_impact": "minimal",
            })

        transparency_log.append(
            f"Identified {len(resequencing_options)}"
            f" resequencing options;"
            f" {len(tier_critical)} tier-critical"
            f" activities protected"
        )

        # Step 5: Create approval request if needed
        approval = None
        if delay_days > 0 and resequencing_options:
            approval = ApprovalRequest(
                id=str(uuid.uuid4()),
                agent_name=self.name,
                action_type="schedule_resequence",
                title=(
                    f"Resequence to recover"
                    f" {delay_days} day delay"
                ),
                description=(
                    f"Proposed resequencing of"
                    f" {len(resequencing_options)}"
                    f" non-tier-critical activities to"
                    f" recover schedule. Tier-critical"
                    f" activities remain untouched."
                ),
                confidence=mc_data.get(
                    "confidence", 0.5
                ) * 100,
                data_sources=data_sources,
                transparency_log=transparency_log,
                impact=ImpactSummary(
                    schedule_delta_days=-min(
                        delay_days, 5
                    ),
                    description=(
                        "Potential schedule recovery via"
                        " resequencing"
                    ),
                ),
            )

        event_data = {
            "critical_path": cp_data.get(
                "critical_path", {}
            ),
            "float_report": float_data.get(
                "float_report", []
            ),
            "monte_carlo": {
                "p50": mc_data.get("p50_completion"),
                "p80": mc_data.get("p80_completion"),
                "p95": mc_data.get("p95_completion"),
                "confidence": mc_data.get("confidence"),
            },
            "resequencing_options": resequencing_options,
            "delay_context": {
                "delay_days": delay_days,
                "affected_activities": affected_activities,
            },
        }
        if approval:
            event_data["approval_request"] = (
                approval.model_dump()
            )

        severity = "info"
        if delay_days > 5:
            severity = "warning"
        if delay_days > 14:
            severity = "critical"
        if delay_days > 0 and mc_data.get(
            "confidence", 1.0
        ) < 0.3:
            severity = "critical"

        cross_agent = delay_days >= 7

        return await self.publish_event(
            event_type="schedule_analysis",
            severity=severity,
            data=event_data,
            confidence=mc_data.get("confidence", 0.5),
            data_sources=data_sources,
            transparency_log=transparency_log,
            requires_cross_agent=cross_agent,
            target_agent=(
                "risk_forecaster" if cross_agent
                else None
            ),
        )
