from pydantic import BaseModel
from typing import List, Optional


class AudioInput(BaseModel):
    transcript: Optional[str] = None
    emotions: Optional[List[str]] = []
    tone: Optional[List[str]] = []


class ImageInput(BaseModel):
    caption: Optional[str] = None
    objects: Optional[List[str]] = []
    scene: Optional[str] = None


class UserProfile(BaseModel):
    age: Optional[str] = None
    gender: Optional[str] = None
    occupation: Optional[str] = None


class PipelineInput(BaseModel):
    user_input: str
    audio: Optional[AudioInput] = None
    image: Optional[ImageInput] = None
    document: Optional[str] = None
    profile: Optional[UserProfile] = None


class PipelineOutput(BaseModel):
    memory_narrative: str
    tokens_used: Optional[int] = None
    model: Optional[str] = None
