FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY core ./core
COPY ingestors ./ingestors
COPY pipeline ./pipeline
COPY retrieval ./retrieval
COPY llm_gateway ./llm_gateway
COPY api ./api
COPY workers ./workers
COPY db ./db

RUN pip install --no-cache-dir -e .

EXPOSE 8080

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
