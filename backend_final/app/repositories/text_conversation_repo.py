from sqlalchemy.orm import Session
from app.models.text_conversation import TextConversation


def create_text_conversation(db: Session, data: dict):

    conversation = TextConversation(**data)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def get_user_conversations(db: Session, user_id: int):

    return (
        db.query(TextConversation)
        .filter(TextConversation.user_id == user_id)
        .order_by(TextConversation.created_at.desc())
        .all()
    )


def get_chat_conversations(db: Session, chat_id: int):

    return (
        db.query(TextConversation)
        .filter(TextConversation.chat_id == chat_id)
        .order_by(TextConversation.created_at.asc())
        .all()
    )


def get_conversation_by_id(db: Session, conversation_id: int):

    return (
        db.query(TextConversation)
        .filter(TextConversation.id == conversation_id)
        .first()
    )


def get_all_user_conversations(db: Session, user_id: int):

    return (
        db.query(TextConversation)
        .filter(TextConversation.user_id == user_id)
        .order_by(TextConversation.created_at.desc())
        .all()
    )


def get_all_chat_conversations(db: Session, chat_id: int):

    return (
        db.query(TextConversation)
        .filter(TextConversation.chat_id == chat_id)
        .order_by(TextConversation.created_at.asc())
        .all()
    )


def get_single_conversation(db: Session, conversation_id: int):

    return (
        db.query(TextConversation)
        .filter(TextConversation.id == conversation_id)
        .first()
    )
