from sqlalchemy.orm import Session
from app.models.media import Media
from app.models.audit_log import AuditLog


def delete_media(db: Session, media_id: int, admin_id: str):
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        return False
    db.delete(media)
    db.commit()

    audit = AuditLog(
        source="admin",
        action="DELETE_MEDIA",
        target_type="media",
        target_id=media_id,
        log_info=(f"Admin {admin_id} " f"deleted media {media_id}"),
    )

    db.add(audit)
    db.commit()

    return True
