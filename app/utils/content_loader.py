from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent

LIGHTBOX_DIR = PROJECT_DIR / "static" / "images" / "photo_lightbox2"
LIGHTBOX_THUMB_DIR = PROJECT_DIR / "static" / "images" / "photo_lightbox2_thumb"
CAROUSEL_DIR = PROJECT_DIR / "static" / "images" / "sunset"

_IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png")


def get_combined_lightbox_images() -> list[tuple[str, str]]:
    if not LIGHTBOX_DIR.is_dir():
        return []

    image_data = []
    image_data_thumb = []
    for image_path in LIGHTBOX_DIR.iterdir():
        if image_path.suffix.lower() in _IMAGE_SUFFIXES:
            image_data.append("photo_lightbox2/" + image_path.name)
            image_data_thumb.append("photo_lightbox2_thumb/" + image_path.name)

    return list(zip(image_data, image_data_thumb))


def get_carousel_urls(request) -> list:
    if not CAROUSEL_DIR.is_dir():
        return []

    return [
        str(request.url_for("static", path="images/sunset/" + file.name))
        for file in sorted(CAROUSEL_DIR.glob("*.jpg"))
    ]

