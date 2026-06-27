from fastapi import APIRouter
from sqlmodel import select

from app.db.session import SessionDep
from app.models.page_view import PageView

router = APIRouter(prefix="/analyzing")


@router.get("/track_page")
async def track_page(db: SessionDep):
    page_view = db.exec(select(PageView)).first()
    if not page_view:
        page_view = PageView(count=1)
        db.add(page_view)
    else:
        page_view.count += 1

    db.commit()
    db.refresh(page_view)
    return {"message": "Page view recorded"}


@router.get("/page_view_count")
async def page_view_count(db: SessionDep):
    page_view = db.exec(select(PageView)).first()
    total_views = page_view.count if page_view else 0
    return {"total_views": total_views}
