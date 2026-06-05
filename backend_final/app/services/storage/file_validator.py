ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]
ALLOWED_AUDIO_TYPES = ["audio/mpeg", "audio/wav", "audio/x-wav"]
ALLOWED_TEXT_TYPES = ["text/plain"]
MAX_FILE_SIZE = 50 * 1024 * 1024


def validate_file(content_type: str, file_size: int):
    allowed_types = ALLOWED_IMAGE_TYPES + ALLOWED_AUDIO_TYPES + ALLOWED_TEXT_TYPES

    if content_type not in allowed_types:
        return False

    if file_size > MAX_FILE_SIZE:
        return False

    return True
