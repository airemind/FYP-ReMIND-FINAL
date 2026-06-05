import os
import pickle
import faiss
import numpy as np
from text_ai.config.config import settings


class VectorStore:

    def __init__(self):

        self.dim = settings.EMBEDDING_DIM
        self.path = settings.VECTOR_DB_PATH
        self.index = faiss.IndexFlatIP(self.dim)
        self.texts = []
        self.load()

    # add memory

    def add(self, embedding, text):
        embedding = np.array([embedding], dtype="float32")
        faiss.normalize_L2(embedding)
        self.index.add(embedding)
        self.texts.append(text)

    # search memory
    def search(self, embedding, k=None):
        if len(self.texts) == 0:
            return []
        if k is None:
            k = min(settings.TOP_K, len(self.texts))
        embedding = np.array([embedding], dtype="float32")
        faiss.normalize_L2(embedding)
        scores, indices = self.index.search(embedding, k)
        results = []
        similarity_threshold = 0.25
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            if score < similarity_threshold:
                continue
            if idx < len(self.texts):
                results.append(self.texts[idx])
        return results

    # save

    def save(self):
        os.makedirs(self.path, exist_ok=True)
        faiss.write_index(self.index, os.path.join(self.path, "faiss_index.bin"))
        with open(os.path.join(self.path, "texts.pkl"), "wb") as f:
            pickle.dump(self.texts, f)

    # load
    def load(self):
        index_path = os.path.join(self.path, "faiss_index.bin")
        text_path = os.path.join(self.path, "texts.pkl")
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        if os.path.exists(text_path):
            with open(text_path, "rb") as f:
                self.texts = pickle.load(f)
