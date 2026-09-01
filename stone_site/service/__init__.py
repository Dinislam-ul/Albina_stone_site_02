from stone_site.tasks.celery_app import celery_app
from stone_site.tasks.email_tasks import send_welcome_email_task

__all__ = ['celery_app', 'send_welcome_email_task']