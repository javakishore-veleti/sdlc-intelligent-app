"""Assistant endpoints: ask a question, list available collections."""
from fastapi import APIRouter

from common.constants.constants import DEFAULT_FRAMEWORK, DEFAULT_STRATEGY, DEFAULT_TOP_K
from facades.registry import build_qa_facade
from schemas.qa import AskRequest, AskResponse
from vector.chroma_client import list_collection_names

router = APIRouter(tags=["Assistant"])
_facade = build_qa_facade()


@router.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    """Answer a question from the ingested documentation, with citations."""
    return _facade.ask(
        question=req.question,
        framework=req.framework or DEFAULT_FRAMEWORK,
        strategy=req.strategy or DEFAULT_STRATEGY,
        filters={"project_id": req.project_id, "project_sprint": req.project_sprint},
        top_k=req.top_k or DEFAULT_TOP_K,
    )


@router.get("/collections")
def collections() -> list[str]:
    """List vector-DB collections (e.g. langchain__... and langgraph__...)."""
    return list_collection_names()
