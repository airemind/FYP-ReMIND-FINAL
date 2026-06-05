"""
voice_config.py

Configuration module for Voice AI services in ReMIND.
Handles environment variables and voice-related constants.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class VoiceConfig:
    """
    Configuration container for voice-related settings.

    This class stores API keys and constants required
    for speech-to-text and text-to-speech processing.
    """

    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    SAMPLE_RATE = 16000
    AUDIO_FORMAT = "wav"
