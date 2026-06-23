from __future__ import annotations

import subprocess
from pathlib import Path

from core.models import DocumentChunk
from ingestors.smyalichi.chunker import chunk_file

DEFAULT_GLOBS = (
    "modules/**/*.php",
    "templates/**/*.twig",
    "docs/**/*.md",
    "rag-platform/**/*.py",
    "README.md",
)


class SmyalichiCodeIngestor:
    def __init__(self, root: Path, include_globs: tuple[str, ...] = DEFAULT_GLOBS) -> None:
        self.root = root.resolve()
        self.include_globs = include_globs

    def current_git_sha(self) -> str | None:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip() or None
        except (subprocess.SubprocessError, FileNotFoundError):
            return None

    def discover_files(self) -> list[Path]:
        files: set[Path] = set()
        for pattern in self.include_globs:
            for path in self.root.glob(pattern):
                if path.is_file() and ".git" not in path.parts:
                    files.add(path)
        return sorted(files)

    def ingest(self) -> list[DocumentChunk]:
        git_sha = self.current_git_sha()
        chunks: list[DocumentChunk] = []
        for path in self.discover_files():
            chunks.extend(chunk_file(path, self.root, git_sha))
        return chunks
