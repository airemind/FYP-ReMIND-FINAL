import time


def evaluate_response(response: str, start_time: float, context: list):
    end_time = time.time()

    # Basic metrics
    length = len(response)
    latency = round(end_time - start_time, 2)

    # Context usage score
    context_hits = sum(1 for c in context if c[:30] in response)
    context_score = context_hits / max(len(context), 1)

    # Readability (very basic)
    sentence_count = response.count(".") + 1
    readability = length / max(sentence_count, 1)

    metrics = {
        "response_length": length,
        "latency_seconds": latency,
        "context_usage_score": round(context_score, 2),
        "readability_score": round(readability, 2),
    }

    metadata = {
        "model": "llama-3.3-70b",
        "language": "en",
        "intent_detected": True,
        "context_used": len(context),
        "status": "success",
    }

    return metrics, metadata
