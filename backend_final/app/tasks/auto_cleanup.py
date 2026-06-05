from app.services.clear.auto_clean import run_auto_cleanup
from app.logs.ai_logger import ai_logger
from app.logs.error_logger import error_logger


def cleanup_temp_files():
    try:
        run_auto_cleanup()
        ai_logger.info("Automatic cleanup completed")

    except Exception as e:
        error_logger.error(f"Automatic cleanup failed: " f"{str(e)}")
