export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

export interface ChatSession {
  session_id: string;
  messages: ChatMessage[];
  created_at: string;
  updated_at: string;
}

export interface SendMessageRequest {
  message: string;
  session_id?: string;
}

export interface SendMessageResponse {
  session_id: string;
  reply: string;
  sources: string[];
}

export interface QueryRequest {
  question: string;
  top_k?: number;
}

export interface QueryResponse {
  answer: string;
  sources: string[];
  chunks_used: number;
  confidence: {
    best_distance: number;
    avg_distance: number;
  };
}

export interface SystemStats {
  chroma_stats: {
    collection_name: string;
    total_documents: number;
    chroma_dir: string;
  };
  embedding_model: string;
  llm_model: string;
  top_k_retrieval: number;
}

export interface HealthCheck {
  status: "healthy" | "degraded";
  ollama_connected: boolean;
  chroma_ready: boolean;
}
