from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.router import api_router
from app.core.config import settings
from app.db.init_db import create_db_and_tables
from app.web.router import web_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    create_db_and_tables()
    yield
    


app = FastAPI(lifespan=lifespan, debug=settings.debug)

# ── Global State ──────────────────────────────────────────────────────────
app.state.global_variables = {
    "svg_path": "/static/svgs/icons.svg",
}

# ── Static Files ──────────────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/content", StaticFiles(directory="content"), name="content")
app.mount("/shop", StaticFiles(directory="frontend/vue_project/dist", html=True), name="shop")
# ── API Routes ────────────────────────────────────────────────────────────
app.include_router(api_router)

# ── Page Routes ───────────────────────────────────────────────────────────
app.include_router(web_router)


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "version": "1.0.0"}

