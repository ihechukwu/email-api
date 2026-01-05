from app.api_keys.dependencies import api_key_auth
from fastapi import Depends, APIRouter, BackgroundTasks
from .schemas import SendEmailRequest
from app.users.mails import create_message, mail


emails_router = APIRouter()


@emails_router.post("/send")
async def send_email(
    payload: SendEmailRequest,
    background_task: BackgroundTasks,
    user=Depends(api_key_auth),
):

    email_list = payload.to
    subject = payload.subject
    body = payload.html
    message = create_message(recipients=email_list, subject=subject, body=body)
    background_task.add_task(mail.send_message, message)

    return {"msg": "message sent successfully"}
