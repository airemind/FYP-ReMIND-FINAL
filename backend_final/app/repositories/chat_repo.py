from sqlalchemy.orm import Session
from app.models.chat import Chat


def create_chat(db: Session, user_id: int, title: str):
    chat = Chat(user_id=user_id, title=title)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def get_user_chats(db: Session, user_id: int):
    return (
        db.query(Chat)
        .filter(Chat.user_id == user_id)
        .order_by(Chat.last_activity.desc(), Chat.message_count.desc())
        .all()
    )


def get_chat_by_id(db: Session, chat_id: int):
    return db.query(Chat).filter(Chat.id == chat_id).first()


def delete_chat(db: Session, chat_id: int):
    chat = get_chat_by_id(db, chat_id)
    if chat:
        db.delete(chat)
        db.commit()
    return chat


def update_chat_title(db: Session, chat_id: int, title: str):
    chat = get_chat_by_id(db, chat_id)
    if not chat:
        return None
    chat.title = title
    db.commit()
    db.refresh(chat)
    return chat
