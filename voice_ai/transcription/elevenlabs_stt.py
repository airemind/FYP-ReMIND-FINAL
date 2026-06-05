"""
elevenlabs_stt.py

Handles Speech-to-Text transcription using ElevenLabs API.
Also computes language detection and confidence score.
"""

import os
import requests
from langdetect import detect, LangDetectException
from spellchecker import SpellChecker
from voice_ai.config.voice_config import VoiceConfig
from voice_ai.utils.logger import get_logger

logger = get_logger("ElevenLabsSTT")

ELEVENLABS_STT_URL = "https://api.elevenlabs.io/v1/speech-to-text"


def _spelling_accuracy(text: str) -> float:
    """
    Calculate spelling accuracy of transcript.
    """
    spell = SpellChecker()
    words = text.lower().split()
    if len(words) == 0:
        return 0.0
    misspelled = spell.unknown(words)
    correct_words = len(words) - len(misspelled)
    accuracy = correct_words / len(words)
    return round(accuracy, 2)


def _detect_language(text: str) -> str:
    """Detect language from transcript."""
    try:
        return detect(text)
    except (LangDetectException, ValueError):
        return "unknown"


def _estimate_confidence(text: str) -> float:
    """
    Estimate transcription confidence using
    multiple heuristics.
    """
    words = text.split()
    if len(words) == 0:
        return 0.0
    score = 0.6
    # punctuation
    if "." in text or "," in text:
        score += 0.1
    # length bonus
    if len(words) > 10:
        score += 0.1
    # filler penalty
    fillers = ["uh", "um", "ah"]
    filler_count = sum(1 for w in words if w.lower() in fillers)
    if filler_count > 0:
        score -= 0.05
    # spelling accuracy
    spelling_score = _spelling_accuracy(text)
    score += spelling_score * 0.2
    return round(min(score, 0.99), 2)


def transcribe_audio(audio_path: str) -> dict:
    """
    Transcribe audio using ElevenLabs STT.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    headers = {"xi-api-key": VoiceConfig.ELEVENLABS_API_KEY}
    data = {"model_id": "scribe_v1"}
    with open(audio_path, "rb") as audio_file:
        files = {"file": ("audio.wav", audio_file, "audio/wav")}
        logger.info("Sending audio to ElevenLabs STT")
        response = requests.post(
            ELEVENLABS_STT_URL, headers=headers, data=data, files=files, timeout=60
        )

    if response.status_code != 200:
        raise RuntimeError(
            f"ElevenLabs STT failed: {response.status_code} - {response.text}"
        )
    result = response.json()
    transcript = result.get("text", "")
    language = _detect_language(transcript)
    confidence = _estimate_confidence(transcript)
    spelling_score = _spelling_accuracy(transcript)
    logger.info("Transcription received from ElevenLabs")

    return {
        "transcript": transcript,
        "language": language,
        "confidence": confidence,
        "spelling_accuracy": spelling_score,
        "provider": "ElevenLabs",
    }
