MEMORY_KEYWORDS = [
    "remember",
    "memory",
    "recall",
    "forgot",
    "forget",
    "past",
    "childhood",
    "family",
    "wedding",
    "friend",
    "mother",
    "father",
    "event",
    "name",
    "recognize",
]

NON_MEMORY_KEYWORDS = [
    "assignment",
    "homework",
    "code",
    "programming",
    "math",
    "calculate",
    "essay",
    "project",
    "exam",
    "quiz",
    "python",
    "java",
    "javascript",
]


def classify_intent(text: str):
    text = text.lower()

    memory_score = 0
    non_memory_score = 0

    for word in MEMORY_KEYWORDS:
        if word in text:
            memory_score += 1

    for word in NON_MEMORY_KEYWORDS:
        if word in text:
            non_memory_score += 1

    # Reject non-memory prompts
    if non_memory_score > memory_score:
        return "restricted"

    # Memory-related intents
    if memory_score > 0:
        return "memory_recall"

    return "general"
