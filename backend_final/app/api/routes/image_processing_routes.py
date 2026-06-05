from fastapi import APIRouter, UploadFile, File, Depends
import os
import shutil
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.services.orchestration.image_orchestrator import process_and_store_image

router = APIRouter(prefix="/image-processing", tags=["Production Image AI"])

TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)


@router.post("/upload")
async def upload_and_process_image(
    user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    temp_path = os.path.join(TEMP_DIR, file.filename)
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    result = process_and_store_image(image_path=temp_path, db=db, user_id=user_id)
    return result
