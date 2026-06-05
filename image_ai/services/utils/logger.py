import os
import logging

from image_ai.config import LOGS_DIR

os.makedirs(LOGS_DIR, exist_ok=True)

# Log file path
LOG_FILE_PATH = os.path.join(LOGS_DIR, "enhancement.log")

# Creates logger
logger = logging.getLogger("ReMIND_Enhancement_Logger")
logger.setLevel(logging.INFO)

# Prevents duplicate handlers
if not logger.handlers:

    # Log format
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    # Writes logs to file
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Shows logs in terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Adds handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Info logs
def log_info(message, session_id=None):
    if session_id:
        logger.info(f"[Session: {session_id}] {message}")
    else:
        logger.info(message)

# Warning logs
def log_warning(message, session_id=None):
    if session_id:
        logger.warning(f"[Session: {session_id}] {message}")
    else:
        logger.warning(message)

# Error logs
def log_error(message, session_id=None):
    if session_id:
        logger.error(f"[Session: {session_id}] {message}")
    else:
        logger.error(message)
        
# Session separator
def log_separator():
    with open(LOG_FILE_PATH, "a") as log_file:
        log_file.write("\n---------------------------------------------------------------------------------------------\n")
