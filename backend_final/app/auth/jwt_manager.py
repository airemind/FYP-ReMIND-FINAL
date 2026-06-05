from datetime import datetime, timedelta, timezone
from uuid import uuid4
from jose import jwt
from jose import JWTError
from fastapi import HTTPException
from app.config.settings import settings


# CREATE ACCESS TOKEN
def create_access_token(data: dict):

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    session_id = str(uuid4())
    payload = data.copy()
    payload.update({"session_id": session_id, "exp": expire})
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return token


# VERIFY ACCESS TOKEN
def verify_access_token(token: str):

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
