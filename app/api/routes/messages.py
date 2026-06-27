from fastapi import APIRouter, HTTPException
from app.db.session import SessionDep
from app.models.message import Message
from app.schemas.message import MessageCreate


router = APIRouter(prefix="/messaging")



@router.post("/messages")
async def post_message(msg: MessageCreate, session: SessionDep):
    new_message = Message(
        name=msg.name,
        title=msg.title,
        content=msg.content,
        parent_id=msg.parent_id,
        is_approved=True,
    )
    session.add(new_message)
    session.commit()
    session.refresh(new_message)
    return {"status": "waiting_approval"}


@router.post("/admin/approve/{message_id}")
async def approve_message(message_id: int, session: SessionDep):
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="留言不存在")
    message.is_approved = True
    session.add(message)
    session.commit()
    return {"status": "approved"}

