from pathlib import Path

# 当前文件：fastApiProject1/app/core/paths.py
PROJECT_DIR = Path(__file__).resolve().parents[2]

APP_DIR = PROJECT_DIR / "app"
CONTENT_DIR = PROJECT_DIR / "content"
ASSETS_DIR = PROJECT_DIR / "assets"
DATA_DIR = PROJECT_DIR / "data"

STATIC_DIR = PROJECT_DIR / "static"
TEMPLATES_DIR = PROJECT_DIR / "templates"