"""
tone_classifier.py

Advanced AI-powered tone classification
for ReMIND.

Uses GoEmotions model.

Detects:
- nostalgic
- reflective
- appreciative
- joyful
- emotional
- sad
- caring
- curious
- excited
- neutral

Returns:
primary tone
top tones
tone strength
"""

from transformers import pipeline

from voice_ai.utils.logger import get_logger

logger = get_logger("ToneClassifier")

tone_pipeline = pipeline(
    "text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None
)


MAX_TEXT_LENGTH = 512


# geomotion to human tone mapping

TONE_MAPPING = {
    "admiration": "appreciative",
    "amusement": "joyful",
    "approval": "positive",
    "caring": "caring",
    "curiosity": "curious",
    "desire": "hopeful",
    "excitement": "excited",
    "gratitude": "appreciative",
    "joy": "joyful",
    "love": "emotional",
    "nostalgia": "nostalgic",
    "optimism": "hopeful",
    "pride": "confident",
    "realization": "reflective",
    "relief": "relieved",
    "sadness": "sad",
    "surprise": "surprised",
    "neutral": "neutral",
}


# classify tone


def classify_tone(text: str) -> dict:
    try:
        if not text or not text.strip():
            return {
                "tones": ["neutral"],
                "primary_tone": "neutral",
                "tone_strength": 0.0,
            }
        text = text.strip()
        if len(text) > MAX_TEXT_LENGTH:
            text = text[:MAX_TEXT_LENGTH]
        predictions = tone_pipeline(text)[0]
        predictions = sorted(predictions, key=lambda x: x["score"], reverse=True)
        tones = []
        for item in predictions[:5]:
            label = item["label"].lower()
            mapped_tone = TONE_MAPPING.get(label, label)
            if mapped_tone not in tones:
                tones.append(mapped_tone)
        primary_label = predictions[0]["label"].lower()
        primary_tone = TONE_MAPPING.get(primary_label, primary_label)
        tone_strength = round(float(predictions[0]["score"]), 2)
        result = {
            "tones": tones,
            "primary_tone": primary_tone,
            "tone_strength": tone_strength,
        }
        logger.info(f"Tone detected: " f"{primary_tone} " f"({tone_strength})")
        return result

    except Exception as e:
        logger.error(f"Tone classification failed: " f"{str(e)}")
        return {"tones": ["neutral"], "primary_tone": "neutral", "tone_strength": 0.0}
