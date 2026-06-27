from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from app.web.template_engine import templates

router = APIRouter()

@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("pages/about.html", {"request": request})