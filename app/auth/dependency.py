from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request
from .utils import decode_access_token


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:

        cred = await super().__call__(request)
        token = cred.credentials

        token_data = self.token_is_valid()

        return token_data

    def token_is_valid(self, token: str):

        return decode_access_token(token)
    


class AccessTokenBearer(TokenBearer):
    def verify_access_token(self, token_data: dict):
        

