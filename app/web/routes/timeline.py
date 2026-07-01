from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
# from fastapi.templating import Jinja2Templates
from app.web.template_engine import templates
import json

from app.core.config import settings
from app.core.paths import PROJECT_DIR






router = APIRouter()
# templates = Jinja2Templates(directory="templates")

@router.get("/timeline", response_class=HTMLResponse)
async def shop(request: Request):
    timeline_json = PROJECT_DIR / "content/timeline_file/my_timeline.json"
    storymap_json = PROJECT_DIR / "content/storymap/mystorymap.json"
    with open(timeline_json, "r", encoding="utf-8") as f:
        timeline_json = json.load(f)

    with open(storymap_json, "r", encoding="utf-8") as f:
        storymap_json = json.load(f)

    replace_urls(timeline_json)
    replace_urls(storymap_json)

  
    return templates.TemplateResponse("pages/timeline.html", {"request": request,
                                                              "timeline_json": timeline_json,
                                                              "storymap_json": storymap_json})


# 递归替换 url 中的图片路径为 Cloudflare 域名
_IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".mp3")
def replace_urls(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "url" and isinstance(value, str) and value.startswith("/"):
                if value.lower().endswith(_IMAGE_EXTS):
                    obj[key] = f"{settings.cloudflare_images_domain}{value}"
            else:
                replace_urls(value)
    elif isinstance(obj, list):
        for item in obj:
            replace_urls(item)

