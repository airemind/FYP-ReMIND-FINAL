from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.message_schema import MessageCreate
from app.services.chat.message_service import send_message, get_messages

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/{chat_id}")
def create_message_route(
    chat_id: int,
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return send_message(
        db, chat_id, current_user.role, message.content, message.message_type
    )


@router.get("/{chat_id}")
def get_chat_messages_route(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_messages(db, chat_id)
