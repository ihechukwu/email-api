from datetime import timedelta
from .utils import create_access_token, verify_password_hash
from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import LoginResponse, UserLogin
from app.core.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.users.service import UserService
from app.core.config import settings


auth_router = APIRouter()

user_service = UserService()


@auth_router.post("/login", response_model=LoginResponse)
async def login(user_data: UserLogin, session: AsyncSession = Depends(get_session)):

    user = await user_service.get_user_by_email(user_data.email, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )

    is_password_valid = verify_password_hash(user_data.password, user.password)

    if not is_password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token({"user_id": str(user.id), "email": user.email})
    refresh_token = create_access_token(
        {"user_id": str(user.id), "email": user.email},
        expire=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        refresh=True,
    )

    return {
        "user": user,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
