import json
import os


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def read_text_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
