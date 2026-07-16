"""Request/response schemas for the assistant."""
from typing import Any, Optional

from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str
    framework: Optional[str] = None  # langchain | langgraph (default from config)
    strategy: Optional[str] = None
    project_id: Optional[str] = None
    project_sprint: Optional[str] = None
    top_k: Optional[int] = None


class Citation(BaseModel):
    document: Optional[str] = None
    application: Optional[str] = None
    sprint: Optional[str] = None
    page: Optional[int] = None


class RetrievedChunk(BaseModel):
    text: str
    distance: Optional[float] = None
    metadata: dict[str, Any] = {}


class AskResponse(BaseModel):
    answer: str
    framework: str
    strategy: str
    citations: list[Citation]
    retrieved: list[RetrievedChunk]
