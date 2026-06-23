CREATE EXTENSION IF NOT EXISTS vector;

CREATE SCHEMA IF NOT EXISTS smyalichi_rag;

CREATE TABLE IF NOT EXISTS smyalichi_rag.chunks (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1024) NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    module TEXT NOT NULL,
    source_type TEXT NOT NULL,
    path TEXT NOT NULL,
    content_tsv TSVECTOR,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_chunks_embedding
    ON smyalichi_rag.chunks
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_chunks_content_tsv
    ON smyalichi_rag.chunks
    USING GIN (content_tsv);

CREATE INDEX IF NOT EXISTS idx_chunks_module_source
    ON smyalichi_rag.chunks (module, source_type);

CREATE INDEX IF NOT EXISTS idx_chunks_path
    ON smyalichi_rag.chunks (path);
