from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.chat import Chat
from app.logs.ai_logger import ai_logger
from app.logs.error_logger import error_logger


def delete_expired_chats():

    db: Session = SessionLocal()
    try:
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=15)
        expired_chats = db.query(Chat).filter(Chat.updated_at < cutoff_date).all()
        deleted_count = 0

        for chat in expired_chats:
            db.delete(chat)
            deleted_count += 1

        db.commit()
        ai_logger.info(f"Deleted {deleted_count} expired chats")

    except Exception as e:
        error_logger.error(f"Chat cleanup failed: {str(e)}")

    finally:
        db.close()
