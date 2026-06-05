from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")


def get_current_admin(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        role = payload.get("role")
        if role != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")

        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid admin token")
