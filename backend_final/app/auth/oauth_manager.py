from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy.orm import Session
from app.config.settings import settings
from app.repositories.user_repo import get_user_by_email
from app.models.user import User
from app.auth.jwt_manager import create_access_token, verify_access_token
from app.auth.session_manager import create_session


def google_authenticate(
    db: Session,
    google_token: str,
):
    try:
        user_info = id_token.verify_oauth2_token(
            google_token, requests.Request(), settings.GOOGLE_CLIENT_ID
        )
    except Exception as e:
        print("Google verification failed:", e)
        return None

    email = user_info.get("email")
    google_id = user_info.get("sub")
    username = user_info.get("name", email.split("@")[0])
    existing_user = get_user_by_email(db, email)

    # EXISTING USER

    if existing_user:
        token = create_access_token({"sub": str(existing_user.id)})
        payload = verify_access_token(token)
        session_id = payload.get("session_id")
        create_session(db, existing_user.id, session_id)

        return {
            "access_token": token,
            "token_type": "bearer",
            "session_id": session_id,
            "is_new_user": False,
            "user": {
                "id": existing_user.id,
                "username": existing_user.username,
                "email": existing_user.email,
            },
        }

    # NEW USER

    new_user = User(
        username=username,
        email=email,
        hashed_password=None,
        oauth_provider="google",
        google_id=google_id,
        role="user",
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id)})
    payload = verify_access_token(token)
    session_id = payload.get("session_id")
    create_session(db, new_user.id, session_id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "session_id": session_id,
        "is_new_user": True,
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
        },
    }
