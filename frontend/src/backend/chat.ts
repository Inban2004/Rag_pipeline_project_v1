import { apiRequest } from "./client";
import type {
  ChatMessage,
  ChatSession,
  SendMessageRequest,
  SendMessageResponse,
} from "./types";

export async function sendMessage(
  message: string,
  sessionId?: string
): Promise<SendMessageResponse> {
  const body: SendMessageRequest = { message };
  if (sessionId) {
    body.session_id = sessionId;
  }
  return apiRequest<SendMessageResponse>("/chat/send", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function getChatHistory(
  sessionId: string
): Promise<ChatSession> {
  return apiRequest<ChatSession>(`/chat/history/${sessionId}`);
}

export async function clearChatHistory(sessionId: string): Promise<void> {
  await apiRequest(`/chat/history/${sessionId}`, { method: "DELETE" });
}

export async function listChatSessions(): Promise<{
  sessions: Array<{
    session_id: string;
    message_count: number;
    created_at: string;
    updated_at: string;
  }>;
}> {
  return apiRequest("/chat/sessions");
}
