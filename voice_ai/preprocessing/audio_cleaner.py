"""
audio_cleaner.py

Normalizes audio volume to ensure consistent
signal strength and clarity.
"""

from pydub import AudioSegment
from voice_ai.utils.logger import get_logger

logger = get_logger("AudioCleaner")


def clean_audio(input_path: str, output_path: str) -> str:
    """
    Normalize audio volume.

    Args:
        input_path (str): Formatted WAV file.
        output_path (str): Cleaned WAV file.

    Returns:
        str: Path to cleaned audio file.
    """
    audio = AudioSegment.from_wav(input_path)
    audio = audio.normalize()

    audio.export(output_path, format="wav")
    logger.info("Audio cleaning completed")

    return output_path
