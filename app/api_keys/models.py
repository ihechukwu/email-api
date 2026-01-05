from sqlalchemy import table
from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime


class ApiKey(SQLModel, table=True):

    __tablename__ = "apikeys"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, unique=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, ondelete="CASCADE")
    key: str = Field(index=True, unique=True)
    is_active: bool = True
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )
    last_used_at: datetime | None = None
