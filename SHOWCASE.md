# Showcase slice integration

Этот публичный репозиторий содержит модуль `site` и scaffold Sprint 1 RAG. Полный Symfony-монолит (`price`, `data`, `crm`, `kernel`) находится в приватном Gitea.

## Что есть в showcase

- `modules/site/` — публичная витрина, SEO, блог
- `modules/kernel/src/RAG/` — контракты и HTTP-клиент к RAG runtime
- `rag-platform/` — FastAPI runtime, ingestor, hybrid search, workers
- `docs/rag/PLAN.md` — архитектурный план Deep RAG

## Что нужно из полного монолита

| Артефакт | Назначение |
|----------|------------|
| `translations/site.{ru,en}.yaml` | ~216 ключей `site` domain |
| `templates/base.html.twig` | родительский layout |
| `assets/images/`, `assets/videos/` | медиа для лендинга |
| Webpack Encore `site_app` entry | JS bundle |
| `config/services.yaml` | DI wiring |

## Локальный preview site module

1. Скопировать showcase в `modules/site` полного проекта.
2. Убедиться, что маршруты site подключены через `routes/site.yaml`.
3. Очистить кэш Symfony и открыть `/` и `/en`.

## Локальный запуск RAG

См. [rag-platform/README.md](../rag-platform/README.md) и [docs/rag/DEPLOY.md](rag/DEPLOY.md).

## Sprint 1 статус

- [x] `rag-platform` scaffold
- [x] schema `smyalichi_rag`
- [x] code ingestor (showcase + docs)
- [x] hybrid search + Qwen gateway (с fallback)
- [x] eval: 25 вопросов
- [x] `kernel/RAG` PHP facade
- [ ] ingest полного Gitea monolith (требует credentials)
- [ ] admin UI подсказок по парсерам (Sprint 2)
