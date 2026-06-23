from __future__ import annotations

from core.models import ChunkMetadata, RetrievedChunk, SourceType
from retrieval.reranker import SimpleReranker


def test_reranker_boosts_code_chunks_for_parser_question() -> None:
    reranker = SimpleReranker()
    chunks = [
        RetrievedChunk(
            chunk_id="1",
            content="doc text",
            score=0.9,
            metadata=ChunkMetadata(module="docs", source_type=SourceType.DOC, path="README.md"),
            citation_id="[1]",
        ),
        RetrievedChunk(
            chunk_id="2",
            content="class ParserFallback",
            score=0.85,
            metadata=ChunkMetadata(module="price", source_type=SourceType.CODE, path="modules/price/Foo.php"),
            citation_id="[2]",
        ),
    ]
    ranked = reranker.rerank("How does parser fallback work?", chunks, top_k=2)
    assert ranked[0].chunk_id == "2"
