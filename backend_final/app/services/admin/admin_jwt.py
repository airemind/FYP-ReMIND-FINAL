from datetime import datetime, timedelta, timezone

from jose import jwt
from app.config.settings import settings

SECRET_KEY = settings.ADMIN_SECRET_KEY
ALGORITHM = settings.ALGORITHM
EXPIRE_HOURS = 24


def create_admin_token(admin_id: str, role: str):
    payload = {
        "sub": admin_id,
        "role": role,
        "exp": (datetime.now(timezone.utc) + timedelta(hours=EXPIRE_HOURS)),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
