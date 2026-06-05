from sqlalchemy.orm import Session
from app.models.session import Session as UserSession


def create_session(db: Session, user_id: int, session_id: str):
    session = UserSession(user_id=user_id, session_id=session_id)
    db.add(session)
    db.commit()
    return session


def invalidate_session(db: Session, session_id: str):
    session = db.query(UserSession).filter(UserSession.session_id == session_id).first()
    if session:
        session.is_active = False
        db.commit()
