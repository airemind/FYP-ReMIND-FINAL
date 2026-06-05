from sqlalchemy.orm import Session
from app.models.message import Message


def create_message(db: Session, message_data: dict):
    message = Message(**message_data)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_chat_messages(db: Session, chat_id: int):

    return (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at.asc())
        .all()
    )
