from datetime import date, datetime
from pathlib import Path
from typing import Any

from fastapi.templating import Jinja2Templates


def datetimeformat(
    value: Any,
    fmt: str = "%Y-%m-%d %H:%M:%S",
) -> str:
    """Jinja2 中用于格式化日期时间的过滤器。"""

    if value is None:
        return ""

    if isinstance(value, (datetime, date)):
        return value.strftime(fmt)

    return str(value)


# 当前文件位置：app/web/template_engine.py
# parents[2] 指向项目根目录：app/ → web/ → 根目录
PROJECT_DIR = Path(__file__).resolve().parents[2]

templates = Jinja2Templates(
    directory=str(PROJECT_DIR / "templates")
)

# 注册模板过滤器
templates.env.filters["datetimeformat"] = datetimeformat