<?php

declare(strict_types=1);

namespace App\Context\Kernel\RAG\Application;

use App\Context\Kernel\RAG\Domain\RagAnswer;
use App\Context\Kernel\RAG\Domain\RagQuery;
use App\Context\Kernel\RAG\Infrastructure\HttpRagRuntimeClient;

final class BuildRagContextUseCase
{
    public function __construct(
        private readonly HttpRagRuntimeClient $ragRuntimeClient,
    ) {
    }

    public function execute(RagQuery $query): RagAnswer
    {
        return $this->ragRuntimeClient->ask($query);
    }
}
