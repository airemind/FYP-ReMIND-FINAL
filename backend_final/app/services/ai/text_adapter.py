import os
import sys

from app.config.settings import settings

AI_TEXT_PATH = settings.AI_TEXT_PATH
PROJECT_ROOT = os.path.dirname(AI_TEXT_PATH)
sys.path.append(PROJECT_ROOT)

from text_ai.pipeline.core_pipeline import run_pipeline


def process_text(
    user_input: str, audio=None, image=None, profile=None, recent_conversations=None
):
    return run_pipeline(
        user_input=user_input,
        audio=audio,
        image=image,
        profile=profile,
        conversation_history=recent_conversations,
    )
