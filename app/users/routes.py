from fastapi import APIRouter, Depends
from httpx import get
from .service import UserService
from .schemas import UserCreate, UserResponse
from app.core.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.auth.utils import get_password_hash


users_router = APIRouter()
user_service = UserService()


@users_router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_session)):

    user_data.password = get_password_hash(user_data.password)

    user = await user_service.register(user_data=user_data, session=session)

    return user
