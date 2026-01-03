from fastapi import APIRouter
from app.users.routes import users_router
from app.auth.routes import auth_router

api_router = APIRouter()

api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
