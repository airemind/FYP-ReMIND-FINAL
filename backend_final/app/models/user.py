from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    role = Column(String, nullable=False)
    # OAUTH
    oauth_provider = Column(String, nullable=True)
    google_id = Column(String, nullable=True)

    # User controls

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_logged_in = Column(Boolean, default=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(timezone.utc),
    )

    # RELATIONSHIPS

    chats = relationship("Chat", back_populates="user", cascade="all, delete")
    sessions = relationship("Session", back_populates="user", cascade="all, delete")
    patient_profiles = relationship(
        "PatientProfile", back_populates="user", cascade="all, delete"
    )
    media = relationship("Media", back_populates="user", cascade="all, delete")
