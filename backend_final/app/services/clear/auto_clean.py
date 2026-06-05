import os
import time
from app.logs.ai_logger import ai_logger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../../../"))


TEMP_FOLDERS = [
    os.path.join(PROJECT_ROOT, "temp"),
    os.path.join(PROJECT_ROOT, "temp_uploads"),
    os.path.join(PROJECT_ROOT, "temp_audio_uploads"),
    os.path.join(PROJECT_ROOT, "temp_image_uploads"),
]

MAX_AGE_SECONDS = 3600


def run_auto_cleanup():
    current_time = time.time()
    for folder in TEMP_FOLDERS:
        if not os.path.exists(folder):
            continue
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getmtime(file_path)
                    if file_age > MAX_AGE_SECONDS:
                        os.remove(file_path)
                        ai_logger.info(f"Deleted old temp file: " f"{file_path}")
            except Exception as e:
                ai_logger.error(f"Cleanup failed for " f"{file_path}: " f"{str(e)}")
