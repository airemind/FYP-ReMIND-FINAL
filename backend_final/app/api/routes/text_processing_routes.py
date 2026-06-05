from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.services.orchestration.text_orchestrator import process_and_store_text
from app.repositories.text_conversation_repo import (
    get_all_user_conversations,
    get_all_chat_conversations,
    get_single_conversation,
)

router = APIRouter(prefix="/text-processing", tags=["Text AI"])


class TextRequest(BaseModel):
    user_id: int
    user_input: str
    chat_id: int | None = None
    audio: dict | None = None
    image: dict | None = None
    document: str | None = None
    profile: dict | None = None


@router.post("/chat")
async def process_text_request(request: TextRequest, db: Session = Depends(get_db)):
    result = process_and_store_text(
        db=db,
        user_id=request.user_id,
        user_input=request.user_input,
        chat_id=request.chat_id,
        audio=request.audio,
        image=request.image,
        document=request.document,
        profile=request.profile,
    )

    return result


@router.get("/history/user/{user_id}")
async def get_user_history(user_id: int, db: Session = Depends(get_db)):
    conversations = get_all_user_conversations(db, user_id)
    return conversations


@router.get("/history/chat/{chat_id}")
async def get_chat_history(chat_id: int, db: Session = Depends(get_db)):
    conversations = get_all_chat_conversations(db, chat_id)
    return conversations


@router.get("/history/{conversation_id}")
async def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = get_single_conversation(db, conversation_id)
    return conversation
