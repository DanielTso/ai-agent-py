"""Celery application for scheduled agent tasks."""

from celery import Celery

from construction.config import get_construction_settings

settings = get_construction_settings()

celery_app = Celery(
    "construction_pm",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

# Import tasks so they're registered
celery_app.autodiscover_tasks(["construction.tasks"])
