from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from pydantic import EmailStr
from app.core.config import settings


def get_mailer(sender_name: str):

    config = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,  # fixed email
        MAIL_FROM_NAME=sender_name,  # dynamic name
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
    )

    return FastMail(config)


def create_message(recipients: list[EmailStr], subject: str, body: str):
    return MessageSchema(
        recipients=recipients, subject=subject, body=body, subtype=MessageType.html
    )
