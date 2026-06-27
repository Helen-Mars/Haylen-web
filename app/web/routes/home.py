from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.requests import Request

from app.db.session import SessionDep
from app.utils.content_loader import get_carousel_urls, get_combined_lightbox_images
from app.services.message_service import get_approved_message_tree
from app.web.template_engine import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, session: SessionDep):
    return templates.TemplateResponse(
        "pages/home.html",
        {
            "request": request,
            "images": get_combined_lightbox_images(),
            "carousel_list": get_carousel_urls(request),
            "messages": get_approved_message_tree(session),
        },
    )
