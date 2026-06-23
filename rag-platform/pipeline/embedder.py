from __future__ import annotations

import hashlib
import math
import os

from core.contracts import EmbedderPort
from pipeline.config import Settings


class HashEmbedder(EmbedderPort):
    """Deterministic lightweight embedder for dev/tests without ML deps."""

    def __init__(self, dimension: int = 1024) -> None:
        self._dimension = dimension

    @property
    def dimension(self) -> int:
        return self._dimension

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]

    def _embed_one(self, text: str) -> list[float]:
        seed = hashlib.sha256(text.encode("utf-8")).digest()
        values: list[float] = []
        counter = 0
        while len(values) < self._dimension:
            block = hashlib.sha256(seed + counter.to_bytes(4, "big")).digest()
            for byte in block:
                values.append((byte / 127.5) - 1.0)
                if len(values) >= self._dimension:
                    break
            counter += 1
        norm = math.sqrt(sum(v * v for v in values)) or 1.0
        return [v / norm for v in values]


class SentenceTransformerEmbedder(EmbedderPort):
    def __init__(self, model_name: str) -> None:
        from sentence_transformers import SentenceTransformer

        self._model = SentenceTransformer(model_name)
        self._dimension = int(self._model.get_sentence_embedding_dimension())

    @property
    def dimension(self) -> int:
        return self._dimension

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors = self._model.encode(texts, normalize_embeddings=True)
        return [vector.tolist() for vector in vectors]


def build_embedder(settings: Settings) -> EmbedderPort:
    if os.getenv("RAG_USE_ML_EMBEDDER") == "1":
        return SentenceTransformerEmbedder(settings.embedding_model)
    return HashEmbedder(settings.embedding_dimension)
