from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.db import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)
    action = Column(String, nullable=False)
    target_type = Column(String, nullable=True)
    target_id = Column(Integer, nullable=True)
    log_info = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
