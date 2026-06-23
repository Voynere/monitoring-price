<?php

declare(strict_types=1);

namespace App\Context\Kernel\RAG\Port;

use App\Context\Kernel\RAG\Domain\RagAnswer;
use App\Context\Kernel\RAG\Domain\RagQuery;

interface RagQueryPort
{
    public function ask(RagQuery $query): RagAnswer;
}
