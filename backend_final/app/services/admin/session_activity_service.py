from datetime import datetime
from sqlalchemy.orm import Session
from app.models.session import Session as UserSession


def update_session_activity(db: Session, session_id: str):
    session = db.query(UserSession).filter(UserSession.session_id == session_id).first()
    if not session:
        return
    session.last_activity = datetime.utcnow()
    db.commit()
