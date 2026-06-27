from fastapi import APIRouter
# from fastapi.responses import HTMLResponse
from starlette.requests import Request
from app.web.template_engine import templates
import json
from app.core.paths import CONTENT_DIR



router = APIRouter()

# topic = "peace, elevate, enjoy"
@router.get("/self-cultivation/{topic}", name="cultivation")
async def cultivation_page(request: Request, topic: str):
    if topic == "peace":
        card_path = CONTENT_DIR / "cultivation_card"

        print(card_path.glob("*.json"))

        card_list = []
        for file in sorted(card_path.glob("*.json")):
            with file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                data["bg_image"] = request.url_for("static", path="images/cultivation/"+data["bg_image"])
                data["audio_src"] = request.url_for("assets", path="audio/peace_music/"+data["audio_src"])

                card_list.append(data)

        
        print("card_list:",card_list)

        return templates.TemplateResponse("pages/self-cultivation.html", {
            "request": request,
            "topic": topic,
            "cards": card_list
        })
    
    else:
        return templates.TemplateResponse("pages/self-cultivation.html", {
            "request": request,
            "topic": topic})





