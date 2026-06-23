from __future__ import annotations

import json
from typing import Any

import psycopg
from pgvector.psycopg import register_vector

from pipeline.config import Settings


class HybridSearch:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def search(
        self,
        question: str,
        query_embedding: list[float],
        module: str,
        filters: dict[str, list[str]],
        top_k: int = 8,
    ) -> list[dict[str, Any]]:
        source_types = filters.get("source_type", [])
        params: list[Any] = [json.dumps(query_embedding), question, module, top_k]
        source_filter_sql = ""
        if source_types:
            source_filter_sql = "AND source_type = ANY(%s)"
            params.insert(3, source_types)

        sql = f"""
            WITH vector_hits AS (
                SELECT
                    id,
                    content,
                    metadata,
                    1 - (embedding <=> %s::vector) AS vector_score
                FROM smyalichi_rag.chunks
                WHERE module = %s
                {source_filter_sql}
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            ),
            keyword_hits AS (
                SELECT
                    id,
                    content,
                    metadata,
                    ts_rank_cd(content_tsv, plainto_tsquery('simple', %s)) AS keyword_score
                FROM smyalichi_rag.chunks
                WHERE module = %s
                {source_filter_sql}
                  AND content_tsv @@ plainto_tsquery('simple', %s)
                ORDER BY keyword_score DESC
                LIMIT %s
            ),
            merged AS (
                SELECT
                    COALESCE(v.id, k.id) AS id,
                    COALESCE(v.content, k.content) AS content,
                    COALESCE(v.metadata, k.metadata) AS metadata,
                    COALESCE(v.vector_score, 0) * 0.65 + COALESCE(k.keyword_score, 0) * 0.35 AS score
                FROM vector_hits v
                FULL OUTER JOIN keyword_hits k ON v.id = k.id
            )
            SELECT id, content, metadata, score
            FROM merged
            ORDER BY score DESC
            LIMIT %s
        """

        bind_params: list[Any]
        if source_types:
            bind_params = [
                query_embedding,
                module,
                source_types,
                query_embedding,
                top_k,
                question,
                module,
                source_types,
                question,
                top_k,
                top_k,
            ]
        else:
            bind_params = [
                query_embedding,
                module,
                query_embedding,
                top_k,
                question,
                module,
                question,
                top_k,
                top_k,
            ]

        with psycopg.connect(self.settings.database_url) as conn:
            register_vector(conn)
            with conn.cursor() as cur:
                cur.execute(sql, bind_params)
                rows = cur.fetchall()

        return [
            {
                "id": row[0],
                "content": row[1],
                "metadata": row[2] if isinstance(row[2], dict) else json.loads(row[2]),
                "score": row[3],
            }
            for row in rows
        ]
