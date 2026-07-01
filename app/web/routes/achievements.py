import json

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.web.template_engine import templates
from app.utils.content_loader import PROJECT_DIR

router = APIRouter()
@router.get("/achievements", response_class=HTMLResponse)
async def get_achievement(request: Request):
    publication_path = PROJECT_DIR / "content" / "publication" / "publication.json"

    # 读取 JSON 文件
    with open(publication_path, 'r', encoding='utf-8') as f:
        publications = json.load(f)

    for publication in publications:
        publication["pdflink"] = publication['pdflink']

    # 将修改后的 publications 传递到模板
    return templates.TemplateResponse("pages/achievements.html", {"request": request, "publications": publications})

