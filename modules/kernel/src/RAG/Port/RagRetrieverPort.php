<?php

declare(strict_types=1);

namespace App\Context\Kernel\RAG\Port;

use App\Context\Kernel\RAG\Domain\RagQuery;
use App\Context\Kernel\RAG\Domain\RetrievedChunk;

interface RagRetrieverPort
{
    /**
     * @return list<RetrievedChunk>
     */
    public function retrieve(RagQuery $query): array;
}
