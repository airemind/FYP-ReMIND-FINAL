import re


def clean_text(text: str) -> str:
    """Basic cleaning"""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def combine_texts(texts: list) -> str:
    """Combine multiple texts into one"""
    return "\n".join([t for t in texts if t])


def truncate_text(text: str, max_length: int = 2000) -> str:
    """Limit input size"""
    return text[:max_length]
