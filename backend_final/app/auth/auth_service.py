from sqlalchemy.orm import Relationship, Session
from fastapi import HTTPException
from app.auth.jwt_manager import verify_access_token
from app.auth.password_manager import hash_password, verify_password
from app.auth.jwt_manager import create_access_token
from app.auth.session_manager import create_session
from app.repositories.user_repo import (
    get_user_by_email,
    get_user_by_username,
    create_user,
)


# REGISTER USER
def register_user(db: Session, user_data):

    existing_user = get_user_by_email(db, user_data.email)
    existing_username = get_user_by_username(db, user_data.username)

    if existing_user:
        raise HTTPException(status_code=409, detail="Email already exists")

    if existing_username:
        raise HTTPException(status_code=409, detail="Username already exists")

    # USER DICTIONARY
    user_dict = {
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": hash_password(user_data.password),
        "role": user_data.role,
    }

    return create_user(db, user_dict)


# LOGIN USER
def login_user(db: Session, identifier: str, password: str):

    user = get_user_by_email(db, identifier)

    if not user:
        user = get_user_by_username(db, identifier)

    # USER NOT FOUND
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        return None

    # BLOCK USER
    if not user.is_active:
        raise HTTPException(
            status_code=403, detail="User account is blocked, Please contact Admin"
        )
        return None

    # PASSWORD VERIFY
    if not verify_password(password, user.hashed_password):
        return None

    # JWT TOKEN
    token = create_access_token(
        data={"sub": str(user.id), "role": user.role, "email": user.email}
    )

    # EXTRACT SESSION ID
    payload = verify_access_token(token)
    session_id = payload.get("session_id")

    # CREATE SESSION
    create_session(db, user.id, session_id)

    # FINAL RESPONSE
    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        },
    }
