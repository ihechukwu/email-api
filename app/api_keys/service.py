from sqlmodel.ext.asyncio.session import AsyncSession
from .models import ApiKey
from sqlalchemy import select
import uuid
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status


class ApiKeyService:

    async def create_api_key(self, user_id: uuid.UUID, key: str, session: AsyncSession):

        api_key_hash = await self.get_api_key(user_id=user_id, session=session)
        if api_key_hash:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already generated api key",
            )
        new_key = ApiKey(key=key, user_id=user_id)

        try:
            session.add(new_key)
            await session.commit()
            await session.refresh(new_key)

            return new_key

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong",
            )

    async def get_api_key(self, user_id: uuid.UUID, session: AsyncSession):
        """
        Docstring for get_api_key
        returns hashed api key by user_id

        :param self: Description
        :param user_id: Description
        :type user_id: uuid.UUID
        :param session: Description
        :type session: AsyncSession
        """
        statement = select(ApiKey).where(ApiKey.user_id == user_id)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async def get_api_key_by_hash(self, api_hash: str, session: AsyncSession):
        """
        Docstring for get_api_key_by_hash

        returns hash api key by api key

        :param self: Description
        :param api_hash: Description
        :type api_hash: str
        :param session: Description
        :type session: AsyncSession
        """
        statement = select(ApiKey).where(
            ApiKey.key == api_hash, ApiKey.is_active == True
        )
        result = await session.execute(statement)
        return result.scalar_one_or_none()
