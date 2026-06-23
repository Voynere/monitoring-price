# Деплой RAG Platform (Sprint 1)

## Prod topology

| Сервис | Порт | Назначение |
|--------|------|------------|
| `rag-api` | 8080 | FastAPI `/rag/smyalichi/query` |
| `rag-worker` | — | RabbitMQ consumer `rag.smyalichi` |
| `postgres` + pgvector | 5432 | schema `smyalichi_rag` |
| `redis` | 6379 | кэш embeddings |
| `rabbitmq` | 5672 | очередь индексации |
| `ollama` / vLLM | 11434 | Qwen + embedding runtime |

## Шаги выкладки

```bash
cd rag-platform
docker compose -f docker-compose.yml pull
docker compose -f docker-compose.yml up -d --build
docker compose exec rag-api rag-ingest --root /app/repo
curl -fsS http://localhost:8080/rag/smyalichi/health
```

## Интеграция с Symfony (Gitea monolith)

1. Скопировать `modules/kernel/src/RAG/` в полный монолит.
2. Зарегистрировать `HttpRagRuntimeClient` в DI с `RAG_RUNTIME_URL`.
3. Подключить use cases в `price` / `seo` / `data`.

```yaml
# config/services.yaml (фрагмент)
App\Context\Kernel\RAG\Infrastructure\HttpRagRuntimeClient:
  arguments:
    $baseUrl: '%env(RAG_RUNTIME_URL)%'
```

## Переменные окружения

| Переменная | Пример |
|------------|--------|
| `DATABASE_URL` | `postgresql://smyalichi:***@postgres:5432/smyalichi_rag` |
| `RABBITMQ_URL` | `amqp://guest:guest@rabbitmq:5672/` |
| `LLM_BASE_URL` | `http://ollama:11434/v1` |
| `EMBEDDING_DIMENSION` | `1024` |
| `RAG_USE_ML_EMBEDDER` | `1` в prod при наличии GPU |

## Post-deploy checks

- `GET /health` → `ok`
- `POST /rag/smyalichi/query` с тестовым вопросом из `tests/eval_questions.json`
- `POST /rag/smyalichi/reindex` → `queued`
- Langfuse trace для retrieval + generation (Sprint 3)
