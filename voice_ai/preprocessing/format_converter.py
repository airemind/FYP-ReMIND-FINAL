"""
format_converter.py

Converts any supported audio format into a
standard WAV format (16kHz, mono).
"""

from pydub import AudioSegment
from voice_ai.utils.logger import get_logger

logger = get_logger("FormatConverter")


def convert_to_wav(input_path: str, output_path: str) -> str:
    """
    Convert audio to WAV format (16kHz, mono).

    Args:
        input_path (str): Raw audio file path.
        output_path (str): Output WAV file path.

    Returns:
        str: Path to formatted WAV file.
    """
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    audio.export(output_path, format="wav")
    logger.info("Audio formatting completed")

    return output_path
