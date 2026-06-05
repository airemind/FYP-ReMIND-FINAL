from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.db import Base
from app.models.chat import Chat


class TextConversation(Base):
    __tablename__ = "text_conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=True)
    user_input = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    detected_intent = Column(String, nullable=True)
    extracted_entities = Column(JSON, nullable=True)
    retrieved_context = Column(JSON, nullable=True)
    response_length = Column(Integer, nullable=True)
    latency_seconds = Column(Float, nullable=True)
    readability_score = Column(Float, nullable=True)
    model_used = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    chat = relationship("Chat", back_populates="text_conversations")
