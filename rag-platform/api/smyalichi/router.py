from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pathlib import Path
from pydantic import BaseModel, Field

from api.rag_service import RagQueryService
from core.models import RagQueryRequest, RagQueryResponse
from pipeline.config import Settings
from workers.index_worker import enqueue_reindex

router = APIRouter(prefix="/rag/smyalichi", tags=["smyalichi-rag"])
_service = RagQueryService()
_settings = Settings()


class ReindexRequest(BaseModel):
    root: str = Field(default=".", description="Repository root to ingest")


@router.post("/query", response_model=RagQueryResponse)
def query_rag(request: RagQueryRequest) -> RagQueryResponse:
    if request.project != "smyalichi":
        raise HTTPException(status_code=400, detail="Only project=smyalichi is supported in MVP")
    return _service.ask(request)


@router.post("/reindex")
def reindex(request: ReindexRequest) -> dict[str, str]:
    enqueue_reindex(Path(request.root), _settings)
    return {"status": "queued", "root": request.root}


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "smyalichi-rag"}
