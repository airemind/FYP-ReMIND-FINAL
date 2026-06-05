import hashlib


class SimpleCache:
    def __init__(self):
        self.cache = {}

    def generate_key(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def get(self, text):
        key = self.generate_key(text)
        return self.cache.get(key)

    def set(self, text, value):
        key = self.generate_key(text)
        self.cache[key] = value
