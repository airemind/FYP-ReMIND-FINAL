# Voice AI Module — ReMIND

## Author
Muhammad Hassan Ashraf

## Responsibility
This module handles all voice-related AI services and data science tasks in ReMIND, including:
- Audio preprocessing
- Speech-to-text transcription
- Emotion & tone analysis
- Voice synthesis
- Evaluation & optimization

## Pipeline Overview
Audio → Format → Clean → Trim → ElevenLabs STT → Emotion/Tone → Text AI → ElevenLabs TTS → processed Audio

## Technologies Used
- ElevenLabs STT
- PyDub
- Librosa
- Google TTS
- Python

## How to Run
1. Activate virtual environment
2. Add API keys to `.env`
3. Run:
   python orchestration/voice_pipeline.py

## Output
- Transcription JSON
- Emotional metadata
- Generated voice memory

## Evaluation
Latency, cost, and accuracy metrics are calculated for performance validation.

## Limitations
- Depends on external APIs
- Emotion detection is rule-based
- Internet required

## Future Improvements
- ML-based emotion classifier
- Multilingual speech support
- Voice personalization
