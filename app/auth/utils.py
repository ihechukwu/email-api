from pwdlib import PasswordHash
import jwt
from fastapi import HTTPException, Header, status
from app.core.config import settings
from datetime import datetime, timedelta
import uuid


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTE = settings.ACCESS_TOKEN_EXPIRE_MINUTE

password_hash = PasswordHash.recommended()

credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password_hash(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict, expire: timedelta = None, refresh: bool = False):

    to_encode = data.copy()
    if expire:
        expire = datetime.utcnow() + expire

    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)

    to_encode.update({"exp": expire, "jti": str(uuid.uuid4), "refresh": refresh})

    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
        return encoded_jwt

    except jwt.PyJWTError:
        raise credential_exception


def decode_access_token(token: str):

    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        return payload

    except jwt.PyJWTError:
        raise credential_exception
