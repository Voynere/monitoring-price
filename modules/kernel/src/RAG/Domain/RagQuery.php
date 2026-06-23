<?php

declare(strict_types=1);

namespace App\Context\Kernel\RAG\Domain;

final class RagQuery
{
    /**
     * @param array<string, list<string>> $filters
     */
    public function __construct(
        public readonly string $module,
        public readonly string $question,
        public readonly array $filters = [],
        public readonly string $model = 'qwen3.6-35b-a3b',
        public readonly int $topK = 8,
        public readonly string $project = 'smyalichi',
    ) {
    }
}
