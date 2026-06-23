from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class SourceType(StrEnum):
    CODE = "code"
    DOC = "doc"
    CONFIG = "config"
    LOG = "log"
    BLOG = "blog"


class ChunkMetadata(BaseModel):
    project: str = "smyalichi"
    module: str
    source_type: SourceType
    path: str
    git_sha: str | None = None
    language: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class DocumentChunk(BaseModel):
    id: str | None = None
    content: str
    metadata: ChunkMetadata
    embedding: list[float] | None = None
    content_tsv: str | None = None


class RetrievedChunk(BaseModel):
    chunk_id: str
    content: str
    score: float
    metadata: ChunkMetadata
    citation_id: str


class RagQueryRequest(BaseModel):
    project: str = "smyalichi"
    module: str
    question: str
    filters: dict[str, list[str]] = Field(default_factory=dict)
    model: str = "qwen3.6-35b-a3b"
    top_k: int = 8


class RagAnswer(BaseModel):
    answer: str
    citations: list[RetrievedChunk]
    model: str
    latency_ms: int


class RagQueryResponse(BaseModel):
    project: str
    module: str
    question: str
    answer: RagAnswer
