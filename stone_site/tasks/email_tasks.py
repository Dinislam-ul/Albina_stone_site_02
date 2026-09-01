from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from stone_site.core.config import settings
from stone_site.tasks.celery_app import celery_app
import asyncio

conf = ConnectionConfig(
     MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM_EMAIL,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_USE_TLS,
    MAIL_SSL_TLS=settings.MAIL_USE_SSL,
    USE_CREDENTIALS=False,
    VALIDATE_CERTS=False,
)


@celery_app.task(name="send_welcome_email_task")
def send_welcome_email_task(email: str, username:str):
    try:
        content = f"Hello, {username}. Welcome to Stone Site!"
        message = MessageSchema(
            subject = "Welcome email",
            recipients=[email],
            body=content,
            subtype="html"
        )
        fm = FastMail(conf)
        asyncio.run(fm.send_message(message))
        return f"Message for {username} was send on {email}"
    except Exception as e:  # noqa: BLE001
        raise Exception(f"There is an error during send a message on email {email}: {e}")  # noqa: TRY002
    