import os
import hashlib
import shutil

from image_ai.config import CACHE_DIR

os.makedirs(CACHE_DIR, exist_ok=True)

print("USING CACHER:", __file__)

# Generates unique hash for image
def generate_image_hash(image_path):
    hasher = hashlib.sha256()
    with open(image_path, "rb") as image_file:
        while chunk := image_file.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()
    
# Creates cache folder path
def get_cache_path(image_hash):
    return os.path.join(CACHE_DIR, image_hash)
    
# Checks cached result
def is_cached(image_hash):
    cache_path = get_cache_path(image_hash)
    return os.path.exists(cache_path)
    
# Saves enhanced image and caption
def save_to_cache(image_hash, image_path, caption=""):
    cache_path = get_cache_path(image_hash)
    os.makedirs(cache_path, exist_ok=True)
    cached_image_path = os.path.join(cache_path,"enhanced_image.png")

    shutil.copy(image_path, cached_image_path)
    caption_path = os.path.join(cache_path, "caption.txt")

    with open(caption_path, "w") as file:
        file.write(caption or "")

# Loads cached result
def load_from_cache(image_hash):
    cache_path = get_cache_path(image_hash)
    image_path = os.path.join(cache_path, "enhanced_image.png")
    caption_path = os.path.join(cache_path,"caption.txt")

    with open(caption_path, "r") as file:
        caption = file.read()

    return {
        "enhanced_image": image_path,
        "caption": caption,
        "metrics": {
           "caption_time": 0.0,
           "processing_time": 0.0
        },
        "cache_used": True
    }
