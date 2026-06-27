from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.requests import Request

from app.web.template_engine import templates

router = APIRouter()


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("pages/register.html", {"request": request})
