from fastapi import APIRouter
from app.api.endpoints import crypto
from app.api.v1.endpoints import auth

api_router = APIRouter()

# Включаем роутер аутентификации
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Включаем роутер криптографических операций
api_router.include_router(crypto.router, prefix="/crypto", tags=["crypto"]) 