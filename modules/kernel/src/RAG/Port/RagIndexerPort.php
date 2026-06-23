<?php

declare(strict_types=1);

namespace App\Context\Kernel\RAG\Port;

interface RagIndexerPort
{
    /**
     * @param array<string, mixed> $payload
     */
    public function enqueueReindex(array $payload): void;
}
