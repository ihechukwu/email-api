from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status, Depends
from .utils import decode_access_token
from app.core.database import get_session
from app.users.service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession


user_service = UserService()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:

        cred = await super().__call__(request)
        token = cred.credentials

        token_data = self.token_is_valid(token)
        self.verify_access_token(token_data)

        return token_data

    def token_is_valid(self, token: str):

        return decode_access_token(token)


class AccessTokenBearer(TokenBearer):
    def verify_access_token(self, token_data: dict):

        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please provide access token",
            )


class RefreshTokenBearer(TokenBearer):
    def verify_access_token(self, token_data: dict):

        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="provide refresh token"
            )


async def get_current_user(
    user_credentials: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):

    user_email = user_credentials.get("email")

    user = await user_service.get_user_by_email(email=user_email, session=session)
    if user.is_verified == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please verify your account",
        )

    return user
