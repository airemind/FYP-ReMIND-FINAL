from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.db import Base


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    sender = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    message_type = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    caption = Column(Text, nullable=True)
    enhanced_image = Column(Text, nullable=True)
    generated_audio = Column(Text, nullable=True)
    transcript = Column(Text, nullable=True)
    emotion = Column(String, nullable=True)
    tones = Column(JSON, nullable=True)
    retrieved_context = Column(JSON, nullable=True)
    chat = relationship("Chat", back_populates="messages")
