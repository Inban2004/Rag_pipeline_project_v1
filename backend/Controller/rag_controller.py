# controller/rag_controller.py

import sys
from pathlib import Path

# Add parent directory to path so we can import config
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import APIRouter, HTTPException
from Models.models import (
    QueryRequest, QueryResponse,
    IngestRequest, IngestResponse,
    SystemStats, HealthCheck
)
from Service.rag_orchestrator import RAGOrchestrator
import requests
from config import OLLAMA_HOST, PDF_DIR


router = APIRouter(prefix="/api/v1", tags=["rag"])
orchestrator = RAGOrchestrator()


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Check if all services are up."""
    try:
        # Test Ollama
        ollama_ok = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5).status_code == 200
    except:
        ollama_ok = False
    
    return HealthCheck(
        status="healthy" if ollama_ok else "degraded",
        ollama_connected=ollama_ok,
        chroma_ready=orchestrator.chroma.get_stats()["total_documents"] > 0
    )


@router.get("/stats", response_model=SystemStats)
async def get_stats():
    """Get RAG system statistics."""
    return SystemStats(**orchestrator.get_stats())


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Ask a question, get RAG-powered answer.
    """
    try:
        # Override top_k if provided
        original_k = orchestrator.top_k
        if request.top_k:
            orchestrator.top_k = request.top_k
        
        result = orchestrator.answer(request.question)
        
        # Restore default
        orchestrator.top_k = original_k
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            chunks_used=result["chunks_used"],
            confidence=result["retrieval_confidence"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest", response_model=IngestResponse)
async def ingest(request: IngestRequest):
    """
    Ingest a PDF into the RAG system.
    """
    result = orchestrator.ingest_pdf(request.pdf_path)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return IngestResponse(**result)


@router.get("/pdfs")
async def list_pdfs():
    """List all PDFs in the data folder."""
    pdfs = []
    for f in PDF_DIR.glob("*.pdf"):
        pdfs.append({
            "name": f.name,
            "size": f.stat().st_size,
            "path": str(f)
        })
    return {"pdfs": pdfs, "count": len(pdfs)}


@router.delete("/pdfs/{filename}")
async def delete_pdf(filename: str):
    """Delete a PDF file."""
    pdf_path = PDF_DIR / filename
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="PDF not found")
    
    pdf_path.unlink()
    return {"status": "success", "message": f"Deleted {filename}"}