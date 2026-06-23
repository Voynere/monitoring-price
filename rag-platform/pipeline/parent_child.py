from __future__ import annotations

from dataclasses import dataclass

from core.models import ChunkMetadata, DocumentChunk


@dataclass(frozen=True)
class ParentChildChunk:
    parent: DocumentChunk
    children: list[DocumentChunk]


def attach_parent_child(chunks: list[DocumentChunk]) -> list[ParentChildChunk]:
    """Group method-level chunks under their parent class/file chunk."""
    by_path: dict[str, list[DocumentChunk]] = {}
    for chunk in chunks:
        by_path.setdefault(chunk.metadata.path, []).append(chunk)

    result: list[ParentChildChunk] = []
    for path, path_chunks in by_path.items():
        class_chunks = [c for c in path_chunks if c.metadata.extra.get("kind") == "class"]
        method_chunks = [c for c in path_chunks if c.metadata.extra.get("kind") == "method"]
        if method_chunks and not class_chunks:
            sample = method_chunks[0]
            parent = DocumentChunk(
                id=f"{sample.id}_parent",
                content=f"file {path}",
                metadata=sample.metadata.model_copy(
                    update={"extra": {**sample.metadata.extra, "kind": "class", "role": "parent", "symbol": path}}
                ),
            )
        elif class_chunks:
            parent = class_chunks[0]
            parent_meta = parent.metadata.model_copy(
                update={"extra": {**parent.metadata.extra, "role": "parent"}}
            )
            parent = parent.model_copy(update={"metadata": parent_meta})
        else:
            for chunk in path_chunks:
                result.append(ParentChildChunk(parent=chunk, children=[]))
            continue

        children = []
        for child in method_chunks:
            child_meta = child.metadata.model_copy(
                update={"extra": {**child.metadata.extra, "role": "child", "parent_id": parent.id}}
            )
            children.append(child.model_copy(update={"metadata": child_meta}))
        result.append(ParentChildChunk(parent=parent, children=children))
    return result


def flatten_for_index(groups: list[ParentChildChunk]) -> list[DocumentChunk]:
  flattened: list[DocumentChunk] = []
  for group in groups:
      flattened.append(group.parent)
      flattened.extend(group.children)
  return flattened
