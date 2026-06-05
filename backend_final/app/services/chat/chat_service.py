from sqlalchemy.orm import Session
from app.repositories.chat_repo import (
    create_chat,
    get_chat_by_id,
    get_user_chats,
    delete_chat,
    update_chat_title,
)


def create_new_chat(db: Session, user_id: int, title: str = "New Chat"):
    return create_chat(db, user_id, title)


def get_chats(db: Session, user_id: int):
    return get_user_chats(db, user_id)


def remove_chat(db: Session, user_id: int, chat_id: int):
    chat = get_chat_by_id(db, chat_id)
    if not chat:
        return False
    if chat.user_id != user_id:
        return False
    delete_chat(db, chat_id)
    return True


def rename_chat(db: Session, user_id: int, chat_id: int, new_title: str):
    chat = get_chat_by_id(db, chat_id)
    if not chat:
        return False
    if chat.user_id != user_id:
        return False
    update_chat_title(db, chat_id, new_title)
    return True
