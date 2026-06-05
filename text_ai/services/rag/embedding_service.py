from sentence_transformers import SentenceTransformer
import numpy as np

from text_ai.config.config import settings

# load modal once

model = SentenceTransformer(settings.EMBEDDING_MODEL)


def get_embedding(text: str):
    if not text:
        return np.zeros(settings.EMBEDDING_DIM, dtype="float32")
    text = text.strip()
    if not text:
        return np.zeros(settings.EMBEDDING_DIM, dtype="float32")
    embedding = model.encode(text, normalize_embeddings=True)
    return np.array(embedding, dtype="float32")
