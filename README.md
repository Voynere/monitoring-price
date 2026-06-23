# Smyalichi Monitoring Price

## RU

Smyalichi Monitoring Price — платформа для мониторинга цен конкурентов и поддержки операционных решений в e-commerce.
Проект объединяет сбор и нормализацию данных, аналитические срезы, административные панели и публичную витрину.

### О проекте

- Контроль цен и изменений по конкурентам в разрезе городов, компаний и товарных групп.
- Централизованная обработка данных для внутренних команд.
- Публичный слой для презентации продукта и контент-каналов.

### Модульная архитектура

Проект реализован как модульный монолит с явными контекстами:

- `price` — доменная логика мониторинга цен и прикладные сценарии.
- `data` — проекции и обработка потоков данных.
- `crm` — процессы клиентского сопровождения и операционного взаимодействия.
- `site` — публичная веб-витрина.
- `seo` — отдельный контекст поисковой оптимизации и SEO-интеграций.
- `kernel` — общий runtime-слой и кросс-контекстная инфраструктура.

### Стек разработки

- Backend: `PHP 8.5+`, `Symfony`, `Doctrine ORM`, `Messenger`.
- Data & infra: `PostgreSQL`, `Redis`, `RabbitMQ`.
- Frontend: `Twig`, `JavaScript`, `Webpack Encore`, `CSS`.
- Quality: `PHPUnit`, `PHPStan`, `Deptrac`, CI pipelines.

### LLM/AI в продукте

- Используются собственные LLM-подходы для прикладных задач разбора сложных источников.
- Применяются доменные правила валидации и fallback-стратегии для стабильности результата.
- Классические алгоритмы и LLM-обработка объединены в единый production-пайплайн.

Публичная версия репозитория содержит безопасный showcase-срез и не раскрывает критичные внутренние реализации.

### Deep RAG (Sprint 1)

- Архитектурный план: [docs/rag/PLAN.md](docs/rag/PLAN.md)
- Runtime-сервис: [rag-platform/](rag-platform/)
- Symfony-фасад: [modules/kernel/src/RAG/](modules/kernel/src/RAG/)
- Деплой: [docs/rag/DEPLOY.md](docs/rag/DEPLOY.md)
- Интеграция showcase: [SHOWCASE.md](SHOWCASE.md)

---

## EN

Smyalichi Monitoring Price is a platform for competitor price monitoring and operational decision support in e-commerce.
It combines data collection and normalization, analytics views, admin tooling, and a public-facing product showcase.

### About the Project

- Tracks competitor prices and changes across cities, companies, and product groups.
- Provides centralized data processing for internal teams.
- Includes a public layer for product presentation and content channels.

### Modular Architecture

The project is built as a modular monolith with clear bounded contexts:

- `price` — core pricing-monitoring domain and use cases.
- `data` — projections and data flow processing.
- `crm` — customer-facing operations and business workflows.
- `site` — public web showcase.
- `seo` — dedicated SEO context and search-related integrations.
- `kernel` — shared runtime layer and cross-context infrastructure.

### Development Stack

- Backend: `PHP 8.5+`, `Symfony`, `Doctrine ORM`, `Messenger`.
- Data & infra: `PostgreSQL`, `Redis`, `RabbitMQ`.
- Frontend: `Twig`, `JavaScript`, `Webpack Encore`, `CSS`.
- Quality: `PHPUnit`, `PHPStan`, `Deptrac`, CI pipelines.

### LLM/AI in the Product

- Custom LLM-driven approaches are used for complex source parsing tasks.
- Domain-specific validation rules and fallback strategies are applied for reliability.
- Classical algorithms and LLM-based processing are combined in a single production pipeline.

This public repository exposes a safe showcase subset and does not include critical internal implementations.

### Deep RAG (Sprint 1)

- Architecture plan: [docs/rag/PLAN.md](docs/rag/PLAN.md)
- Runtime service: [rag-platform/](rag-platform/)
- Symfony facade: [modules/kernel/src/RAG/](modules/kernel/src/RAG/)
- Deploy guide: [docs/rag/DEPLOY.md](docs/rag/DEPLOY.md)
- Showcase integration: [SHOWCASE.md](SHOWCASE.md)
