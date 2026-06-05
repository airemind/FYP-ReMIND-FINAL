"""
emotion_detector.py

Advanced emotion detection for ReMIND.

Features:
- Multi-emotion detection
- Long transcript support
- Confidence scoring
- Emotion ranking
- Robust error handling
"""

from transformers import pipeline

from voice_ai.utils.logger import get_logger

logger = get_logger("EmotionDetector")

# load model once

emotion_pipeline = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None,
)

# config

MAX_TEXT_LENGTH = 512


# detect emotion with confidence scores and ranking
def detect_emotion(text: str) -> dict:
    try:
        if not text or not text.strip():
            return {
                "emotion": "neutral",
                "emotion_confidence": 0.0,
                "top_emotions": [{"label": "neutral", "confidence": 0.0}],
            }

        text = text.strip()

        # limit long transcripts

        if len(text) > MAX_TEXT_LENGTH:
            text = text[:MAX_TEXT_LENGTH]
        predictions = emotion_pipeline(text)[0]
        predictions = sorted(predictions, key=lambda x: x["score"], reverse=True)
        primary = predictions[0]
        top_emotions = []
        for item in predictions[:3]:
            top_emotions.append(
                {
                    "label": item["label"].lower(),
                    "confidence": round(float(item["score"]), 2),
                }
            )
        result = {
            "emotion": primary["label"].lower(),
            "emotion_confidence": round(float(primary["score"]), 2),
            "top_emotions": top_emotions,
        }
        logger.info(
            f"Emotion detected: {result['emotion']} "
            f"({result['emotion_confidence']})"
        )
        return result
    except Exception as e:
        logger.error(f"Emotion detection failed: {str(e)}")
        return {
            "emotion": "neutral",
            "emotion_confidence": 0.0,
            "top_emotions": [{"label": "neutral", "confidence": 0.0}],
        }
