"""汇总所有 API 路由"""
from fastapi import APIRouter

from .routes.analytics import router as analytics_router
from .routes.auth import router as auth_router
from .routes.chat import router as chat_router
from .routes.messages import router as messages_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router, tags=["Auth"])
api_router.include_router(messages_router, tags=["Messages"])
api_router.include_router(chat_router, tags=["Chat"])
api_router.include_router(analytics_router, tags=["Analytics"])



