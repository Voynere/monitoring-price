from __future__ import annotations

from core.contracts import RetrieverPort
from core.models import ChunkMetadata, RagQueryRequest, RetrievedChunk, SourceType
from pipeline.config import Settings
from retrieval.hybrid_search import HybridSearch


class PgHybridRetriever(RetrieverPort):
    def __init__(self, settings: Settings) -> None:
        self.search = HybridSearch(settings)

    def retrieve(self, request: RagQueryRequest, query_embedding: list[float]) -> list[RetrievedChunk]:
        rows = self.search.search(
            question=request.question,
            query_embedding=query_embedding,
            module=request.module,
            filters=request.filters,
            top_k=request.top_k,
        )
        chunks: list[RetrievedChunk] = []
        for index, row in enumerate(rows, start=1):
            metadata = ChunkMetadata.model_validate(row["metadata"])
            chunks.append(
                RetrievedChunk(
                    chunk_id=row["id"],
                    content=row["content"],
                    score=float(row["score"]),
                    metadata=metadata,
                    citation_id=f"[{index}]",
                )
            )
        return chunks
