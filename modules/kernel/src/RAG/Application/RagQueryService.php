<?php

declare(strict_types=1);

namespace App\Context\Kernel\RAG\Application;

use App\Context\Kernel\RAG\Domain\RagAnswer;
use App\Context\Kernel\RAG\Domain\RagQuery;
use App\Context\Kernel\RAG\Port\RagQueryPort;

final class RagQueryService implements RagQueryPort
{
    public function __construct(
        private readonly BuildRagContextUseCase $buildRagContextUseCase,
    ) {
    }

    public function ask(RagQuery $query): RagAnswer
    {
        return $this->buildRagContextUseCase->execute($query);
    }
}
