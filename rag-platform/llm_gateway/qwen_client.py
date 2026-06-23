from __future__ import annotations

import time

import httpx

from core.contracts import LlmGatewayPort
from core.models import RagAnswer, RagQueryRequest, RetrievedChunk
from pipeline.config import Settings


class QwenLlmGateway(LlmGatewayPort):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def generate(self, request: RagQueryRequest, chunks: list[RetrievedChunk]) -> RagAnswer:
        started = time.perf_counter()
        prompt = self._build_prompt(request, chunks)
        try:
            answer_text = self._call_llm(request.model, prompt)
        except (httpx.HTTPError, httpx.TimeoutException):
            answer_text = self._fallback_answer(request, chunks)

        latency_ms = int((time.perf_counter() - started) * 1000)
        return RagAnswer(
            answer=answer_text,
            citations=chunks,
            model=request.model,
            latency_ms=latency_ms,
        )

    def _build_prompt(self, request: RagQueryRequest, chunks: list[RetrievedChunk]) -> str:
        context_lines = []
        for chunk in chunks:
            context_lines.append(
                f"{chunk.citation_id} path={chunk.metadata.path} module={chunk.metadata.module}\n{chunk.content[:1200]}"
            )
        context = "\n\n".join(context_lines) or "No retrieved context."
        return (
            "You are Smyalichi RAG assistant for competitor price monitoring platform.\n"
            "Answer in the same language as the question.\n"
            "Cite chunk ids like [1], [2] when relevant.\n\n"
            f"Module: {request.module}\n"
            f"Question: {request.question}\n\n"
            f"Context:\n{context}"
        )

    def _call_llm(self, model: str, prompt: str) -> str:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a precise technical assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }
        with httpx.Client(base_url=self.settings.llm_base_url, timeout=self.settings.llm_timeout_seconds) as client:
            response = client.post("/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

    def _fallback_answer(self, request: RagQueryRequest, chunks: list[RetrievedChunk]) -> str:
        if not chunks:
            return (
                f"Не удалось найти релевантный контекст по модулю `{request.module}` "
                f"для вопроса: {request.question}"
            )
        top = chunks[0]
        return (
            f"LLM недоступен. Наиболее релевантный фрагмент {top.citation_id} "
            f"({top.metadata.path}, score={top.score:.3f}): {top.content[:500]}"
        )
