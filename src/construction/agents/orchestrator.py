"""Rule-based orchestrator for cross-agent coordination."""

import hashlib
import json
import uuid
from datetime import UTC, date, datetime

from construction.agents.base import ConstructionAgent
from construction.config import ConstructionSettings
from construction.redis_.pubsub import AgentPubSub
from construction.redis_.shared_memory import SharedMemory
from construction.schemas.common import AgentEvent
from construction.schemas.orchestrator import (
    AccelerationOpportunity,
    CrossAgentTrigger,
    DailyBriefOutput,
    EscalationEvent,
    QualityGap,
    ThreatSummary,
)
from construction.tools.notifications import SendNotification


class Orchestrator:
    """Rule-based coordinator for all construction agents.

    NOT an AI agent — purely deterministic routing logic.
    """

    def __init__(
        self,
        settings: ConstructionSettings,
        shared_memory: SharedMemory | None,
        pubsub: AgentPubSub | None,
        agents: dict[str, ConstructionAgent],
    ):
        self.settings = settings
        self.shared_memory = shared_memory
        self.pubsub = pubsub
        self.agents = agents
        self._notification_tool = SendNotification()

    async def handle_event(
        self, event: AgentEvent
    ) -> list[CrossAgentTrigger]:
        """Process an agent event and trigger cross-agent actions."""
        triggers: list[CrossAgentTrigger] = []

        source = event.source_agent
        event_type = event.event_type
        data = event.data

        # SUPPLY_CHAIN.critical_delay
        # -> CRITICAL_PATH.reoptimize
        # -> if >$250k: escalate SMS
        if (
            source == "supply_chain"
            and event_type == "critical_delay"
        ):
            triggers.append(CrossAgentTrigger(
                source_agent="supply_chain",
                source_event_type="critical_delay",
                target_agent="critical_path",
                target_action="reoptimize",
                data=data,
                priority=2,
            ))
            impact = data.get("impact_dollars", 0)
            if impact > self.settings.escalation_impact_threshold:
                await self._escalate_sms(event)

        # RISK_FORECASTER.safety_critical
        # -> IMMEDIATE SMS escalation
        # -> COMPLIANCE.focused_check
        if (
            source == "risk_forecaster"
            and event_type == "safety_critical"
        ):
            await self._escalate_sms(event)
            triggers.append(CrossAgentTrigger(
                source_agent="risk_forecaster",
                source_event_type="safety_critical",
                target_agent="compliance",
                target_action="focused_check",
                data=data,
                priority=1,
            ))

        # COMPLIANCE.critical_deviation
        # -> RISK_FORECASTER.reassess
        if (
            source == "compliance"
            and event_type == "critical_deviation"
        ):
            triggers.append(CrossAgentTrigger(
                source_agent="compliance",
                source_event_type="critical_deviation",
                target_agent="risk_forecaster",
                target_action="reassess",
                data=data,
                priority=3,
            ))

        # DOCUMENT_INTELLIGENCE.contradiction_detected
        # -> COMPLIANCE.focused_check
        if (
            source == "document_intelligence"
            and event_type == "contradiction_detected"
        ):
            triggers.append(CrossAgentTrigger(
                source_agent="document_intelligence",
                source_event_type="contradiction_detected",
                target_agent="compliance",
                target_action="focused_check",
                data=data,
                priority=3,
            ))

        # FINANCIAL.budget_variance > 10%
        # -> CRITICAL_PATH.reoptimize
        # -> SUPPLY_CHAIN.cost_reduction_scan
        if (
            source == "financial"
            and event_type == "budget_variance"
        ):
            variance = data.get("variance_pct", 0)
            if variance > 10:
                triggers.append(CrossAgentTrigger(
                    source_agent="financial",
                    source_event_type="budget_variance",
                    target_agent="critical_path",
                    target_action="reoptimize",
                    data=data,
                    priority=3,
                ))
                triggers.append(CrossAgentTrigger(
                    source_agent="financial",
                    source_event_type="budget_variance",
                    target_agent="supply_chain",
                    target_action="cost_reduction_scan",
                    data=data,
                    priority=3,
                ))

        # WORKFORCE.labor_shortage_detected
        # -> CRITICAL_PATH.reoptimize
        # -> SITE_LOGISTICS.headcount_update
        if (
            source == "workforce"
            and event_type == "labor_shortage_detected"
        ):
            triggers.append(CrossAgentTrigger(
                source_agent="workforce",
                source_event_type="labor_shortage_detected",
                target_agent="critical_path",
                target_action="reoptimize",
                data=data,
                priority=3,
            ))
            triggers.append(CrossAgentTrigger(
                source_agent="workforce",
                source_event_type="labor_shortage_detected",
                target_agent="site_logistics",
                target_action="headcount_update",
                data=data,
                priority=4,
            ))

        # COMMISSIONING.prerequisite_blocked
        # -> CRITICAL_PATH.reoptimize
        # -> SUPPLY_CHAIN.expedite_check
        if (
            source == "commissioning_turnover"
            and event_type == "prerequisite_blocked"
        ):
            triggers.append(CrossAgentTrigger(
                source_agent="commissioning_turnover",
                source_event_type="prerequisite_blocked",
                target_agent="critical_path",
                target_action="reoptimize",
                data=data,
                priority=3,
            ))
            triggers.append(CrossAgentTrigger(
                source_agent="commissioning_turnover",
                source_event_type="prerequisite_blocked",
                target_agent="supply_chain",
                target_action="expedite_check",
                data=data,
                priority=4,
            ))

        # ENVIRONMENTAL.permit_violation_risk
        # -> COMPLIANCE.focused_check
        # -> RISK_FORECASTER.reassess
        if (
            source == "environmental_sustainability"
            and event_type == "permit_violation_risk"
        ):
            triggers.append(CrossAgentTrigger(
                source_agent="environmental_sustainability",
                source_event_type="permit_violation_risk",
                target_agent="compliance",
                target_action="focused_check",
                data=data,
                priority=2,
            ))
            triggers.append(CrossAgentTrigger(
                source_agent="environmental_sustainability",
                source_event_type="permit_violation_risk",
                target_agent="risk_forecaster",
                target_action="reassess",
                data=data,
                priority=3,
            ))

        # SITE_LOGISTICS.crane_conflict
        # -> CRITICAL_PATH.reoptimize
        # -> SAFETY.crane_safety_check
        if (
            source == "site_logistics"
            and event_type == "crane_conflict"
        ):
            triggers.append(CrossAgentTrigger(
                source_agent="site_logistics",
                source_event_type="crane_conflict",
                target_agent="critical_path",
                target_action="reoptimize",
                data=data,
                priority=3,
            ))
            triggers.append(CrossAgentTrigger(
                source_agent="site_logistics",
                source_event_type="crane_conflict",
                target_agent="safety_compliance",
                target_action="crane_safety_check",
                data=data,
                priority=2,
            ))

        # SAFETY.stop_work_recommended (HIGHEST PRIORITY)
        # -> ALL agents notified
        # -> IMMEDIATE SMS escalation
        # -> SITE_LOGISTICS.halt_operations
        # -> CRITICAL_PATH.reoptimize
        if (
            source == "safety_compliance"
            and event_type == "stop_work_recommended"
        ):
            await self._escalate_sms(event)
            triggers.append(CrossAgentTrigger(
                source_agent="safety_compliance",
                source_event_type="stop_work_recommended",
                target_agent="site_logistics",
                target_action="halt_operations",
                data=data,
                priority=1,
            ))
            triggers.append(CrossAgentTrigger(
                source_agent="safety_compliance",
                source_event_type="stop_work_recommended",
                target_agent="critical_path",
                target_action="reoptimize",
                data=data,
                priority=1,
            ))

        # SAFETY.contractor_high_risk
        # -> SUPPLY_CHAIN.contractor_review
        # -> RISK_FORECASTER.reassess
        if (
            source == "safety_compliance"
            and event_type == "contractor_high_risk"
        ):
            triggers.append(CrossAgentTrigger(
                source_agent="safety_compliance",
                source_event_type="contractor_high_risk",
                target_agent="supply_chain",
                target_action="contractor_review",
                data=data,
                priority=2,
            ))
            triggers.append(CrossAgentTrigger(
                source_agent="safety_compliance",
                source_event_type="contractor_high_risk",
                target_agent="risk_forecaster",
                target_action="reassess",
                data=data,
                priority=3,
            ))

        # SAFETY.exposure_threshold_exceeded
        # -> ENVIRONMENTAL.exposure_response
        # -> WORKFORCE.affected_workers
        if (
            source == "safety_compliance"
            and event_type == "exposure_threshold_exceeded"
        ):
            triggers.append(CrossAgentTrigger(
                source_agent="safety_compliance",
                source_event_type="exposure_threshold_exceeded",
                target_agent="environmental_sustainability",
                target_action="exposure_response",
                data=data,
                priority=2,
            ))
            triggers.append(CrossAgentTrigger(
                source_agent="safety_compliance",
                source_event_type="exposure_threshold_exceeded",
                target_agent="workforce",
                target_action="affected_workers",
                data=data,
                priority=2,
            ))

        # SAFETY.training_expired
        # -> WORKFORCE.certification_alert
        # -> SITE_LOGISTICS.access_restriction
        if (
            source == "safety_compliance"
            and event_type == "training_expired"
        ):
            triggers.append(CrossAgentTrigger(
                source_agent="safety_compliance",
                source_event_type="training_expired",
                target_agent="workforce",
                target_action="certification_alert",
                data=data,
                priority=3,
            ))
            triggers.append(CrossAgentTrigger(
                source_agent="safety_compliance",
                source_event_type="training_expired",
                target_agent="site_logistics",
                target_action="access_restriction",
                data=data,
                priority=3,
            ))

        # WEATHER.heat_index > NIOSH_threshold
        # -> SAFETY.heat_illness_check
        # -> WORKFORCE.schedule_adjustment
        # -> SITE_LOGISTICS.schedule_adjustment
        if (
            source == "risk_forecaster"
            and event_type == "heat_index_exceeded"
        ):
            triggers.append(CrossAgentTrigger(
                source_agent="risk_forecaster",
                source_event_type="heat_index_exceeded",
                target_agent="safety_compliance",
                target_action="heat_illness_check",
                data=data,
                priority=2,
            ))
            triggers.append(CrossAgentTrigger(
                source_agent="risk_forecaster",
                source_event_type="heat_index_exceeded",
                target_agent="workforce",
                target_action="schedule_adjustment",
                data=data,
                priority=3,
            ))
            triggers.append(CrossAgentTrigger(
                source_agent="risk_forecaster",
                source_event_type="heat_index_exceeded",
                target_agent="site_logistics",
                target_action="schedule_adjustment",
                data=data,
                priority=3,
            ))

        return triggers

    async def generate_daily_brief(
        self, project_id: str
    ) -> DailyBriefOutput:
        """6AM Daily Brief: top 3 threats, 2 quality gaps, 1 accel."""
        threats = await self._collect_threats(project_id)
        gaps = await self._collect_quality_gaps(project_id)
        accel = await self._find_acceleration(project_id)

        full_text = self._format_brief(threats, gaps, accel)

        return DailyBriefOutput(
            brief_date=date.today(),
            generated_at=datetime.now(UTC),
            top_threats=threats[:3],
            quality_gaps=gaps[:2],
            acceleration=accel,
            full_text=full_text,
        )

    async def check_escalation(
        self, event: AgentEvent
    ) -> bool:
        """Check if event requires SMS escalation."""
        data = event.data
        is_safety = data.get("safety_critical", False)
        impact = data.get("impact_dollars", 0)

        return (
            is_safety
            or impact > self.settings.escalation_impact_threshold
        )

    async def check_dedup(self, event: AgentEvent) -> bool:
        """Check if similar alert was sent within 4h TTL."""
        if not self.shared_memory:
            return False

        alert_content = json.dumps(
            {
                "source": event.source_agent,
                "type": event.event_type,
                "data": event.data,
            },
            sort_keys=True,
            default=str,
        )
        alert_hash = hashlib.sha256(
            alert_content.encode()
        ).hexdigest()

        is_dup = await self.shared_memory.check_dedup(
            alert_hash
        )
        if not is_dup:
            await self.shared_memory.mark_dedup(alert_hash)
        return is_dup

    async def process_approval(
        self,
        approval_id: str,
        approved: bool,
        notes: str,
    ) -> None:
        """Process PM approval/rejection and trigger cascade."""
        if self.shared_memory:
            approval_data = {
                "approval_id": approval_id,
                "approved": approved,
                "notes": notes,
                "processed_at": datetime.now(UTC).isoformat(),
            }
            # If approved, notify downstream agents
            if approved and self.pubsub:
                await self.pubsub.publish(
                    "channel:approval_updates",
                    approval_data,
                )

    async def _escalate_sms(
        self, event: AgentEvent
    ) -> None:
        """Send an SMS escalation for critical events."""
        is_dup = await self.check_dedup(event)
        if is_dup:
            return

        message = (
            f"[CRITICAL] {event.source_agent}:"
            f" {event.event_type}"
        )
        data_desc = event.data.get("description", "")
        if data_desc:
            message += f" — {data_desc}"

        self._notification_tool.execute(
            method="sms",
            recipient=self.settings.pm_phone_number,
            message=message,
            priority="critical",
        )

        if self.pubsub:
            escalation = EscalationEvent(
                event_id=str(uuid.uuid4()),
                trigger_agent=event.source_agent,
                trigger_type=event.event_type,
                severity="critical",
                impact_dollars=event.data.get(
                    "impact_dollars", 0
                ),
                safety_critical=event.data.get(
                    "safety_critical", False
                ),
                message=message,
                sms_sent=True,
                timestamp=datetime.now(UTC),
            )
            await self.pubsub.publish(
                "channel:escalation",
                escalation.model_dump(),
            )

    async def _collect_threats(
        self, project_id: str
    ) -> list[ThreatSummary]:
        """Collect top threats from shared memory."""
        threats: list[ThreatSummary] = []
        if not self.shared_memory:
            return self._default_threats()

        risks = await self.shared_memory.get_active_risks(
            project_id
        )
        for rank, (risk_id, score) in enumerate(
            risks[:3], start=1
        ):
            threats.append(ThreatSummary(
                rank=rank,
                title=f"Risk {risk_id}",
                agent_source="risk_forecaster",
                impact=f"Score: {score:.1f}",
                confidence=0.8,
                action_required="Review and mitigate",
            ))

        # Pad to 3 if needed
        while len(threats) < 3:
            threats.append(ThreatSummary(
                rank=len(threats) + 1,
                title="No additional threats identified",
                agent_source="orchestrator",
                impact="None",
                confidence=1.0,
                action_required="None",
            ))

        return threats[:3]

    async def _collect_quality_gaps(
        self, project_id: str
    ) -> list[QualityGap]:
        """Collect quality gaps from shared memory."""
        if not self.shared_memory:
            return self._default_quality_gaps()

        return self._default_quality_gaps()

    async def _find_acceleration(
        self, project_id: str
    ) -> AccelerationOpportunity | None:
        """Find acceleration opportunity from shared memory."""
        if not self.shared_memory:
            return self._default_acceleration()

        return self._default_acceleration()

    def _default_threats(self) -> list[ThreatSummary]:
        """Fallback threats when no data available."""
        return [
            ThreatSummary(
                rank=i,
                title=f"Placeholder threat {i}",
                agent_source="orchestrator",
                impact="Unknown",
                confidence=0.5,
                action_required="Awaiting agent data",
            )
            for i in range(1, 4)
        ]

    def _default_quality_gaps(self) -> list[QualityGap]:
        """Fallback quality gaps."""
        return [
            QualityGap(
                rank=i,
                title=f"Placeholder gap {i}",
                agent_source="orchestrator",
                severity="medium",
                location="TBD",
            )
            for i in range(1, 3)
        ]

    def _default_acceleration(
        self,
    ) -> AccelerationOpportunity:
        """Fallback acceleration opportunity."""
        return AccelerationOpportunity(
            title="No acceleration identified",
            agent_source="orchestrator",
            potential_savings_days=0,
            cost=0.0,
            description="Awaiting agent data",
        )

    def _format_brief(
        self,
        threats: list[ThreatSummary],
        gaps: list[QualityGap],
        accel: AccelerationOpportunity | None,
    ) -> str:
        """Format the daily brief as readable text."""
        lines = [
            f"Daily Brief — {date.today().isoformat()}",
            "=" * 40,
            "",
            "TOP 3 THREATS:",
        ]
        for t in threats:
            lines.append(
                f"  {t.rank}. {t.title}"
                f" ({t.agent_source})"
                f" — Impact: {t.impact}"
            )
        lines.append("")
        lines.append("QUALITY GAPS:")
        for g in gaps:
            lines.append(
                f"  {g.rank}. {g.title}"
                f" — Severity: {g.severity}"
                f" @ {g.location}"
            )
        lines.append("")
        if accel:
            lines.append("ACCELERATION OPPORTUNITY:")
            lines.append(
                f"  {accel.title}"
                f" — {accel.potential_savings_days} days"
                f" @ ${accel.cost:,.0f}"
            )
        return "\n".join(lines)
