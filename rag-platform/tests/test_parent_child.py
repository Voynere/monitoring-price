from __future__ import annotations

from core.models import ChunkMetadata, DocumentChunk, SourceType
from ingestors.smyalichi.chunker import chunk_php_file
from pipeline.parent_child import attach_parent_child, flatten_for_index


def test_parent_child_groups_methods_under_class(tmp_path) -> None:
    php = tmp_path / "modules/price/src/Parser/Fallback.php"
    php.parent.mkdir(parents=True)
    php.write_text(
        """<?php
final class Fallback
{
    public function run(): void
    {
    }

    public function retry(): void
    {
    }
}
""",
        encoding="utf-8",
    )
    chunks = chunk_php_file(php, tmp_path, "sha")
    groups = attach_parent_child(chunks)
    flat = flatten_for_index(groups)
    assert len(flat) >= 2
    method_chunks = [c for c in flat if c.metadata.extra.get("kind") == "method"]
    assert method_chunks
    assert method_chunks[0].metadata.extra.get("parent_id")
