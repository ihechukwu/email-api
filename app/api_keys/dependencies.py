from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from app.core.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import hash_api_key
from .service import ApiKeyService
from datetime import datetime


api_key_service = ApiKeyService()
bearer_scheme = HTTPBearer(auto_error=True)


async def api_key_auth(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_session),
):

    raw_key = creds.credentials
    if not raw_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing API key"
        )

    hashed_api_key = hash_api_key(raw_key)
    api_key = await api_key_service.get_api_key_by_hash(hashed_api_key, session=session)

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or revoked key"
        )

    api_key.last_used_at = datetime.utcnow()
    session.add(api_key)
    await session.commit()

    return api_key.user_id
