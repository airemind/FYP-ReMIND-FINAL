from fastapi import APIRouter, Depends, HTTPException, Query

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database.db import get_db

from app.schemas.admin_schema import AdminLoginRequest, AdminUpdateUserRequest

from app.services.admin.admin_auth_service import admin_login_service

from app.admin.admin_dependency import get_current_admin

from app.services.admin.system_metrics_service import get_system_metrics

from app.services.admin.user_analytics_service import get_user_analytics

from app.services.admin.ai_metrics_service import get_ai_metrics

from app.admin.admin_audit_logger import log_admin_action

# =========================
# REPOSITORIES
# =========================
from app.repositories.admin_user_repo import get_users

from app.repositories.admin_memory_repo import get_memory_controls

from app.repositories.admin_data_repo import get_data_controls

from app.repositories.admin_media_repo import get_media_controls

# =========================
# SERVICES
# =========================
from app.services.admin.user_control_service import (
    disable_user,
    enable_user,
    update_user,
)

from app.services.admin.memory_control_service import delete_chat, delete_message

from app.services.admin.data_control_service import delete_log, clear_all_cache

from app.services.admin.media_control_service import delete_media

router = APIRouter(prefix="/admin", tags=["Admin"])


# admin login
@router.post("/login")
def admin_login(payload: AdminLoginRequest, db: Session = Depends(get_db)):

    return admin_login_service(
        db=db, admin_id=payload.admin_id, password=payload.password
    )


# admin analytics
@router.get("/analytics")
def get_admin_analytics(
    db: Session = Depends(get_db), admin=Depends(get_current_admin)
):

    log_admin_action(admin["sub"], "VIEW_ANALYTICS")

    return {
        "success": True,
        "user_analytics": (get_user_analytics(db)),
        "system_metrics": (get_system_metrics()),
        "ai_metrics": (get_ai_metrics(db)),
    }


# get users
@router.get("/users")
def admin_get_users(
    page: int = Query(1),
    limit: int = Query(100),
    search: str = None,
    role: str = None,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):

    users, total = get_users(db=db, page=page, limit=limit, search=search, role=role)
    response = []
    for user in users:
        response.append(
            {
                "user_id": user.id,
                "username": (user.username),
                "email": (user.email),
                "status": ("active" if user.is_active else "inactive"),
                "state": ("logged_in" if user.is_logged_in else "logged_out"),
                "uptime": (
                    lambda delta: f"{delta.days}d :"
                    f"{delta.seconds//3600}h :"
                    f"{(delta.seconds%3600)//60}m"
                )(datetime.now(timezone.utc) - user.created_at),
            }
        )

    return {
        "success": True,
        "total": total,
        "page": page,
        "limit": limit,
        "users": response,
    }


# disbale user
@router.patch("/users/{user_id}/disable")
def admin_disable_user(
    user_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)
):
    user = disable_user(db, user_id, admin["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "message": "User disabled"}


# enable user
@router.patch("/users/{user_id}/enable")
def admin_enable_user(
    user_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)
):
    user = enable_user(db, user_id, admin["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "message": "User enabled"}


# update user
@router.put("/users/{user_id}")
def admin_update_user(
    user_id: int,
    data: AdminUpdateUserRequest,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):

    user = update_user(db, user_id, data.username, data.email, admin["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "success": True,
        "message": "User updated",
        "updated_user": {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
        },
    }


# get memories
@router.get("/memories")
def admin_get_memories(
    page: int = Query(1),
    limit: int = Query(100),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    data = get_memory_controls(db, page, limit)
    return {"success": True, "memories": data}


# delete chat
@router.delete("/chats/{chat_id}")
def admin_delete_chat(
    chat_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)
):
    delete_chat(db, chat_id, admin["sub"])
    return {"success": True, "message": "Chat deleted"}


# delete message
@router.delete("/messages/{message_id}")
def admin_delete_message(
    message_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)
):
    delete_message(db, message_id, admin["sub"])
    return {"success": True, "message": "Message deleted"}


# get data controls
@router.get("/data")
def admin_get_data(
    page: int = Query(1),
    limit: int = Query(100),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    data = get_data_controls(db, page, limit)
    return {"success": True, "data_controls": data}


# del log
@router.delete("/logs/{log_id}")
def admin_delete_log(
    log_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)
):
    delete_log(db, log_id)
    return {"success": True, "message": "Log deleted"}


# CLEAR CACHE
@router.delete("/cache/clear")
def admin_clear_cache(admin=Depends(get_current_admin)):
    clear_all_cache()
    return {"success": True, "message": "Cache cleared"}


# GET MEDIA
@router.get("/media")
def admin_get_media(
    page: int = Query(1),
    limit: int = Query(100),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    media = get_media_controls(db, page, limit)
    return {"success": True, "media": media}


# DELETE MEDIA
@router.delete("/media/{media_id}")
def admin_delete_media(
    media_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)
):
    delete_media(db, media_id, admin["sub"])
    return {"success": True, "message": "Media deleted"}


# ADMIN LOGOUT
@router.post("/logout")
def admin_logout():
    return {"success": True, "message": "Admin logged out successfully"}
