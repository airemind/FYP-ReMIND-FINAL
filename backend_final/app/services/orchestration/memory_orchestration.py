from sqlalchemy.orm import Session

from app.services.orchestration.image_orchestrator import process_and_store_image
from app.services.orchestration.voice_orchestrator import process_and_store_voice
from app.services.orchestration.text_orchestrator import process_and_store_text

from app.repositories.message_repo import create_message

from app.logs.ai_logger import ai_logger
from app.logs.error_logger import error_logger


def process_multimodal_memory(
    db: Session,
    user_id: int,
    chat_id: int = None,
    image_path: str = None,
    audio_path: str = None,
    user_prompt: str = None,
    profile: dict = None,
):

    try:

        ai_logger.info("Multimodal orchestration started")

        image_result = None
        voice_result = None

        image_caption = None
        audio_transcript = None

        # Save User Message
        user_message_parts = []

        if user_prompt:
            user_message_parts.append(user_prompt)

        if image_path:
            user_message_parts.append("[Image Uploaded]")

        if audio_path:
            user_message_parts.append("[Audio Uploaded]")

        user_message_content = "\n".join(user_message_parts)

        create_message(
            db,
            {
                "chat_id": chat_id,
                "sender": "user",
                "content": user_message_content,
                "message_type": "memory",
            },
        )

        # Image AI
        if image_path:

            image_result = process_and_store_image(
                image_path=image_path,
                db=db,
                user_id=user_id,
                chat_id=chat_id,
            )

            if image_result["success"]:
                image_caption = image_result["caption"]

        # Voice AI
        if audio_path:

            voice_result = process_and_store_voice(
                audio_path=audio_path,
                db=db,
                user_id=user_id,
                chat_id=chat_id,
            )

            if voice_result["success"]:
                audio_transcript = voice_result["transcript"]

        # Build Multimodal Input
        combined_input = []

        if user_prompt:
            combined_input.append(f"User Prompt: {user_prompt}")

        if image_caption:
            combined_input.append(f"Image Caption: {image_caption}")

        if audio_transcript:
            combined_input.append(f"Audio Transcript: {audio_transcript}")

        final_input = "\n".join(combined_input)

        # Text AI
        text_result = process_and_store_text(
            db=db,
            user_id=user_id,
            user_input=final_input,
            chat_id=chat_id,
            audio=voice_result,
            image=image_result,
            profile=profile,
        )

        # Final Response
        final_response = (
            text_result.get("response") or "Memory reconstructed successfully."
        )

        # Save Assistant Message
        create_message(
            db,
            {
                "chat_id": chat_id,
                "sender": "assistant",
                "content": final_response,
                "message_type": "memory",
                "caption": (image_result.get("caption") if image_result else None),
                "enhanced_image": (
                    image_result.get("enhanced_url") if image_result else None
                ),
                "generated_audio": (
                    voice_result.get("generated_audio_url") if voice_result else None
                ),
                "transcript": (
                    voice_result.get("transcript") if voice_result else None
                ),
                "emotion": (voice_result.get("emotion") if voice_result else None),
                "tones": (voice_result.get("tones", []) if voice_result else []),
                "retrieved_context": text_result.get(
                    "retrieved_context",
                    [],
                ),
            },
        )

        ai_logger.info("Multimodal orchestration completed")

        return {
            "success": True,
            "image_ai": image_result,
            "voice_ai": voice_result,
            "text_ai": text_result,
            "final_memory_response": text_result.get("response"),
        }

    except Exception as e:

        error_logger.error(f"Multimodal orchestration failed: {str(e)}")

        return {
            "success": False,
            "error": str(e),
        }
