from __future__ import annotations

from abc import ABC, abstractmethod

from core.models import DocumentChunk, RagAnswer, RagQueryRequest, RetrievedChunk


class EmbedderPort(ABC):
    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError

    @property
    @abstractmethod
    def dimension(self) -> int:
        raise NotImplementedError


class IndexerPort(ABC):
    @abstractmethod
    def upsert(self, chunks: list[DocumentChunk]) -> int:
        raise NotImplementedError


class RetrieverPort(ABC):
    @abstractmethod
    def retrieve(self, request: RagQueryRequest, query_embedding: list[float]) -> list[RetrievedChunk]:
        raise NotImplementedError


class LlmGatewayPort(ABC):
    @abstractmethod
    def generate(self, request: RagQueryRequest, chunks: list[RetrievedChunk]) -> RagAnswer:
        raise NotImplementedError
