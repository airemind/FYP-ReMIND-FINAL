from sqlalchemy.orm import Session
from app.models.media import Media


def create_media(db: Session, media_data: dict):

    media = Media(**media_data)
    db.add(media)
    db.commit()
    db.refresh(media)
    return media
