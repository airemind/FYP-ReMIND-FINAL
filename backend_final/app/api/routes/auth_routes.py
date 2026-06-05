from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt
from app.database.db import SessionLocal
from app.config.settings import settings
from app.schemas.user_schema import (
    UserRegister,
    UserLogin,
    UserResponse,
    GoogleAuthRequest,
)
from app.auth.auth_service import register_user, login_user
from app.auth.oauth_manager import google_authenticate
from app.auth.session_manager import invalidate_session
from app.core.dependencies import oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# REGISTER


@router.post("/register", response_model=UserResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    created_user = register_user(db, user)
    if not created_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return created_user


# LOGIN
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    token = login_user(db, form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token


# GOOGLE LOGIN
@router.post("/google")
def google_login(request: GoogleAuthRequest, db: Session = Depends(get_db)):
    auth_result = google_authenticate(
        db,
        request.token,
    )
    if not auth_result:
        raise HTTPException(status_code=401, detail="Google authentication failed")
    return auth_result


# LOGOUT


@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    session_id = payload.get("session_id")
    invalidate_session(db, session_id)
    return {"message": "Logged out successfully"}
