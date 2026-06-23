from __future__ import annotations

import argparse
from pathlib import Path

from ingestors.smyalichi.code_ingestor import SmyalichiCodeIngestor
from pipeline.config import Settings
from pipeline.indexer import PgVectorIndexer
from pipeline.parent_child import attach_parent_child, flatten_for_index


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest Smyalichi repository into RAG index")
    parser.add_argument("--root", type=Path, default=Path.cwd().parent)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ingestor = SmyalichiCodeIngestor(args.root)
    chunks = ingestor.ingest()
    chunks = flatten_for_index(attach_parent_child(chunks))
    print(f"Discovered {len(chunks)} chunks from {len(ingestor.discover_files())} files")

    if args.dry_run:
        for chunk in chunks[:5]:
            print(f"- {chunk.metadata.path} [{chunk.metadata.source_type}] {len(chunk.content)} chars")
        return

    settings = Settings()
    indexer = PgVectorIndexer(settings)
    indexed = indexer.upsert(chunks)
    print(f"Indexed {indexed} chunks into schema smyalichi_rag")


if __name__ == "__main__":
    main()
