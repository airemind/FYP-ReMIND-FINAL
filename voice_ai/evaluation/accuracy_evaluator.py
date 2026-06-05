import re


def evaluate_transcription_quality(transcript: str) -> dict:
    words = transcript.split()
    total_words = len(words)

    if total_words == 0:
        return {"word_count": 0, "confidence_score": 0, "clarity_score": 0}

    # simple heuristic metrics
    unique_words = len(set(words))
    repetition_ratio = unique_words / total_words

    spelling_errors = len(re.findall(r"[^a-zA-Z0-9\s.,!?']", transcript))

    clarity_score = round(repetition_ratio * 100, 2)

    confidence_score = max(0, round(100 - spelling_errors * 2, 2))

    return {
        "word_count": total_words,
        "clarity_score": clarity_score,
        "confidence_score": confidence_score,
    }
