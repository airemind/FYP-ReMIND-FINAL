import os
import sys

from app.config.settings import settings

AI_VOICE_PATH = settings.AI_VOICE_PATH
PROJECT_ROOT = os.path.dirname(AI_VOICE_PATH)
sys.path.append(PROJECT_ROOT)
from voice_ai.orchestration.voice_pipeline import run_voice_pipeline


def process_voice(
    audio_path: str, response_text: str = None, force_refresh: bool = False
):
    return run_voice_pipeline(
        input_audio_path=audio_path,
        response_text=response_text,
        force_refresh=force_refresh,
    )
