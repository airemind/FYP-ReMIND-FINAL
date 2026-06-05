from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MessageCreate(BaseModel):
    content: Optional[str] = None
    message_type: str


from typing import Optional


class MessageResponse(BaseModel):
    id: int
    sender: str
    content: Optional[str]
    message_type: str
    created_at: datetime
    caption: Optional[str] = None
    enhanced_image: Optional[str] = None
    generated_audio: Optional[str] = None
    transcript: Optional[str] = None
    emotion: Optional[str] = None
    tones: Optional[list] = []
    retrieved_context: Optional[list] = []

    class Config:
        from_attributes = True
