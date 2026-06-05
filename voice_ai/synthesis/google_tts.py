"""
tts.py (Local fallback using gTTS)
"""

from gtts import gTTS
from voice_ai.utils.logger import get_logger

logger = get_logger("LocalTTS")


def generate_speech(text: str, output_path: str) -> str:
    """
    Convert text to speech using gTTS (FREE + reliable)
    """
    if not text.strip():
        raise ValueError("Empty text for TTS")
    logger.info("Generating speech using gTTS")
    tts = gTTS(text=text, lang="en")
    tts.save(output_path)
    logger.info("Audio generated successfully (gTTS)")
    return output_path
