from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    is_verified: bool
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
