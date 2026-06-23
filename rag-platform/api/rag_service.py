from __future__ import annotations

import time

from core.models import RagAnswer, RagQueryRequest, RagQueryResponse
from pipeline.config import Settings
from pipeline.embedder import build_embedder
from llm_gateway.qwen_client import QwenLlmGateway
from retrieval.reranker import SimpleReranker
from retrieval.retriever import PgHybridRetriever


class RagQueryService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        self.embedder = build_embedder(self.settings)
        self.retriever = PgHybridRetriever(self.settings)
        self.reranker = SimpleReranker()
        self.llm = QwenLlmGateway(self.settings)

    def ask(self, request: RagQueryRequest) -> RagQueryResponse:
        started = time.perf_counter()
        query_embedding = self.embedder.embed([request.question])[0]
        retrieved = self.retriever.retrieve(request, query_embedding)
        reranked = self.reranker.rerank(request.question, retrieved, top_k=request.top_k)
        answer = self.llm.generate(request, reranked)
        _ = int((time.perf_counter() - started) * 1000)
        return RagQueryResponse(
            project=request.project,
            module=request.module,
            question=request.question,
            answer=answer,
        )
