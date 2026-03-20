import { apiRequest } from "./client";
import type {
  QueryRequest,
  QueryResponse,
  SystemStats,
  HealthCheck,
} from "./types";

export async function query(question: string, topK?: number): Promise<QueryResponse> {
  const body: QueryRequest = { question };
  if (topK !== undefined) {
    body.top_k = topK;
  }
  return apiRequest<QueryResponse>("/query", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function getStats(): Promise<SystemStats> {
  return apiRequest<SystemStats>("/stats");
}

export async function healthCheck(): Promise<HealthCheck> {
  return apiRequest<HealthCheck>("/health");
}
