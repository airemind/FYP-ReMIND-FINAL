from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.chat import Chat
from app.services.ai.text_adapter import process_text
from app.repositories.text_conversation_repo import (
    create_text_conversation,
    get_chat_conversations,
)
from app.logs.ai_logger import ai_logger
from app.logs.error_logger import error_logger
from app.services.admin.metric_logger_service import store_metric


def process_and_store_text(
    db: Session,
    user_id: int,
    user_input: str,
    chat_id: int = None,
    audio=None,
    image=None,
    document=None,
    profile=None,
    session_id: str = "unknown",
):

    try:

        ai_logger.info("Text orchestration started")

        # Recent Conversations
        recent_conversations = get_chat_conversations(
            db,
            chat_id=chat_id,
        )
        recent_conversations = recent_conversations[-6:]
        serialized_conversations = []

        for convo in recent_conversations:
            serialized_conversations.append(
                {
                    "user_input": convo.user_input,
                    "ai_response": convo.ai_response,
                    "intent": convo.detected_intent,
                }
            )

        # AI Processing
        ai_result = process_text(
            user_input=user_input,
            audio=audio,
            image=image,
            profile=profile,
            recent_conversations=serialized_conversations,
        )

        if not ai_result["success"]:
            return ai_result

        # Save Conversation
        conversation_data = {
            "user_id": user_id,
            "chat_id": chat_id,
            "user_input": user_input,
            "ai_response": ai_result["response"],
            "detected_intent": ai_result["intent"],
            "extracted_entities": ai_result["entities"],
            "retrieved_context": ai_result["retrieved_context"],
            "response_length": ai_result["metrics"]["response_length"],
            "latency_seconds": ai_result["metrics"]["latency_seconds"],
            "readability_score": ai_result["metrics"]["readability_score"],
            "model_used": ai_result["metadata"]["model"],
        }

        conversation = create_text_conversation(
            db,
            conversation_data,
        )

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
            "conversation_id": conversation.id,
            "response": conversation.ai_response,
            "intent": conversation.detected_intent,
            "entities": conversation.extracted_entities,
            "retrieved_context": conversation.retrieved_context,
            "metrics": {
                "response_length": conversation.response_length,
                "latency_seconds": conversation.latency_seconds,
                "readability_score": conversation.readability_score,
            },
            "model_used": conversation.model_used,
            "created_at": (
                str(conversation.created_at) if conversation.created_at else None
            ),
            "cache_used": False,
        }

        # Store Metrics
        store_metric(
            db=db,
            user_id=user_id,
            session_id=session_id,
            ai_module="TEXT_AI",
            pipeline_used="TEXT_AI",
            latency=result["metrics"]["latency_seconds"],
            estimated_cost=0.0,
            cache_used=result["cache_used"],
        )

        ai_logger.info("Text processing completed successfully")

        return result

    except Exception as e:

        error_logger.error(f"Text orchestration failed: {str(e)}")

        return {
            "success": False,
            "error": str(e),
        }
