from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.admin_repo import get_admin_by_admin_id
from app.auth.password_manager import verify_password
from app.auth.jwt_manager import create_access_token
from app.core.constants import ALLOWED_ADMIN_IDS


def admin_login_service(db: Session, admin_id: str, password: str):

    # allowed id check
    if admin_id not in ALLOWED_ADMIN_IDS:
        raise HTTPException(status_code=403, detail="Unauthorized admin ID")

    # find admin
    admin = get_admin_by_admin_id(db, admin_id)

    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    # pass verify
    if not verify_password(password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    # jwt token
    token = create_access_token(data={"sub": admin.admin_id, "role": "admin"})

    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer",
        "admin": {"id": admin.id, "name": admin.name},
    }
