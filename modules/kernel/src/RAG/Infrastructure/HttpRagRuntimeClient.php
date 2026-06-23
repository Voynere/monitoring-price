<?php

declare(strict_types=1);

namespace App\Context\Kernel\RAG\Infrastructure;

use App\Context\Kernel\RAG\Domain\RagAnswer;
use App\Context\Kernel\RAG\Domain\RagQuery;
use App\Context\Kernel\RAG\Domain\RetrievedChunk;
use App\Context\Kernel\RAG\Port\RagIndexerPort;
use App\Context\Kernel\RAG\Port\RagQueryPort;
use App\Context\Kernel\RAG\Port\RagRetrieverPort;
use Symfony\Contracts\HttpClient\HttpClientInterface;

final class HttpRagRuntimeClient implements RagQueryPort, RagRetrieverPort, RagIndexerPort
{
    public function __construct(
        private readonly HttpClientInterface $httpClient,
        private readonly string $baseUrl,
    ) {
    }

    public function ask(RagQuery $query): RagAnswer
    {
        $response = $this->httpClient->request('POST', rtrim($this->baseUrl, '/').'/rag/smyalichi/query', [
            'json' => [
                'project' => $query->project,
                'module' => $query->module,
                'question' => $query->question,
                'filters' => $query->filters,
                'model' => $query->model,
                'top_k' => $query->topK,
            ],
            'timeout' => 120,
        ]);

        $payload = $response->toArray(false);
        $answer = $payload['answer'] ?? [];

        $citations = [];
        foreach ($answer['citations'] ?? [] as $citation) {
            $citations[] = new RetrievedChunk(
                chunkId: (string) ($citation['chunk_id'] ?? ''),
                content: (string) ($citation['content'] ?? ''),
                score: (float) ($citation['score'] ?? 0.0),
                metadata: is_array($citation['metadata'] ?? null) ? $citation['metadata'] : [],
                citationId: (string) ($citation['citation_id'] ?? ''),
            );
        }

        return new RagAnswer(
            answer: (string) ($answer['answer'] ?? ''),
            citations: $citations,
            model: (string) ($answer['model'] ?? $query->model),
            latencyMs: (int) ($answer['latency_ms'] ?? 0),
        );
    }

    public function retrieve(RagQuery $query): array
    {
        return $this->ask($query)->citations;
    }

    public function enqueueReindex(array $payload): void
    {
        $this->httpClient->request('POST', rtrim($this->baseUrl, '/').'/rag/smyalichi/reindex', [
            'json' => $payload,
            'timeout' => 30,
        ]);
    }
}
