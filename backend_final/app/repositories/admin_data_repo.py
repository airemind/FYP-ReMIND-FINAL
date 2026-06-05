from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def get_data_controls(db: Session, page: int = 1, limit: int = 10):

    logs = db.query(AuditLog).offset((page - 1) * limit).limit(limit).all()

    response = []

    for log in logs:

        response.append(
            {
                "log_id": log.id,
                "source": log.source,
                "action": log.action,
                "target_type": (log.target_type),
                "target_id": (log.target_id),
                "log_info": (log.log_info),
                "created_at": (log.created_at),
            }
        )

    return response
