<?php

declare(strict_types=1);

namespace App\Context\Kernel\RAG\Domain;

final class RetrievedChunk
{
    /**
     * @param array<string, mixed> $metadata
     */
    public function __construct(
        public readonly string $chunkId,
        public readonly string $content,
        public readonly float $score,
        public readonly array $metadata,
        public readonly string $citationId,
    ) {
    }
}
