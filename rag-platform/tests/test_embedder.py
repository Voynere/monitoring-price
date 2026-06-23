from __future__ import annotations

from pipeline.embedder import HashEmbedder


def test_hash_embedder_dimension_and_normalization() -> None:
    embedder = HashEmbedder(dimension=128)
    vectors = embedder.embed(["hello", "world"])
    assert len(vectors) == 2
    assert len(vectors[0]) == 128
    assert vectors[0] != vectors[1]
    norm = sum(v * v for v in vectors[0]) ** 0.5
    assert abs(norm - 1.0) < 1e-6
