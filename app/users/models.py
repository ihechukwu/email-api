from pydantic import EmailStr
from sqlalchemy import table
from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, unique=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email} >"
