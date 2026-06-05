from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from app.cache.redis_cache import redis_client


def delete_log(db: Session, log_id: int):
    log = db.query(AuditLog).filter(AuditLog.id == log_id).first()

    if not log:
        return False

    db.delete(log)
    db.commit()
    return True


def clear_all_cache():
    redis_client.flushall()
    return True
