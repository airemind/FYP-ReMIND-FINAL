import os
import shutil
from app.logs.ai_logger import ai_logger
from app.logs.error_logger import error_logger


def delete_file(file_path: str):

    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            ai_logger.info(f"Deleted file: {file_path}")

    except Exception as e:
        error_logger.error(f"File deletion failed: {str(e)}")


def delete_directory(directory_path: str):

    try:
        if directory_path and os.path.exists(directory_path):
            shutil.rmtree(directory_path)
            ai_logger.info(f"Deleted directory: {directory_path}")

    except Exception as e:
        error_logger.error(f"Directory deletion failed: {str(e)}")
