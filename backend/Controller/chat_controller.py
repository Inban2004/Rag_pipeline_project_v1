# controller/chat_controller.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import APIRouter, HTTPException
from Models.models import (
    SendMessageRequest, SendMessageResponse,
    ChatSession
)
from Service.chat_service import ChatService


router = APIRouter(prefix="/api/v1/chat", tags=["chat"])
chat_service = ChatService()


@router.post("/send", response_model=SendMessageResponse)
async def send_message(request: SendMessageRequest):
    try:
        result = chat_service.send_message(
            message=request.message,
            session_id=request.session_id
        )
        return SendMessageResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}", response_model=ChatSession)
async def get_history(session_id: str):
    history = chat_service.get_history(session_id)
    if not history:
        raise HTTPException(status_code=404, detail="Session not found")
    return ChatSession(**history)


@router.delete("/history/{session_id}")
async def clear_history(session_id: str):
    success = chat_service.clear_history(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "success", "message": "History cleared"}


@router.get("/sessions")
async def list_sessions():
    return {"sessions": chat_service.list_sessions()}
