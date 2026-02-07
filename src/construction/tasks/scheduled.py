"""Scheduled Celery tasks for all construction agents."""

import asyncio
import logging

from celery.schedules import crontab

from construction.config import get_construction_settings
from construction.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


def _run_async(coro):
    """Helper to run async code in Celery synchronous tasks."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(name="agents.risk_forecaster")
def run_risk_forecaster(project_id: str = "default"):
    """Run Risk Forecaster agent -- hourly."""
    logger.info("Running risk_forecaster for project %s", project_id)
    from construction.agents.risk_forecaster import RiskForecasterAgent

    agent = RiskForecasterAgent()
    result = _run_async(agent.run({"project_id": project_id}))
    return {
        "agent": "risk_forecaster",
        "status": "completed",
        "event_type": result.event_type,
    }


@celery_app.task(name="agents.supply_chain")
def run_supply_chain(project_id: str = "default"):
    """Run Supply Chain agent -- every 4 hours."""
    logger.info("Running supply_chain for project %s", project_id)
    from construction.agents.supply_chain import SupplyChainAgent

    agent = SupplyChainAgent()
    result = _run_async(agent.run({"project_id": project_id}))
    return {
        "agent": "supply_chain",
        "status": "completed",
        "event_type": result.event_type,
    }


@celery_app.task(name="agents.compliance_verifier")
def run_compliance_verifier(project_id: str = "default"):
    """Run Compliance Verifier -- twice daily."""
    logger.info("Running compliance_verifier for project %s", project_id)
    from construction.agents.compliance_verifier import ComplianceVerifierAgent

    agent = ComplianceVerifierAgent()
    result = _run_async(agent.run({"project_id": project_id}))
    return {
        "agent": "compliance_verifier",
        "status": "completed",
        "event_type": result.event_type,
    }


@celery_app.task(name="agents.financial_intelligence")
def run_financial_intelligence(project_id: str = "default"):
    """Run Financial Intelligence -- daily."""
    logger.info("Running financial_intelligence for project %s", project_id)
    from construction.agents.financial_intelligence import (
        FinancialIntelligenceAgent,
    )

    agent = FinancialIntelligenceAgent()
    result = _run_async(agent.run({"project_id": project_id}))
    return {
        "agent": "financial_intelligence",
        "status": "completed",
        "event_type": result.event_type,
    }


@celery_app.task(name="agents.workforce_labor")
def run_workforce_labor(project_id: str = "default"):
    """Run Workforce & Labor -- daily."""
    logger.info("Running workforce_labor for project %s", project_id)
    from construction.agents.workforce_labor import WorkforceLaborAgent

    agent = WorkforceLaborAgent()
    result = _run_async(agent.run({"project_id": project_id}))
    return {
        "agent": "workforce_labor",
        "status": "completed",
        "event_type": result.event_type,
    }


@celery_app.task(name="agents.commissioning_turnover")
def run_commissioning_turnover(project_id: str = "default"):
    """Run Commissioning & Turnover -- daily."""
    logger.info("Running commissioning_turnover for project %s", project_id)
    from construction.agents.commissioning_turnover import (
        CommissioningTurnoverAgent,
    )

    agent = CommissioningTurnoverAgent()
    result = _run_async(agent.run({"project_id": project_id}))
    return {
        "agent": "commissioning_turnover",
        "status": "completed",
        "event_type": result.event_type,
    }


@celery_app.task(name="agents.environmental_sustainability")
def run_environmental_sustainability(project_id: str = "default"):
    """Run Environmental & Sustainability -- daily."""
    logger.info(
        "Running environmental_sustainability for project %s",
        project_id,
    )
    from construction.agents.environmental_sustainability import (
        EnvironmentalSustainabilityAgent,
    )

    agent = EnvironmentalSustainabilityAgent()
    result = _run_async(agent.run({"project_id": project_id}))
    return {
        "agent": "environmental_sustainability",
        "status": "completed",
        "event_type": result.event_type,
    }


@celery_app.task(name="agents.safety_compliance")
def run_safety_compliance(project_id: str = "default"):
    """Run Safety Compliance -- continuous + daily briefing."""
    logger.info("Running safety_compliance for project %s", project_id)
    from construction.agents.safety_compliance import (
        SafetyComplianceAgent,
    )

    agent = SafetyComplianceAgent()
    result = _run_async(agent.run({"project_id": project_id}))
    return {
        "agent": "safety_compliance",
        "status": "completed",
        "event_type": result.event_type,
    }


@celery_app.task(name="agents.site_logistics")
def run_site_logistics(project_id: str = "default"):
    """Run Site Logistics -- real-time."""
    logger.info("Running site_logistics for project %s", project_id)
    from construction.agents.site_logistics import SiteLogisticsAgent

    agent = SiteLogisticsAgent()
    result = _run_async(agent.run({"project_id": project_id}))
    return {
        "agent": "site_logistics",
        "status": "completed",
        "event_type": result.event_type,
    }


@celery_app.task(name="agents.claims_dispute")
def run_claims_dispute(project_id: str = "default"):
    """Run Claims & Dispute Prevention -- continuous (event-driven)."""
    logger.info("Running claims_dispute for project %s", project_id)
    from construction.agents.claims_dispute import ClaimsDisputeAgent

    agent = ClaimsDisputeAgent()
    result = _run_async(agent.run({"project_id": project_id}))
    return {
        "agent": "claims_dispute",
        "status": "completed",
        "event_type": result.event_type,
    }


@celery_app.task(name="orchestrator.daily_brief")
def generate_daily_brief(project_id: str = "default"):
    """Generate 6AM Daily Command Brief."""
    logger.info("Generating daily brief for project %s", project_id)
    from construction.agents.orchestrator import Orchestrator

    orchestrator = Orchestrator(
        settings=get_construction_settings(),
        shared_memory=None,
        pubsub=None,
        agents={},
    )
    result = _run_async(orchestrator.generate_daily_brief(project_id))
    return {
        "brief_date": str(result.brief_date),
        "status": "generated",
    }


# Celery Beat schedule
celery_app.conf.beat_schedule = {
    "risk-forecaster-hourly": {
        "task": "agents.risk_forecaster",
        "schedule": 3600.0,  # Every hour
    },
    "supply-chain-4h": {
        "task": "agents.supply_chain",
        "schedule": 14400.0,  # Every 4 hours
    },
    "compliance-verifier-12h": {
        "task": "agents.compliance_verifier",
        "schedule": 43200.0,  # Twice daily
    },
    "financial-intelligence-daily": {
        "task": "agents.financial_intelligence",
        "schedule": 86400.0,  # Daily
    },
    "workforce-labor-daily": {
        "task": "agents.workforce_labor",
        "schedule": 86400.0,  # Daily
    },
    "commissioning-turnover-daily": {
        "task": "agents.commissioning_turnover",
        "schedule": 86400.0,  # Daily
    },
    "environmental-sustainability-daily": {
        "task": "agents.environmental_sustainability",
        "schedule": 86400.0,  # Daily
    },
    "safety-compliance-15min": {
        "task": "agents.safety_compliance",
        "schedule": 900.0,  # Every 15 minutes (continuous)
    },
    "site-logistics-5min": {
        "task": "agents.site_logistics",
        "schedule": 300.0,  # Every 5 minutes (real-time)
    },
    "claims-dispute-30min": {
        "task": "agents.claims_dispute",
        "schedule": 1800.0,  # Every 30 minutes (continuous)
    },
    "daily-brief-6am": {
        "task": "orchestrator.daily_brief",
        "schedule": crontab(hour=6, minute=0),
    },
}
