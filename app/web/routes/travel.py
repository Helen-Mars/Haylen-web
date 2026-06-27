from fastapi import Request
from fastapi.routing import APIRouter
from app.web.template_engine import templates

router = APIRouter()
# topic = []
@router.get("/travel/{topic}", name="travel")
async def travel(request: Request, topic: str):
    return templates.TemplateResponse("pages/travel.html", {
        "request": request,
        "topic": topic
    })

