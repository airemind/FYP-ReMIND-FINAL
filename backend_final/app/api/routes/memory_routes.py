import os
import uuid
import shutil

from fastapi import APIRouter, UploadFile, File, Form, Depends

from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.services.orchestration.memory_orchestration import process_multimodal_memory

router = APIRouter(prefix="/memory", tags=["Multimodal Memory AI"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../../temp_uploads"))

os.makedirs(TEMP_DIR, exist_ok=True)


@router.post("/process")
async def process_memory(
    user_id: int = Form(...),
    user_prompt: str = Form(None),
    chat_id: int = Form(None),
    image: UploadFile = File(None),
    audio: UploadFile = File(None),
    db: Session = Depends(get_db),
):

    image_path = None
    audio_path = None

    # save image

    if image:
        image_extension = os.path.splitext(image.filename)[1]
        image_filename = f"{uuid.uuid4()}" f"{image_extension}"
        image_path = os.path.join(TEMP_DIR, image_filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    # save audio

    if audio:
        audio_extension = os.path.splitext(audio.filename)[1]
        audio_filename = f"{uuid.uuid4()}" f"{audio_extension}"
        audio_path = os.path.join(TEMP_DIR, audio_filename)
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
    result = process_multimodal_memory(
        db=db,
        user_id=user_id,
        chat_id=chat_id,
        image_path=image_path,
        audio_path=audio_path,
        user_prompt=user_prompt,
    )

    return result
