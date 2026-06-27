from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.requests import Request

from app.web.template_engine import templates

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("pages/login.html", {"request": request})
