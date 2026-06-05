from sqlalchemy.orm import Session
from app.repositories.message_repo import create_message, get_chat_messages
from app.repositories.chat_repo import get_chat_by_id


def send_message(
    db: Session, chat_id: int, sender: str, content: str, message_type: str = "text"
):
    chat = get_chat_by_id(db, chat_id)
    if not chat:
        return None
    message_data = {
        "chat_id": chat_id,
        "sender": sender,
        "content": content,
        "message_type": message_type,
    }

    return create_message(db, message_data)


def get_messages(db: Session, chat_id: int):
    return get_chat_messages(db, chat_id)
