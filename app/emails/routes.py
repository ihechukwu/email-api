from app.api_keys.dependencies import api_key_auth
from fastapi import Depends, APIRouter

emails_router = APIRouter()


@emails_router.get("/send")
async def send_email(user=Depends(api_key_auth)):
    return {"msg": user}
