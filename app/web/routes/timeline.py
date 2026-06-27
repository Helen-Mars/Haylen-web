from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
# from fastapi.templating import Jinja2Templates
from app.web.template_engine import templates
import json
from pathlib import Path

router = APIRouter()
# templates = Jinja2Templates(directory="templates")

@router.get("/timeline", response_class=HTMLResponse)
async def shop(request: Request):
    json_path = Path("content/timeline_file/my_timeline.json")
    with open(json_path, "r", encoding="utf-8") as f:
        timeline_json = json.load(f)

    return templates.TemplateResponse("pages/timeline.html", {"request": request,
                                                              "timeline_json": timeline_json})