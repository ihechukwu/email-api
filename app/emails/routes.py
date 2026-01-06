from app.api_keys.dependencies import api_key_auth
from fastapi import Depends, APIRouter, BackgroundTasks
from .schemas import SendEmailRequest
from .utils import get_mailer, create_message


emails_router = APIRouter()


@emails_router.post("/send")
async def send_email(
    payload: SendEmailRequest,
    background_task: BackgroundTasks,
    user=Depends(api_key_auth),
):
    mailer = get_mailer(payload.sender)

    email_list = payload.to
    subject = payload.subject
    body = payload.html
    message = create_message(recipients=email_list, subject=subject, body=body)
    background_task.add_task(mailer.send_message, message)

    return {"msg": "message sent successfully"}
