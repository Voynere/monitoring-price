<?php

declare(strict_types=1);

namespace App\Context\Kernel\RAG\Domain;

final class RagAnswer
{
    /**
     * @param list<RetrievedChunk> $citations
     */
    public function __construct(
        public readonly string $answer,
        public readonly array $citations,
        public readonly string $model,
        public readonly int $latencyMs,
    ) {
    }
}
