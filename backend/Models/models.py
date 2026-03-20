# models.py

import sys
from pathlib import Path

# Add parent directory to path so we can import config
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 3  # Allow override per query


class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    chunks_used: int
    confidence: Dict[str, float]  # best_distance, avg_distance


class IngestRequest(BaseModel):
    pdf_path: str  # Relative to data/pdfs/ or absolute


class IngestResponse(BaseModel):
    file: str
    chunks_added: int
    total_docs_in_db: int
    error: Optional[str] = None


class SystemStats(BaseModel):
    chroma_stats: Dict[str, Any]
    embedding_model: str
    llm_model: str
    top_k_retrieval: int


class HealthCheck(BaseModel):
    status: str
    ollama_connected: bool
    chroma_ready: bool


# Chat Models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: str


class ChatSession(BaseModel):
    session_id: str
    messages: List[ChatMessage]
    created_at: str
    updated_at: str


class SendMessageRequest(BaseModel):
    message: str
    session_id: Optional[str] = None  # None = create new session


class SendMessageResponse(BaseModel):
    session_id: str
    reply: str
    sources: List[str] = []