from sqlalchemy.orm import Session
from app.models.media import Media


def get_media_controls(db: Session, page: int = 1, limit: int = 10):
    media_items = db.query(Media).offset((page - 1) * limit).limit(limit).all()
    response = []
    for media in media_items:
        extension = None
        if media.original_url:
            extension = media.original_url.split(".")[-1]
        response.append(
            {
                "media_id": media.id,
                "chat_id": media.chat_id,
                "media_type": (media.media_type),
                "media_format": extension,
                "processed": (media.enhanced_url is not None),
            }
        )
    return response
