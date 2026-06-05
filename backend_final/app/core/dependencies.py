from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.auth.jwt_manager import verify_access_token
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.config.settings import settings
from app.repositories.user_repo import get_user_by_id
from app.models.session import Session as UserSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = verify_access_token(token)
        user_id = payload.get("sub")
        session_id = payload.get("session_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    session = (
        db.query(UserSession)
        .filter(UserSession.session_id == session_id, UserSession.is_active == True)
        .first()
    )
    if not session:
        raise credentials_exception
    user = get_user_by_id(db, int(user_id))
    if not user:
        raise credentials_exception
    return user
