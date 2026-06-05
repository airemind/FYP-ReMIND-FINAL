from sqlalchemy.orm import Session
from app.models.user import User
from app.models.audit_log import AuditLog


def disable_user(db: Session, user_id: int, admin_id: str):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    user.is_active = False
    user.is_logged_in = False

    db.commit()

    # AUDIT LOG
    audit = AuditLog(
        source="admin",
        action="DISABLE_USER",
        target_type="user",
        target_id=user.id,
        log_info=(f"Admin {admin_id} " f"disabled user {user.id}"),
    )

    db.add(audit)
    db.commit()

    return user


def enable_user(db: Session, user_id: int, admin_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    user.is_active = True
    user.is_logged_in = True
    db.commit()
    audit = AuditLog(
        source="admin",
        action="ENABLE_USER",
        target_type="user",
        target_id=user.id,
        log_info=(f"Admin {admin_id} " f"enabled user {user.id}"),
    )

    db.add(audit)
    db.commit()

    return user


def update_user(db: Session, user_id: int, username: str, email: str, admin_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    user.username = username
    user.email = email
    db.commit()
    audit = AuditLog(
        source="admin",
        action="UPDATE_USER",
        target_type="user",
        target_id=user.id,
        log_info=(f"Admin {admin_id} " f"updated user {user.id}"),
    )

    db.add(audit)
    db.commit()
    return user
