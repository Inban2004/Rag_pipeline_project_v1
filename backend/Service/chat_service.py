# service/chat_service.py
import sys
from pathlib import Path
import uuid
import json
from datetime import datetime
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import DATA_DIR
from Service.rag_orchestrator import RAGOrchestrator


class ChatService:
    def __init__(self):
        self.chats_dir = DATA_DIR / "chats"
        self.chats_dir.mkdir(exist_ok=True)
        self.orchestrator = RAGOrchestrator()
    
    def _get_session_path(self, session_id: str) -> Path:
        return self.chats_dir / f"{session_id}.json"
    
    def _load_session(self, session_id: str) -> Optional[Dict]:
        path = self._get_session_path(session_id)
        if path.exists():
            with open(path, "r") as f:
                return json.load(f)
        return None
    
    def _save_session(self, session: Dict):
        path = self._get_session_path(session["session_id"])
        with open(path, "w") as f:
            json.dump(session, f, indent=2)
    
    def _create_new_session(self) -> Dict:
        now = datetime.now().isoformat()
        return {
            "session_id": str(uuid.uuid4()),
            "messages": [],
            "created_at": now,
            "updated_at": now
        }
    
    def send_message(self, message: str, session_id: Optional[str] = None) -> Dict:
        if session_id:
            session = self._load_session(session_id)
            if not session:
                session = self._create_new_session()
                session["session_id"] = session_id
        else:
            session = self._create_new_session()
        
        user_message = {
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        }
        session["messages"].append(user_message)
        
        rag_result = self.orchestrator.answer(message)
        
        bot_message = {
            "role": "assistant",
            "content": rag_result["answer"],
            "timestamp": datetime.now().isoformat()
        }
        session["messages"].append(bot_message)
        
        session["updated_at"] = datetime.now().isoformat()
        self._save_session(session)
        
        return {
            "session_id": session["session_id"],
            "reply": rag_result["answer"],
            "sources": rag_result["sources"]
        }
    
    def get_history(self, session_id: str) -> Optional[Dict]:
        session = self._load_session(session_id)
        if session:
            return {
                "session_id": session["session_id"],
                "messages": session["messages"],
                "created_at": session["created_at"],
                "updated_at": session["updated_at"]
            }
        return None
    
    def clear_history(self, session_id: str) -> bool:
        path = self._get_session_path(session_id)
        if path.exists():
            path.unlink()
            return True
        return False
    
    def list_sessions(self) -> List[Dict]:
        sessions = []
        for file in self.chats_dir.glob("*.json"):
            with open(file, "r") as f:
                data = json.load(f)
                sessions.append({
                    "session_id": data["session_id"],
                    "message_count": len(data["messages"]),
                    "created_at": data["created_at"],
                    "updated_at": data["updated_at"]
                })
        return sorted(sessions, key=lambda x: x["updated_at"], reverse=True)
