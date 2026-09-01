from celery import Celery

from stone_site.core.config import settings

celery_app = Celery(
    "stone_site_tasks",
    broker = settings.RABBITMQ_URL,
    backend="rpc://",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc = True
)

celery_app.autodiscover_tasks(['stone_site.tasks.email_tasks'])