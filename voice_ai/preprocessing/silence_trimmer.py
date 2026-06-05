"""
silence_trimmer.py

Removes long silent segments from audio.
"""

from pydub import AudioSegment
from pydub.silence import split_on_silence
from voice_ai.utils.logger import get_logger

logger = get_logger("SilenceTrimmer")


def trim_silence(
    input_path: str,
    output_path: str,
    min_silence_len: int = 700,
    silence_thresh: int = -40,
) -> str:
    """
    Trim silence from audio.

    Args:
        input_path (str): Cleaned WAV file.
        output_path (str): Final trimmed audio.
    """
    audio = AudioSegment.from_wav(input_path)

    chunks = split_on_silence(
        audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh
    )

    if not chunks:
        audio.export(output_path, format="wav")
        logger.info("No silence detected")
        return output_path

    trimmed_audio = sum(chunks)
    trimmed_audio.export(output_path, format="wav")  # type: ignore

    logger.info("Silence trimming completed")
    return output_path
