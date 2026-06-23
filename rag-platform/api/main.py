from __future__ import annotations

from fastapi import FastAPI

from api.smyalichi.router import router as smyalichi_router

app = FastAPI(title="Smyalichi RAG Platform", version="0.1.0")
app.include_router(smyalichi_router)


@app.get("/health")
def root_health() -> dict[str, str]:
    return {"status": "ok"}
