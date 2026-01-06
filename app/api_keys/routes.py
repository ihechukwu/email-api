import uuid
from fastapi import APIRouter, Depends, status, HTTPException
from .service import ApiKeyService
from app.core.database import get_session
from app.auth.dependencies import get_current_user
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import generate_api_key, hash_api_key


api_keys_router = APIRouter()
api_key_service = ApiKeyService()


@api_keys_router.get("/generate-api-key")
async def create_api_key(
    user=Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
    user_id = user.id
    key = generate_api_key()
    hashed_key = hash_api_key(key)

    api_key = await api_key_service.create_api_key(
        user_id=user_id, key=hashed_key, session=session
    )
    return {"api_key": key, "warning": "save this key now!"}


@api_keys_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(
    user_id: uuid.UUID,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    await api_key_service.delete_api_key(user_id=user_id, session=session)
    return
