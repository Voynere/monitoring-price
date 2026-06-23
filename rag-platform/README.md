# Smyalichi RAG Platform

Runtime-сервис Deep RAG для Смяличи Monitoring Price.

## Быстрый старт (dev)

```bash
cd rag-platform
pip install -e ".[dev]"
docker compose -f docker-compose.yml up -d postgres redis rabbitmq
psql "$DATABASE_URL" -f db/migrations/001_smyalichi_rag.sql
rag-ingest --root /workspace
uvicorn api.main:app --reload --host 0.0.0.0 --port 8080
```

## API

```http
POST /rag/smyalichi/query
Content-Type: application/json

{
  "project": "smyalichi",
  "module": "price",
  "question": "Как работает fallback при ошибке парсера?",
  "filters": { "source_type": ["code", "doc"] },
  "model": "qwen3.6-35b-a3b"
}
```

## Архитектура

См. [docs/rag/PLAN.md](../docs/rag/PLAN.md).

## Eval

```bash
pytest tests/test_eval_questions.py -v
```
