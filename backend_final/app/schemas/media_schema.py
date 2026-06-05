from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MediaResponse(BaseModel):
    id: int
    media_type: str
    original_url: Optional[str]
    processed_url: Optional[str]
    transcript: Optional[str]
    caption: Optional[str]
    uploaded_at: datetime

    class Config:
        from_attributes = True
