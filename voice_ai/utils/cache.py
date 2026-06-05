"""
cache.py

Caching utility for Voice AI module.
"""

import json
import os
import hashlib

CACHE_FILE = "voice_cache.json"


def _hash_path(path: str) -> str:
    return hashlib.md5(path.encode()).hexdigest()


def load_cache() -> dict:
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_cache(key: str, value: dict):
    cache = load_cache()
    cache[key] = value
    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(cache, file, indent=2)


def get_cached_transcription(audio_path: str):
    cache = load_cache()
    key = _hash_path(audio_path)
    return cache.get(key)


def cache_transcription(audio_path: str, data: dict):
    key = _hash_path(audio_path)
    save_cache(key, data)
