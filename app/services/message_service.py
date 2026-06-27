from sqlmodel import Session, select

from app.models.message import Message


def get_approved_message_tree(session: Session) -> list[dict]:
    messages = session.exec(
        select(Message).where(Message.is_approved).order_by(Message.create_at.desc())
    ).all()

    message_dict = {msg.id: msg.model_dump() for msg in messages}
    for msg in message_dict.values():
        msg["children"] = []

    roots = []
    for msg in message_dict.values():
        parent_id = msg["parent_id"]
        if parent_id is None or parent_id == 0:
            roots.append(msg)
        elif parent_id in message_dict:
            parent_msg = message_dict[parent_id]
            msg["parent_name"] = parent_msg["name"]
            parent_msg["children"].append(msg)

    return roots
