#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${RAG_BASE_URL:-http://localhost:8080}"

echo "==> health"
curl -fsS "${BASE_URL}/health" | tee /tmp/rag-health.json

echo "==> smyalichi health"
curl -fsS "${BASE_URL}/rag/smyalichi/health" | tee /tmp/rag-smyalichi-health.json

echo "==> query smoke"
curl -fsS -X POST "${BASE_URL}/rag/smyalichi/query" \
  -H 'Content-Type: application/json' \
  -d '{"project":"smyalichi","module":"site","question":"Какие страницы в sitemap?","top_k":3}' \
  | tee /tmp/rag-query.json

echo "OK"
