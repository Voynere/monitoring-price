from __future__ import annotations

from core.models import RetrievedChunk


class SimpleReranker:
    """Lightweight reranker: boosts code chunks for architecture questions."""

    CODE_HINTS = ("class", "function", "parser", "fallback", "usecase", "handler")

    def rerank(self, question: str, chunks: list[RetrievedChunk], top_k: int = 8) -> list[RetrievedChunk]:
        lowered = question.lower()
        wants_code = any(hint in lowered for hint in self.CODE_HINTS)

        def score(chunk: RetrievedChunk) -> float:
            bonus = 0.0
            if wants_code and chunk.metadata.source_type.value == "code":
                bonus += 0.1
            if chunk.metadata.path.endswith(".php"):
                bonus += 0.05
            return chunk.score + bonus

        return sorted(chunks, key=score, reverse=True)[:top_k]
