from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
# from fastapi.templating import Jinja2Templates
from app.web.template_engine import templates

router = APIRouter()
# templates = Jinja2Templates(directory="templates")

@router.get("/shop", response_class=HTMLResponse)
async def shop(request: Request):
    return templates.TemplateResponse("pages/shop.html", {"request": request})
