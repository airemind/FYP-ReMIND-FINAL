from fastapi import APIRouter, UploadFile, File

import os
import shutil
import uuid
from pathlib import Path
from app.services.ai.image_adapter import (
    enhance_uploaded_image as run_image_enhancement,
)
from app.services.storage.cloudinary_service import upload_image
from app.utils.file_cleanup import delete_file, delete_directory

router = APIRouter(prefix="/image-ai", tags=["Image AI"])

TEMP_DIR = "temp_uploads"


@router.post("/enhance")
async def enhance_image_route(file: UploadFile = File(...)):

    # ensure temp directory exists

    os.makedirs(TEMP_DIR, exist_ok=True)

    # safe filename generation

    file_extension = Path(file.filename).suffix
    safe_filename = f"{uuid.uuid4()}{file_extension}"
    temp_path = os.path.join(TEMP_DIR, safe_filename)

    # save temp file

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # run enhancement pipeline

    result = run_image_enhancement(temp_path)
    if not result["success"]:
        return result

    # cloudinary upload

    enhanced_upload = upload_image(result["enhanced_image"], folder="remind/enhanced")

    # cleanup

    delete_file(temp_path)
    delete_file(result["enhanced_image"])
    session_dir = os.path.dirname(result["enhanced_image"])
    delete_directory(session_dir)

    # response

    return {
        "success": True,
        "enhanced_url": (enhanced_upload["url"]),
        "metrics": (result["metrics"]),
        "pipeline_used": (result["pipeline_used"]),
    }
