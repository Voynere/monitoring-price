from __future__ import annotations

import json
from typing import Any

import psycopg
from pgvector.psycopg import register_vector

from core.contracts import EmbedderPort, IndexerPort
from core.models import DocumentChunk
from pipeline.config import Settings
from pipeline.embedder import build_embedder


class PgVectorIndexer(IndexerPort):
    def __init__(self, settings: Settings, embedder: EmbedderPort | None = None) -> None:
        self.settings = settings
        self.embedder = embedder or build_embedder(settings)

    def upsert(self, chunks: list[DocumentChunk]) -> int:
        if not chunks:
            return 0

        texts = [chunk.content for chunk in chunks]
        embeddings = self.embedder.embed(texts)

        with psycopg.connect(self.settings.database_url) as conn:
            register_vector(conn)
            with conn.cursor() as cur:
                for chunk, embedding in zip(chunks, embeddings, strict=True):
                    chunk_id = chunk.id or self._stable_id(chunk)
                    metadata_json = chunk.metadata.model_dump(mode="json")
                    cur.execute(
                        """
                        INSERT INTO smyalichi_rag.chunks
                            (id, content, embedding, metadata, module, source_type, path, content_tsv)
                        VALUES
                            (%s, %s, %s, %s::jsonb, %s, %s, %s, to_tsvector('simple', %s))
                        ON CONFLICT (id) DO UPDATE SET
                            content = EXCLUDED.content,
                            embedding = EXCLUDED.embedding,
                            metadata = EXCLUDED.metadata,
                            module = EXCLUDED.module,
                            source_type = EXCLUDED.source_type,
                            path = EXCLUDED.path,
                            content_tsv = EXCLUDED.content_tsv,
                            updated_at = NOW()
                        """,
                        (
                            chunk_id,
                            chunk.content,
                            embedding,
                            json.dumps(metadata_json),
                            chunk.metadata.module,
                            chunk.metadata.source_type.value,
                            chunk.metadata.path,
                            chunk.content,
                        ),
                    )
            conn.commit()
        return len(chunks)

    @staticmethod
    def _stable_id(chunk: DocumentChunk) -> str:
        digest = json.dumps(
            {"path": chunk.metadata.path, "content": chunk.content[:200]},
            sort_keys=True,
        )
        return "chunk_" + __import__("hashlib").sha256(digest.encode()).hexdigest()[:16]


def fetch_chunk_count(settings: Settings) -> int:
    with psycopg.connect(settings.database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM smyalichi_rag.chunks")
            row = cur.fetchone()
            return int(row[0]) if row else 0
