from pydantic import EmailStr
from sqlmodel.ext.asyncio.session import AsyncSession
from app.users.models import User
from app.users.schemas import UserCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy import select
from fastapi import HTTPException, status


class UserService:

    async def register(self, user_data: UserCreate, session: AsyncSession):

        new_user = User(**user_data.model_dump())

        if await self.get_user_by_email(
            new_user.email, session
        ):  # check ig user exists
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already taken "
            )
        new_user.role = "user"

        try:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists",
            )

    async def get_user_by_email(self, email: EmailStr, session: AsyncSession):

        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        return result.scalar_one_or_none()
