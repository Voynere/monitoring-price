from __future__ import annotations

from pathlib import Path

from ingestors.smyalichi.chunker import chunk_php_file, chunk_text_file
from ingestors.smyalichi.code_ingestor import SmyalichiCodeIngestor


def test_chunk_php_file_splits_methods(tmp_path: Path) -> None:
    php = tmp_path / "Example.php"
    php.write_text(
        """<?php
final class Example
{
    public function alpha(): string
    {
        return 'a';
    }

    public function beta(): int
    {
        return 1;
    }
}
""",
        encoding="utf-8",
    )
    chunks = chunk_php_file(php, tmp_path, "abc123")
    assert len(chunks) >= 2
    assert any("alpha" in chunk.content for chunk in chunks)
    assert chunks[0].metadata.source_type.value == "code"


def test_chunk_text_file_overlap(tmp_path: Path) -> None:
    md = tmp_path / "doc.md"
    md.write_text("word " * 500, encoding="utf-8")
    chunks = chunk_text_file(md, tmp_path, None, max_chunk=400, overlap=50)
    assert len(chunks) > 1


def test_ingestor_discovers_showcase_files() -> None:
    root = Path(__file__).resolve().parents[2]
    ingestor = SmyalichiCodeIngestor(root)
    files = ingestor.discover_files()
    assert any("SitePageRegistry.php" in str(path) for path in files)
    chunks = ingestor.ingest()
    assert len(chunks) > 20
