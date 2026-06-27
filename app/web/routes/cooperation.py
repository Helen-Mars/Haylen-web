from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from app.web.template_engine import templates

router = APIRouter()


@router.get("/cooperation", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("pages/cooperation.html", {"request": request})
