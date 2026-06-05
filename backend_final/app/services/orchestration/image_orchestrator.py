import os
import hashlib
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.chat import Chat
from app.services.ai.image_adapter import process_image
from app.services.ai.text_adapter import process_text
from app.services.storage.cloudinary_service import upload_image
from app.models.media import Media
from app.logs.ai_logger import ai_logger
from app.logs.error_logger import error_logger
from app.cache.redis_cache import get_cache, set_cache
from app.utils.file_cleanup import delete_file, delete_directory
from app.services.admin.metric_logger_service import store_metric


def process_and_store_image(
    image_path: str,
    db: Session,
    user_id: int,
    chat_id: int = None,
    profile=None,
    patient_profile=None,
    session_id: str = "unknown",
):

    try:
        ai_logger.info("Image orchestration started")

        filename = os.path.basename(image_path)

        # Cache Hash
        with open(image_path, "rb") as f:
            file_hash = hashlib.md5(f.read()).hexdigest()

        cache_key = f"image:{file_hash}"

        # Cache Check
        cached_response = get_cache(cache_key)

        if cached_response:
            ai_logger.info("Image cache hit")
            return cached_response

        # Image AI Processing
        image_result = process_image(image_path)

        if not image_result["success"]:
            return image_result

        # Memory AI Processing
        text_result = process_text(
            user_input=image_result["caption"],
            image={"caption": image_result["caption"]},
            profile=profile,
        )

        memory_response = text_result.get("response", image_result["caption"])

        # Cloudinary Uploads
        original_upload = upload_image(image_path, folder="remind/original")

        enhanced_upload = upload_image(
            image_result["enhanced_image"], folder="remind/enhanced"
        )

        # Save Media
        media = Media(
            user_id=user_id,
            chat_id=chat_id,
            media_type="image",
            original_url=original_upload["url"],
            enhanced_url=enhanced_upload["url"],
            caption=memory_response,
        )

        db.add(media)
        db.commit()
        db.refresh(media)

        # Update Chat Activity
        if chat_id:

            chat = db.query(Chat).filter(Chat.id == chat_id).first()

            if chat:
                chat.last_activity = datetime.now(timezone.utc)
                chat.message_count += 1
                db.commit()

        # Final Response
        result = {
            "success": True,
            "media_id": media.id,
            "caption": image_result["caption"],
            "memory_response": memory_response,
            "intent": text_result["intent"],
            "entities": text_result["entities"],
            "retrieved_context": text_result["retrieved_context"],
            "original_url": original_upload["url"],
            "enhanced_url": enhanced_upload["url"],
            "metrics": image_result["metrics"],
            "pipeline_used": ["IMAGE_AI", "TEXT_AI"],
            "cache_used": False,
        }

        # Store Metrics
        store_metric(
            db=db,
            user_id=user_id,
            session_id=session_id,
            ai_module="IMAGE_AI",
            pipeline_used="IMAGE_AI,TEXT_AI",
            latency=image_result["metrics"]["processing_time"],
            estimated_cost=0.0,
            cache_used=result["cache_used"],
        )

        # Save Cache
        set_cache(cache_key, result, expiration=3600)

        # Cleanup Files
        delete_file(image_path)
        delete_file(image_result["enhanced_image"])

        session_dir = os.path.dirname(image_result["enhanced_image"])

        delete_directory(session_dir)

        ai_logger.info("Image orchestration completed successfully")

        return result

    except Exception as e:

        error_logger.error(f"Image orchestration failed: {str(e)}")

        return {
            "success": False,
            "error": str(e),
        }
