from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from app.database.db import Base


class Metric(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    chat_id = Column(Integer, nullable=True)
    session_id = Column(String, nullable=True)
    ai_module = Column(String, nullable=False)
    pipeline_used = Column(String, nullable=True)
    latency = Column(Float, default=0.0)
    estimated_cost = Column(Float, default=0.0)
    cache_used = Column(Boolean, default=False)
    system_load = Column(Float, default=0.0)
    ping_ms = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
