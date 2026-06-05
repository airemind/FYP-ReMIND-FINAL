import logging
import os
from datetime import datetime

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)
audit_logger = logging.getLogger("admin_audit")
audit_logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"{LOG_DIR}/admin_audit.log")
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
handler.setFormatter(formatter)
audit_logger.addHandler(handler)


def log_admin_action(admin_id: str, action: str, target: str = None):
    message = f"ADMIN={admin_id} | " f"ACTION={action}"
    if target:
        message += f" | TARGET={target}"
    audit_logger.info(message)
