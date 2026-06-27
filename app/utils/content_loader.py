from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent


CAROUSEL_DIR = PROJECT_DIR / "static" / "images" / "sunset"

_IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png")


def get_carousel_urls(request) -> list:
    if not CAROUSEL_DIR.is_dir():
        return []

    return [
        str(request.url_for("static", path="images/sunset/" + file.name))
        for file in sorted(CAROUSEL_DIR.glob("*.jpg"))
    ]

