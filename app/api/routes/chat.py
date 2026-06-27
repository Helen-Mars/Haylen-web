from fastapi import APIRouter
from openai import OpenAI

from app.core.config import settings
from app.schemas.chat import ChatRequest


client = OpenAI(api_key=settings.openai_api_key)

router = APIRouter(prefix="/chatting")


@router.post("/chat")
async def chat_api(req: ChatRequest):
    try:
        response = client.responses.create(
            model=req.model,
            instructions="You are a coding assistant that talks like a pirate.",
            input=req.message,
        )
        return {"reply": response.output_text}
    except Exception as e:
        return {"error": str(e)}

