from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://smyalichi:smyalichi@localhost:5432/smyalichi_rag"
    redis_url: str = "redis://localhost:6379/0"
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"
    embedding_model: str = "BAAI/bge-m3"
    embedding_dimension: int = 1024
    ollama_base_url: str = "http://localhost:11434"
    llm_base_url: str = "http://localhost:11434/v1"
    llm_model: str = "qwen3.6-35b-a3b"
    llm_timeout_seconds: float = 120.0
    rag_queue_name: str = "rag.smyalichi"
