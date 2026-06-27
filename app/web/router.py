"""汇总所有页面路由"""

from fastapi import APIRouter

from .routes.home import router as home_router
from .routes.about import router as about_router
from .routes.cooperation import router as cooperation_router
from .routes.cultivation import router as cultivation_router
from .routes.learning import router as learning_router
from .routes.shop import router as shop_router
from .routes.timeline import router as timeline_router
from .routes.travel import router as travel_router
from .routes.work import router as work_router
from .routes.register import router as register_router
from .routes.login import router as login_router

web_router = APIRouter()

web_router.include_router(home_router, tags=["Web"])
web_router.include_router(learning_router, tags=["Web"])
web_router.include_router(work_router, tags=["Web"])
web_router.include_router(cooperation_router, tags=["Web"])
web_router.include_router(about_router, tags=["Web"])
web_router.include_router(cultivation_router, tags=["Web"])
web_router.include_router(travel_router, tags=["Web"])
web_router.include_router(shop_router, tags=["Web"])
web_router.include_router(timeline_router, tags=["Web"])
web_router.include_router(register_router, tags=["Web"])
web_router.include_router(login_router, tags=["Web"])

