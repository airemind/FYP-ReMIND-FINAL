import os


def estimate_audio_duration(file_path: str) -> float:
    """
    Rough duration estimation (in seconds)
    """
    file_size = os.path.getsize(file_path)  # bytes
    bitrate = 16000  # approx for WAV (16kbps)
    duration = file_size / bitrate
    return round(duration, 2)


def estimate_stt_cost(duration_sec: float) -> float:
    """
    Simulated cost calculation
    """
    cost_per_minute = 0.006  # approx
    minutes = duration_sec / 60
    return round(minutes * cost_per_minute, 5)
