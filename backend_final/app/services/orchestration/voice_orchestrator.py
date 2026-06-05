import os
import uuid
import hashlib
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.chat import Chat
from app.models.media import Media
from app.services.ai.voice_adapter import process_voice
from app.services.ai.text_adapter import process_text
from app.services.storage.cloudinary_service import upload_audio
from app.logs.ai_logger import ai_logger
from app.logs.error_logger import error_logger
from app.cache.redis_cache import get_cache, set_cache
from app.utils.file_cleanup import (
    delete_file,
    delete_directory,
)

from voice_ai.synthesis.google_tts import generate_speech
from app.services.admin.metric_logger_service import (
    store_metric,
)


def process_and_store_voice(
    audio_path: str,
    db: Session,
    user_id: int,
    chat_id: int = None,
    session_id: str = "unknown",
):
    try:
        ai_logger.info("Voice orchestration started")
        filename = os.path.basename(audio_path)
        # Cache Hash
        with open(audio_path, "rb") as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        cache_key = f"voice:{file_hash}"
        # Cache Check
        cached_response = get_cache(cache_key)
        if cached_response:
            ai_logger.info("Voice cache hit")
            return cached_response

        # Voice AI
        voice_result = process_voice(
            audio_path,
            force_refresh=True,
        )

        transcript = voice_result["transcript"]

        # Memory AI Processing
        text_result = process_text(
            user_input=transcript,
            audio={
                "transcript": transcript,
                "emotion": voice_result["emotion"],
                "tones": voice_result["tones"],
            },
        )

        memory_response = text_result["response"]
        # Generate Speech
        generated_audio_path = f"/tmp/{uuid.uuid4()}.mp3"
        generate_speech(
            memory_response,
            generated_audio_path,
        )

        # Cloudinary Uploads
        original_upload = upload_audio(
            voice_result["audio_path"],
            folder="remind/audio/original",
        )

        generated_upload = upload_audio(
            generated_audio_path,
            folder="remind/audio/generated",
        )

        # Save Media
        media = Media(
            user_id=user_id,
            chat_id=chat_id,
            media_type="audio",
            original_url=original_upload["url"],
            enhanced_url=generated_upload["url"],
            caption=memory_response,
        )

        db.add(media)
        db.commit()
        db.refresh(media)

        # Final Response
        result = {
            "success": True,
            "media_id": media.id,
            "transcript": transcript,
            "memory_response": memory_response,
            "intent": text_result["intent"],
            "entities": text_result["entities"],
            "retrieved_context": text_result["retrieved_context"],
            "language": voice_result["language"],
            "confidence": voice_result["confidence"],
            "spelling_accuracy": voice_result["spelling_accuracy"],
            "emotion": voice_result["emotion"],
            "emotion_confidence": voice_result["emotion_confidence"],
            "tones": voice_result["tones"],
            "tone_strength": voice_result["tone_strength"],
            "latency_sec": voice_result["latency_sec"],
            "audio_duration_sec": voice_result["audio_duration_sec"],
            "estimated_cost_usd": voice_result["estimated_cost_usd"],
            "quality_metrics": voice_result["quality_metrics"],
            "original_audio_url": original_upload["url"],
            "generated_audio_url": generated_upload["url"],
            "pipeline_used": [
                "VOICE_AI",
                "TEXT_AI",
            ],
            "cache_used": False,
        }

        # Store Metrics
        store_metric(
            db=db,
            user_id=user_id,
            session_id=session_id,
            ai_module="VOICE_AI",
            pipeline_used="VOICE_AI,TEXT_AI",
            latency=voice_result["latency_sec"],
            estimated_cost=voice_result["estimated_cost_usd"],
            cache_used=result["cache_used"],
        )

        # Update Chat Activity
        if chat_id:
            chat = db.query(Chat).filter(Chat.id == chat_id).first()
            if chat:
                chat.last_activity = datetime.now(timezone.utc)
                chat.message_count += 1
                db.commit()

        # Save Cache
        set_cache(
            cache_key,
            result,
            expiration=3600,
        )

        # Cleanup Files
        delete_file(audio_path)
        delete_file(voice_result.get("audio_path"))
        delete_file(generated_audio_path)
        processed_dir = os.path.dirname(voice_result.get("audio_path"))
        delete_directory(processed_dir)
        ai_logger.info("Voice processing completed successfully")
        return result
    except Exception as e:
        error_logger.error(f"Voice orchestration failed: {str(e)}")

        return {
            "success": False,
            "error": str(e),
        }
