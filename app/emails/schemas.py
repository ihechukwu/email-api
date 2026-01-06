from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional, List


class SendEmailRequest(BaseModel):

    to: List[EmailStr]
    subject: str = Field(min_length=1, max_length=250)
    html: str
    sender: str
