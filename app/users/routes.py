from fastapi import APIRouter, Depends, BackgroundTasks
from httpx import get
from .service import UserService
from .schemas import UserCreate, UserResponse
from app.core.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.auth.utils import get_password_hash
from app.auth.dependencies import get_current_user
from .mails import create_message, mail
from app.auth.utils import create_url_safe_token
from app.core.config import settings


users_router = APIRouter()
user_service = UserService()


@users_router.post("/register")
async def register(
    user_data: UserCreate,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):

    user_data.password = get_password_hash(user_data.password)

    user = await user_service.register(user_data=user_data, session=session)
    token = create_url_safe_token({"email": user.email})
    link = f"http://{settings.DOMAIN}/api/v1/auth/verify-email?token={token}"

    html_message = f"""
        <h2>Welcome to  our Email API services</h2>
        <p> Click <a href="{link}"> here</a> to verify your account</p>

"""
    subject = "Account verification"

    message = create_message(
        recipients=[user.email], subject=subject, body=html_message
    )

    background_task.add_task(mail.send_message, message)

    return {"msg": "registration successful, check email to verify account"}


@users_router.get("/generate-token")
async def generate_token(
    user=Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
    return user
