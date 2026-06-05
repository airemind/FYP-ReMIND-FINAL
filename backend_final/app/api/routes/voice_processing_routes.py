from fastapi import APIRouter, UploadFile, File, Depends
import os
import shutil
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.services.orchestration.voice_orchestrator import process_and_store_voice

router = APIRouter(prefix="/voice-processing", tags=["Voice AI"])

TEMP_DIR = "temp_audio_uploads"

os.makedirs(TEMP_DIR, exist_ok=True)


@router.post("/upload")
async def upload_and_process_audio(
    user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    temp_path = os.path.join(TEMP_DIR, file.filename)
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    result = process_and_store_voice(audio_path=temp_path, db=db, user_id=user_id)
    return result
