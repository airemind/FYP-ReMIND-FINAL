from apscheduler.schedulers.background import BackgroundScheduler
from app.tasks.chat_cleanup import delete_expired_chats
from app.tasks.auto_cleanup import cleanup_temp_files
from app.logs.ai_logger import ai_logger

scheduler = BackgroundScheduler()


def start_scheduler():
    # DELETE OLD CHATS
    scheduler.add_job(delete_expired_chats, trigger="interval", hours=24)

    # CLEAN TEMP FILES
    scheduler.add_job(cleanup_temp_files, trigger="interval", minutes=5)

    scheduler.start()
    ai_logger.info("APScheduler started successfully")
