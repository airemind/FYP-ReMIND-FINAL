import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")
CACHE_DIR = os.path.join(BASE_DIR, "cache")
EVALUATION_DIR = os.path.join(BASE_DIR, "evaluation_results")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(EVALUATION_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
