from sqlalchemy.orm import Session
from app.models.chat import Chat
from app.models.media import Media
from app.models.metric import Metric
from app.models.audit_log import AuditLog
from app.models.text_conversation import TextConversation


def delete_chat(db: Session, chat_id: int, admin_id: str):

    # DELETE MESSAGES
    db.query(TextConversation).filter(TextConversation.chat_id == chat_id).delete()

    # DELETE MEDIA
    db.query(Media).filter(Media.chat_id == chat_id).delete()

    # DELETE METRICS
    db.query(Metric).filter(Metric.chat_id == chat_id).delete()

    # DELETE CHAT
    db.query(Chat).filter(Chat.id == chat_id).delete()
    db.commit()

    audit = AuditLog(
        source="admin",
        action="DELETE_CHAT",
        target_type="chat",
        target_id=chat_id,
        log_info=(f"Admin {admin_id} " f"deleted chat {chat_id}"),
    )

    db.add(audit)
    db.commit()
    return True


def delete_message(db: Session, message_id: int, admin_id: str):
    message = (
        db.query(TextConversation).filter(TextConversation.id == message_id).first()
    )
    if not message:
        return False

    db.delete(message)
    db.commit()

    audit = AuditLog(
        source="admin",
        action="DELETE_MESSAGE",
        target_type="message",
        target_id=message_id,
        log_info=(f"Admin {admin_id} " f"deleted message {message_id}"),
    )

    db.add(audit)
    db.commit()

    return True
