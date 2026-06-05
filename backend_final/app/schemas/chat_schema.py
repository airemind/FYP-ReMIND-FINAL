from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ChatCreate(BaseModel):
    title: str = "New Chat"


class ChatUpdate(BaseModel):
    title: Optional[str] = None


class ChatResponse(BaseModel):

    id: int
    title: str
    message_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
