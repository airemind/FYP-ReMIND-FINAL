import os
from uuid import uuid4
from fastapi import UploadFile
from app.config.settings import settings
from sqlalchemy.orm import Session
from app.services.storage.file_validator import validate_file
from app.services.storage.cloudinary_service import upload_image, upload_audio
from app.repositories.media_repo import create_media

UPLOAD_DIR = settings.UPLOAD_DIR
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_upload(db: Session, file: UploadFile, message_id: int = None):
    content = await file.read()
    file_size = len(content)
    valid = validate_file(file.content_type, file_size)

    if not valid:
        return None

    unique_name = f"{uuid4()}_{file.filename}"
    local_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(local_path, "wb") as f:
        f.write(content)

    if "image" in file.content_type:
        cloud_result = upload_image(local_path, folder="remind/images")
        media_type = "image"

    else:
        cloud_result = upload_audio(local_path, folder="remind/audio")
        media_type = "audio"

    media_data = {
        "user_id": 1,
        "chat_id": None,
        "media_type": media_type,
        "original_url": cloud_result["url"],
    }
    media = create_media(db, media_data)

    os.remove(local_path)
    return media
