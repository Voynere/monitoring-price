from __future__ import annotations

import hashlib
import re
from pathlib import Path

from core.models import ChunkMetadata, DocumentChunk, SourceType

PHP_CLASS_PATTERN = re.compile(
    r"^(?:(?:final|abstract)\s+)?class\s+(\w+).*?\{(.*?)^\}",
    re.MULTILINE | re.DOTALL,
)
PHP_METHOD_PATTERN = re.compile(
    r"(?:(?:public|private|protected)\s+)?function\s+(\w+)\s*\([^)]*\)\s*(?::\s*\??[\w\\|]+)?\s*\{(.*?)^\s*\}",
    re.MULTILINE | re.DOTALL,
)
TWIG_BLOCK_PATTERN = re.compile(r"\{%\s*block\s+(\w+)\s*%\}(.*?)\{%\s*endblock\s*%\}", re.DOTALL)


def _chunk_id(path: str, index: int, label: str) -> str:
    digest = hashlib.sha256(f"{path}:{index}:{label}".encode()).hexdigest()[:16]
    return f"chunk_{digest}"


def _module_from_path(path: Path, root: Path) -> str:
    parts = path.relative_to(root).parts
    if len(parts) >= 2 and parts[0] == "modules":
        return parts[1]
    if parts[0] == "rag-platform":
        return "rag"
    if parts[0] == "docs":
        return "docs"
    return "site"


def _source_type_for_suffix(suffix: str) -> SourceType:
    mapping = {
        ".php": SourceType.CODE,
        ".twig": SourceType.BLOG,
        ".md": SourceType.DOC,
        ".yaml": SourceType.CONFIG,
        ".yml": SourceType.CONFIG,
        ".sql": SourceType.CONFIG,
    }
    return mapping.get(suffix, SourceType.DOC)


def chunk_php_file(path: Path, root: Path, git_sha: str | None) -> list[DocumentChunk]:
    text = path.read_text(encoding="utf-8", errors="replace")
    module = _module_from_path(path, root)
    chunks: list[DocumentChunk] = []

    for class_index, match in enumerate(PHP_CLASS_PATTERN.finditer(text)):
        class_name = match.group(1)
        class_body = match.group(2)
        header = f"class {class_name}"
        methods = list(PHP_METHOD_PATTERN.finditer(class_body))
        if not methods:
            chunks.append(
                DocumentChunk(
                    id=_chunk_id(str(path), class_index, class_name),
                    content=f"{header}\n{class_body.strip()}",
                    metadata=ChunkMetadata(
                        module=module,
                        source_type=SourceType.CODE,
                        path=str(path.relative_to(root)),
                        git_sha=git_sha,
                        language="php",
                        extra={"symbol": class_name, "kind": "class"},
                    ),
                )
            )
            continue

        for method_index, method in enumerate(methods):
            method_name = method.group(1)
            method_body = method.group(2).strip()
            content = f"{header}\nfunction {method_name}() {{\n{method_body}\n}}"
            chunks.append(
                DocumentChunk(
                    id=_chunk_id(str(path), class_index * 100 + method_index, f"{class_name}::{method_name}"),
                    content=content,
                    metadata=ChunkMetadata(
                        module=module,
                        source_type=SourceType.CODE,
                        path=str(path.relative_to(root)),
                        git_sha=git_sha,
                        language="php",
                        extra={"symbol": f"{class_name}::{method_name}", "kind": "method"},
                    ),
                )
            )

    if not chunks:
        chunks.append(
            DocumentChunk(
                id=_chunk_id(str(path), 0, "file"),
                content=text[:4000],
                metadata=ChunkMetadata(
                    module=module,
                    source_type=SourceType.CODE,
                    path=str(path.relative_to(root)),
                    git_sha=git_sha,
                    language="php",
                    extra={"kind": "file"},
                ),
            )
        )
    return chunks


def chunk_twig_file(path: Path, root: Path, git_sha: str | None) -> list[DocumentChunk]:
    text = path.read_text(encoding="utf-8", errors="replace")
    module = _module_from_path(path, root)
    chunks: list[DocumentChunk] = []

    for index, match in enumerate(TWIG_BLOCK_PATTERN.finditer(text)):
        block_name = match.group(1)
        block_body = match.group(2).strip()
        if len(block_body) < 40:
            continue
        chunks.append(
            DocumentChunk(
                id=_chunk_id(str(path), index, block_name),
                content=f"block {block_name}:\n{block_body}",
                metadata=ChunkMetadata(
                    module=module,
                    source_type=SourceType.BLOG,
                    path=str(path.relative_to(root)),
                    git_sha=git_sha,
                    language="twig",
                    extra={"block": block_name},
                ),
            )
        )

    if not chunks:
        chunks.append(
            DocumentChunk(
                id=_chunk_id(str(path), 0, "file"),
                content=text[:4000],
                metadata=ChunkMetadata(
                    module=module,
                    source_type=SourceType.BLOG,
                    path=str(path.relative_to(root)),
                    git_sha=git_sha,
                    language="twig",
                    extra={"kind": "file"},
                ),
            )
        )
    return chunks


def chunk_text_file(path: Path, root: Path, git_sha: str | None, max_chunk: int = 1800, overlap: int = 200) -> list[DocumentChunk]:
    text = path.read_text(encoding="utf-8", errors="replace")
    module = _module_from_path(path, root)
    source_type = _source_type_for_suffix(path.suffix.lower())
    chunks: list[DocumentChunk] = []

    if len(text) <= max_chunk:
        return [
            DocumentChunk(
                id=_chunk_id(str(path), 0, "file"),
                content=text,
                metadata=ChunkMetadata(
                    module=module,
                    source_type=source_type,
                    path=str(path.relative_to(root)),
                    git_sha=git_sha,
                    language=path.suffix.lstrip("."),
                ),
            )
        ]

    start = 0
    index = 0
    while start < len(text):
        end = min(start + max_chunk, len(text))
        piece = text[start:end]
        chunks.append(
            DocumentChunk(
                id=_chunk_id(str(path), index, f"part{index}"),
                content=piece,
                metadata=ChunkMetadata(
                    module=module,
                    source_type=source_type,
                    path=str(path.relative_to(root)),
                    git_sha=git_sha,
                    language=path.suffix.lstrip("."),
                    extra={"part": index},
                ),
            )
        )
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
        index += 1
    return chunks


def chunk_file(path: Path, root: Path, git_sha: str | None = None) -> list[DocumentChunk]:
    suffix = path.suffix.lower()
    if suffix == ".php":
        return chunk_php_file(path, root, git_sha)
    if suffix == ".twig":
        return chunk_twig_file(path, root, git_sha)
    return chunk_text_file(path, root, git_sha)
