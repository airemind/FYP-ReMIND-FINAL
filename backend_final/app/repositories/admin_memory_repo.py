from sqlalchemy.orm import Session

from app.models.chat import Chat
from app.models.media import Media
from app.models.metric import Metric
from app.models.text_conversation import TextConversation


def get_memory_controls(db: Session, page: int = 1, limit: int = 10):
    chats = db.query(Chat).offset((page - 1) * limit).limit(limit).all()
    response = []
    for chat in chats:
        messages = (
            db.query(TextConversation).filter(TextConversation.chat_id == chat.id).all()
        )
        media = db.query(Media).filter(Media.chat_id == chat.id).all()
        metrics = db.query(Metric).filter(Metric.chat_id == chat.id).all()

        # safe value extraction with defaults

        first_message_id = messages[0].id if messages else None
        first_media_id = media[0].id if media else None
        pipeline_used = ", ".join(
            list(
                set(
                    [metric.pipeline_used for metric in metrics if metric.pipeline_used]
                )
            )
        )
        average_latency = (
            round(sum(metric.latency for metric in metrics) / len(metrics), 2)
            if metrics
            else 0
        )
        total_cost = (
            round(sum(metric.estimated_cost for metric in metrics), 4) if metrics else 0
        )
        average_ping = (
            round(sum(metric.ping_ms for metric in metrics) / len(metrics), 2)
            if metrics
            else 0
        )

        # response

        response.append(
            {
                "message_id": first_message_id,
                "chat_id": chat.id,
                "message_count": len(messages),
                "media_attached": len(media) > 0,
                "media_id": first_media_id,
                "pipeline_used": pipeline_used,
                "latency": average_latency,
                "cost": total_cost,
                "ping": average_ping,
            }
        )

    return response
