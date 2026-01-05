from fastapi import APIRouter
from app.users.routes import users_router
from app.auth.routes import auth_router
from app.api_keys.routes import api_keys_router
from app.emails.routes import emails_router

api_router = APIRouter()

api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(api_keys_router, prefix="/keys", tags=["Api Keys"])
api_router.include_router(emails_router, prefix="/emails", tags=["Emails"])
