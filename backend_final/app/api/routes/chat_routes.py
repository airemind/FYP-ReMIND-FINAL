from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.chat import Chat
from app.schemas.chat_schema import ChatCreate, ChatUpdate
from app.services.chat.chat_service import (
    create_new_chat,
    get_chats,
    remove_chat,
    rename_chat,
)

router = APIRouter(prefix="/chats", tags=["Chats"])


@router.post("/")
def create_chat(
    data: ChatCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_new_chat(db, current_user.id, data.title)


@router.get("/")
def user_chats(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return get_chats(db, current_user.id)


@router.delete("/{chat_id}")
def delete_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = remove_chat(db, current_user.id, chat_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"message": "Chat deleted"}


@router.patch("/{chat_id}")
def update_chat(
    chat_id: int,
    payload: ChatUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    chat = (
        db.query(Chat)
        .filter(Chat.id == chat_id, Chat.user_id == current_user.id)
        .first()
    )
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    updated = rename_chat(db, current_user.id, chat_id, payload.title)
    if not updated:
        raise HTTPException(status_code=404, detail="Chat not found")
    db.commit()
    db.refresh(chat)
    return {"success": True, "chat": updated}
